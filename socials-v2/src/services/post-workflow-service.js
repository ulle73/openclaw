const { AppError } = require('../lib/app-error');
const { slugify } = require('../lib/string-utils');

class PostWorkflowService {
  constructor({ rootDir, template, sheets, copy, images, instagram, exporter }) {
    this.rootDir = rootDir;
    this.template = template;
    this.sheets = sheets;
    this.copy = copy;
    this.images = images;
    this.instagram = instagram;
    this.exporter = exporter;
  }

  async getDashboardData(options = {}) {
    const brandKey = this.template.resolveActiveBrandKey(options.brandKey);
    const templateData = await this.template.load({ brandKey });
    let posts = [];
    let sheetError = null;

    if (this.sheets.isConfigured()) {
      try {
        posts = await this.listPosts({ brandKey });
      } catch (error) {
        sheetError = error.message;
      }
    }

    const pipelineSummary = buildPipelineSummary(posts);
    const calendar = buildCalendarData(posts);

    return {
      template: templateData,
      diagnostics: {
        template: this.template.getTemplateStatus(brandKey),
        integrations: {
          sheetsConfigured: this.sheets.isConfigured(),
          openAiConfigured: this.copy.isConfigured(),
          geminiConfigured: this.images.isConfigured(),
          instagramConfigured: this.instagram.isConfigured(),
          instagramAutoPublishEnabled: this.instagram.isAutoPublishEnabled(),
        },
        sheetError,
      },
      posts,
      pipelineSummary,
      calendar,
    };
  }

  async bootstrapSheet() {
    return this.sheets.ensureHeaders();
  }

  async listPosts(options = {}) {
    const brandKey = this.template.resolveActiveBrandKey(options.brandKey);
    const rows = await this.sheets.listRowsForBrand(brandKey);
    return rows.sort((left, right) => right.rowIndex - left.rowIndex);
  }

  async processNext(options = {}) {
    const brandKey = this.template.resolveActiveBrandKey(options.brandKey);
    const post = await this.sheets.findNextRow(brandKey);

    if (!post) {
      return null;
    }

    return this.generateForExistingPost(post, {
      brandKey,
      regenerateCopy: true,
      regenerateImage: true,
    });
  }

  async runQueueTick(options = {}) {
    const published = await this.publishDueScheduled(options);
    if (published) {
      return { type: 'published_scheduled', post: published };
    }

    const processed = await this.processNext(options);
    if (processed) {
      return { type: 'processed_new', post: processed };
    }

    return null;
  }

  async publishDueScheduled(options = {}) {
    const brandKey = this.template.resolveActiveBrandKey(options.brandKey);
    const duePost = await this.sheets.findNextDueScheduledRow(brandKey, new Date());

    if (!duePost) {
      return null;
    }

    const platformKey = duePost.platform || 'instagram';
    const templateData = await this.template.loadPlatform(platformKey, { brandKey });
    return this.publishExistingPost(duePost, templateData);
  }

  async regenerateCopy(postId, options = {}) {
    const brandKey = this.template.resolveActiveBrandKey(options.brandKey);
    const post = await this.requirePost(postId, { brandKey });
    return this.generateForExistingPost(post, {
      brandKey,
      regenerateCopy: true,
      regenerateImage: false,
    });
  }

  async regenerateImage(postId, options = {}) {
    const brandKey = this.template.resolveActiveBrandKey(options.brandKey);
    const post = await this.requirePost(postId, { brandKey });
    return this.generateForExistingPost(post, {
      brandKey,
      regenerateCopy: false,
      regenerateImage: true,
    });
  }

  async saveReviewNotes(postId, reviewNotes, options = {}) {
    const brandKey = this.template.resolveActiveBrandKey(options.brandKey);
    const post = await this.requirePost(postId, { brandKey });

    return this.sheets.updateRow(post.rowIndex, {
      review_notes: reviewNotes || '',
      updated_at: new Date().toISOString(),
    });
  }

  async approvePost(postId, reviewNotes, options = {}) {
    const brandKey = this.template.resolveActiveBrandKey(options.brandKey);
    const post = await this.requirePost(postId, { brandKey });

    this.assertPublishablePost(post);

    return this.sheets.updateRow(post.rowIndex, {
      status: 'approved',
      review_notes: reviewNotes != null ? reviewNotes : post.review_notes,
      approved_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    });
  }

