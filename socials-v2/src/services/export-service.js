const fs = require('fs/promises');
const path = require('path');
const { AppError } = require('../lib/app-error');
const { ensureDir, toProjectRelative, writeJson, writeText } = require('../lib/filesystem');
const { slugify } = require('../lib/string-utils');

class ExportService {
  constructor({ rootDir }) {
    this.rootDir = rootDir;
  }

  async exportPost({ post, company }) {
    if (!post.image_path) {
      throw new AppError('Cannot export a post without an image.', { statusCode: 400 });
    }

    const exportDir = path.join(
      this.rootDir,
      'output',
      'exports',
      `${slugify(post.id || post.topic)}-${Date.now()}`,
    );

    await ensureDir(exportDir);

    const sourceImagePath = path.resolve(this.rootDir, post.image_path);
    const destinationImagePath = path.join(exportDir, path.basename(sourceImagePath));

    await fs.copyFile(sourceImagePath, destinationImagePath);

    await Promise.all([
      writeText(path.join(exportDir, 'title.txt'), post.title || ''),
      writeText(path.join(exportDir, 'hook.txt'), post.hook || ''),
      writeText(path.join(exportDir, 'caption.txt'), post.caption || ''),
      writeText(path.join(exportDir, 'image_prompt.txt'), post.image_prompt || ''),
      writeJson(path.join(exportDir, 'post.json'), {
        exportedAt: new Date().toISOString(),
        company: {
          name: company.name || '',
          website: company.website || '',
          industry: company.industry || '',
        },
        post: {
          id: post.id || '',
          topic: post.topic || '',
          platform: post.platform || '',
          status: post.status || '',
          title: post.title || '',
          hook: post.hook || '',
          caption: post.caption || '',
          image_prompt: post.image_prompt || '',
          image_path: toProjectRelative(this.rootDir, destinationImagePath),
          review_notes: post.review_notes || '',
          approved_at: post.approved_at || '',
          created_at: post.created_at || '',
          updated_at: post.updated_at || '',
        },
      }),
    ]);

    return {
      absolutePath: exportDir,
      exportPath: toProjectRelative(this.rootDir, exportDir),
    };
  }
}

module.exports = { ExportService };