  async schedulePost(postId, scheduledFor, options = {}) {
    const brandKey = this.template.resolveActiveBrandKey(options.brandKey);
    const post = await this.requirePost(postId, { brandKey });
    const parsedScheduleDate = parseDate(scheduledFor);
    if (!parsedScheduleDate) {
      throw new AppError('Invalid schedule date. Use date and time in the scheduler field.', {
        statusCode: 400,
      });
    }

    const status = String(post.status || '')
      .trim()
      .toLowerCase();
    if (!['approved', 'scheduled'].includes(status)) {
      throw new AppError('Only approved posts can be scheduled.', { statusCode: 400 });
    }

    return this.sheets.updateRow(post.rowIndex, {
      status: 'scheduled',
      scheduled_for: parsedScheduleDate.toISOString(),
      updated_at: new Date().toISOString(),
    });
  }

  async exportPost(postId, options = {}) {
    const brandKey = this.template.resolveActiveBrandKey(options.brandKey);
    const post = await this.requirePost(postId, { brandKey });

    const status = String(post.status || '').trim().toLowerCase();

    if (!['approved', 'exported', 'published'].includes(status)) {
      throw new AppError('Post must be approved before export.', { statusCode: 400 });
    }

    const templateData = await this.template.loadPlatform(post.platform || 'instagram', { brandKey });
    const exportResult = await this.exporter.exportPost({
      post,
      company: templateData.company,
    });

    if (status !== 'published') {
      await this.sheets.updateRow(post.rowIndex, {
        status: 'exported',
        updated_at: new Date().toISOString(),
      });
    }

    return exportResult;
  }

  async publishPost(postId, options = {}) {
    const brandKey = this.template.resolveActiveBrandKey(options.brandKey);
    const post = await this.requirePost(postId, { brandKey });
    const platformKey = post.platform || 'instagram';
    const templateData = await this.template.loadPlatform(platformKey, { brandKey });

    return this.publishExistingPost(post, templateData);
  }

  async requirePost(postId, options = {}) {
    const brandKey = this.template.resolveActiveBrandKey(options.brandKey);
    const post = await this.sheets.findRowById(postId, brandKey);

    if (!post) {
      throw new AppError(`Post "${postId}" was not found.`, { statusCode: 404 });
    }

    return post;
  }

  async generateForExistingPost(post, options) {
    const brandKey = this.template.resolveActiveBrandKey(options.brandKey || post.brand_key);
    const regenerateCopy = options.regenerateCopy;
    const regenerateImage = options.regenerateImage;
    const platformKey = post.platform || 'instagram';
    const templateData = await this.template.loadPlatform(platformKey, { brandKey });
    const now = new Date().toISOString();
    const generatedId =
      post.id ||
      `${slugify(post.topic || 'post')}-${String(Date.now()).slice(-6)}`;
    const patch = {
      brand_key: brandKey,
      id: generatedId,
      platform: platformKey,
      status: 'processing',
      created_at: post.created_at || now,
      updated_at: now,
    };

    await this.sheets.updateRow(post.rowIndex, patch);

    try {
      let workingPost = { ...post, ...patch };

      if (regenerateCopy) {
        const draft = await this.copy.generateDraft({
          topic: post.topic,
          company: templateData.company,
          platformKey,
          platformConfig: templateData.platformConfig,
          knowledgeBundle: templateData.knowledgeBundle,
        });

        workingPost = await this.sheets.updateRow(post.rowIndex, {
          title: draft.title,
          hook: draft.hook,
          caption: draft.caption,
          image_prompt: draft.image_prompt,
          status: 'processing',
          updated_at: new Date().toISOString(),
        });
      }

      if (regenerateImage) {
        const imagePrompt = workingPost.image_prompt || post.image_prompt;

        if (!imagePrompt) {
          throw new AppError('Image prompt is missing, so image regeneration cannot run.', {
            statusCode: 400,
          });
        }

        const imageResult = await this.images.generateImage({
          postId: post.id || post.topic || 'post',
          company: templateData.company,
          platformConfig: templateData.platformConfig,
          imagePrompt,
          knowledgeBundle: templateData.knowledgeBundle,
        });

        workingPost = await this.sheets.updateRow(post.rowIndex, {
          image_path: imageResult.imagePath,
          image_public_url: '',
          instagram_container_id: '',
          instagram_media_id: '',
          instagram_permalink: '',
          publish_error: '',
          status: 'generated',
          scheduled_for: '',
          updated_at: new Date().toISOString(),
        });
      } else {
        workingPost = await this.sheets.updateRow(post.rowIndex, {
          status: 'generated',
          updated_at: new Date().toISOString(),
        });
      }

      if (this.shouldAutoPublish(platformKey)) {
        return this.publishExistingPost(workingPost, templateData);
      }

      return workingPost;
    } catch (error) {
      await this.sheets.updateRow(post.rowIndex, {
        status: 'error',
        review_notes: `Auto error: ${error.message}`,
        updated_at: new Date().toISOString(),
      });

      throw error;
    }
  }

  async publishExistingPost(post, templateData) {
    const platformKey = post.platform || 'instagram';
    const currentStatus = String(post.status || '').trim().toLowerCase();

    if (platformKey !== 'instagram') {
      throw new AppError(`Automatic publishing is not implemented for "${platformKey}" yet.`, {
        statusCode: 400,
      });
    }

    if (currentStatus === 'published' || currentStatus === 'publishing') {
      throw new AppError(`Post "${post.id || `row-${post.rowIndex}`}" is already ${currentStatus}.`, {
        statusCode: 400,
      });
    }

    this.assertPublishablePost(post);

    if (!this.instagram.isConfigured()) {
      throw new AppError('Instagram publishing is not configured.', { statusCode: 500 });
    }

    const prePublishRow = await this.sheets.updateRow(post.rowIndex, {
      status: 'publishing',
      publish_attempted_at: new Date().toISOString(),
      publish_error: '',
      updated_at: new Date().toISOString(),
    });

    try {
      const publishResult = await this.instagram.publishImage({
        post: prePublishRow,
        company: templateData.company,
      });

      return this.sheets.updateRow(post.rowIndex, {
        status: 'published',
        image_public_url: publishResult.imagePublicUrl,
        instagram_container_id: publishResult.containerId,
        instagram_media_id: publishResult.mediaId,
        instagram_permalink: publishResult.permalink,
        publish_error: '',
        published_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      });
    } catch (error) {
      await this.sheets.updateRow(post.rowIndex, {
        status: 'error',
        publish_error: error.message,
        updated_at: new Date().toISOString(),
      });

      throw error;
    }
  }

  shouldAutoPublish(platformKey) {
    return (
      platformKey === 'instagram' &&
      this.instagram.isConfigured() &&
      this.instagram.isAutoPublishEnabled()
    );
  }

  assertPublishablePost(post) {
    if (!post.title || !post.caption || !post.image_path) {
      throw new AppError('Post must have title, caption, and image before approval or publish.', {
        statusCode: 400,
      });
    }
  }
}

function buildPipelineSummary(posts) {
  const summary = {
    total: posts.length,
    byStatus: {},
    scheduledCount: 0,
    publishedCount: 0,
    errorCount: 0,
  };

  for (const post of posts) {
    const status = String(post.status || 'unknown')
      .trim()
      .toLowerCase();
    summary.byStatus[status] = (summary.byStatus[status] || 0) + 1;

    if (status === 'scheduled') {
      summary.scheduledCount += 1;
    }

    if (status === 'published') {
      summary.publishedCount += 1;
    }

    if (status === 'error') {
      summary.errorCount += 1;
    }
  }

  return summary;
}

function buildCalendarData(posts) {
  const now = new Date();
  const year = now.getFullYear();
  const month = now.getMonth();
  const firstDay = new Date(year, month, 1);
  const lastDay = new Date(year, month + 1, 0);
  const firstWeekday = normalizeWeekday(firstDay.getDay());
  const totalDays = lastDay.getDate();

  const byDate = {};
  for (const post of posts) {
    const scheduleDate = parseDate(post.scheduled_for);
    if (!scheduleDate) {
      continue;
    }

    if (scheduleDate.getFullYear() !== year || scheduleDate.getMonth() !== month) {
      continue;
    }

    const dateKey = toLocalDateKey(scheduleDate);
    if (!byDate[dateKey]) {
      byDate[dateKey] = [];
    }

    byDate[dateKey].push({
      id: post.id || `row-${post.rowIndex}`,
      topic: post.topic || post.title || 'Untitled',
      status: post.status || 'scheduled',
      platform: post.platform || 'instagram',
      time: scheduleDate.toISOString(),
    });
  }

  const days = [];
  for (let i = 0; i < firstWeekday; i += 1) {
    days.push({ empty: true });
  }

  for (let day = 1; day <= totalDays; day += 1) {
    const date = new Date(year, month, day);
    const dateKey = toLocalDateKey(date);
    days.push({
      empty: false,
      dateKey,
      dayNumber: day,
      isToday: dateKey === toLocalDateKey(now),
      items: byDate[dateKey] || [],
    });
  }

  return {
    monthLabel: now.toLocaleString('sv-SE', { month: 'long', year: 'numeric' }),
    weekdays: ['Mån', 'Tis', 'Ons', 'Tor', 'Fre', 'Lör', 'Sön'],
    days,
  };
}

function normalizeWeekday(day) {
  if (day === 0) {
    return 6;
  }

  return day - 1;
}

function parseDate(value) {
  if (!value) {
    return null;
  }

  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) {
    return null;
  }

  return parsed;
}

function toLocalDateKey(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

module.exports = { PostWorkflowService };
