const path = require('path');
const { AppError } = require('../lib/app-error');

class InstagramPublisherService {
  constructor({ rootDir }) {
    this.rootDir = rootDir;
  }

  isConfigured() {
    return Boolean(
      process.env.INSTAGRAM_ACCESS_TOKEN &&
        process.env.INSTAGRAM_APP_SCOPED_USER_ID &&
        (process.env.INSTAGRAM_PUBLIC_BASE_URL || process.env.PUBLIC_BASE_URL),
    );
  }

  isAutoPublishEnabled() {
    return toBoolean(process.env.INSTAGRAM_AUTO_PUBLISH);
  }

  getAccessToken() {
    const accessToken = process.env.INSTAGRAM_ACCESS_TOKEN;

    if (!accessToken) {
      throw new AppError('INSTAGRAM_ACCESS_TOKEN is missing.', { statusCode: 500 });
    }

    return accessToken;
  }

  getUserId() {
    const userId = process.env.INSTAGRAM_APP_SCOPED_USER_ID;

    if (!userId) {
      throw new AppError('INSTAGRAM_APP_SCOPED_USER_ID is missing.', { statusCode: 500 });
    }

    return userId;
  }

  getApiVersion() {
    return process.env.INSTAGRAM_GRAPH_API_VERSION || 'v25.0';
  }

  getGraphBaseUrl() {
    return (process.env.INSTAGRAM_GRAPH_BASE_URL || 'https://graph.instagram.com').replace(
      /\/+$/,
      '',
    );
  }

  getPublicBaseUrl() {
    const baseUrl = process.env.INSTAGRAM_PUBLIC_BASE_URL || process.env.PUBLIC_BASE_URL;

    if (!baseUrl) {
      throw new AppError(
        'PUBLIC_BASE_URL or INSTAGRAM_PUBLIC_BASE_URL is required for Instagram publishing.',
        { statusCode: 500 },
      );
    }

    if (!/^https?:\/\//i.test(baseUrl)) {
      throw new AppError(
        'PUBLIC_BASE_URL must start with http:// or https:// and be publicly reachable by Meta.',
        {
          statusCode: 500,
        },
      );
    }

    return baseUrl.replace(/\/+$/, '');
  }

  async publishImage({ post, company }) {
    if (!this.isConfigured()) {
      throw new AppError('Instagram publishing is not configured.', { statusCode: 500 });
    }

    if (!post.caption) {
      throw new AppError('Caption is required before publishing to Instagram.', {
        statusCode: 400,
      });
    }

    if (!post.image_path) {
      throw new AppError('Image path is required before publishing to Instagram.', {
        statusCode: 400,
      });
    }

    const imagePublicUrl = post.image_public_url || this.resolvePublicImageUrl(post.image_path);
    const altText = buildAltText({ post, company });
    const container = await this.createImageContainer({
      caption: post.caption,
      imagePublicUrl,
      altText,
    });

    const containerId = container.id;

    if (!containerId) {
      throw new AppError('Instagram did not return a media container id.', { statusCode: 502 });
    }

    const containerStatus = await this.waitUntilContainerReady(containerId);
    const published = await this.publishContainer(containerId);
    const mediaId = published.id;
    const media = mediaId ? await this.getPublishedMedia(mediaId) : null;

    return {
      imagePublicUrl,
      containerId,
      containerStatus: containerStatus.status_code || '',
      mediaId: mediaId || '',
      permalink: media?.permalink || '',
      mediaProductType: media?.media_product_type || '',
      mediaType: media?.media_type || '',
    };
  }

  resolvePublicImageUrl(imagePath) {
    if (/^https?:\/\//i.test(imagePath)) {
      return imagePath;
    }

    const normalizedPath = String(imagePath || '')
      .replace(/\\/g, '/')
      .replace(/^\/+/, '');

    if (!normalizedPath) {
      throw new AppError('image_path is empty and cannot be published.', { statusCode: 400 });
    }

    const absolutePath = path.resolve(this.rootDir, normalizedPath);

    return `${this.getPublicBaseUrl()}/${path.relative(this.rootDir, absolutePath).replace(/\\/g, '/')}`;
  }

  async createImageContainer({ caption, imagePublicUrl, altText }) {
    return this.requestJson(`/${this.getUserId()}/media`, {
      method: 'POST',
      body: {
        image_url: imagePublicUrl,
        caption,
        alt_text: altText,
      },
    });
  }

  async waitUntilContainerReady(containerId) {
    const maxAttempts = Number(process.env.INSTAGRAM_CONTAINER_POLL_ATTEMPTS || 12);
    const pollMs = Number(process.env.INSTAGRAM_CONTAINER_POLL_MS || 5000);
    let latest = null;

    for (let attempt = 0; attempt < maxAttempts; attempt += 1) {
      latest = await this.requestJson(`/${containerId}`, {
        query: { fields: 'id,status,status_code' },
      });

      const statusCode = String(latest.status_code || '').toUpperCase();

      if (!statusCode || statusCode === 'FINISHED' || statusCode === 'PUBLISHED') {
        return latest;
      }

      if (statusCode === 'ERROR' || statusCode === 'EXPIRED') {
        throw new AppError(
          `Instagram container ${containerId} is not publishable. Status: ${statusCode}.`,
          {
            statusCode: 502,
            details: latest,
          },
        );
      }

      await delay(pollMs);
    }

    throw new AppError(
      `Instagram container ${containerId} did not become publishable in time.`,
      {
        statusCode: 504,
        details: latest,
      },
    );
  }

  async publishContainer(containerId) {
    return this.requestJson(`/${this.getUserId()}/media_publish`, {
      method: 'POST',
      body: { creation_id: containerId },
    });
  }

  async getPublishedMedia(mediaId) {
    return this.requestJson(`/${mediaId}`, {
      query: { fields: 'id,permalink,media_product_type,media_type,timestamp' },
    });
  }

  async requestJson(endpointPath, options = {}) {
    const url = new URL(
      `${this.getGraphBaseUrl()}/${this.getApiVersion()}${normalizeEndpointPath(endpointPath)}`,
    );

    if (options.query) {
      for (const [key, value] of Object.entries(options.query)) {
        if (value == null || value === '') {
          continue;
        }

        url.searchParams.set(key, String(value));
      }
    }

    const response = await fetch(url, {
      method: options.method || 'GET',
      headers: {
        Accept: 'application/json',
        Authorization: `Bearer ${this.getAccessToken()}`,
        ...(options.body ? { 'Content-Type': 'application/json' } : {}),
      },
      body: options.body ? JSON.stringify(options.body) : undefined,
    });

    const responseText = await response.text();
    const payload = responseText ? safeJsonParse(responseText) : {};

    if (!response.ok) {
      throw new AppError(
        `Instagram request failed (${response.status} ${response.statusText}): ${responseText}`,
        {
          statusCode: 502,
          details: payload,
        },
      );
    }

    return payload;
  }
}

function buildAltText({ post, company }) {
  const parts = [
    post.title || post.topic || '',
    post.hook || '',
    company?.name || '',
  ]
    .map((value) => String(value || '').trim())
    .filter(Boolean);

  return parts.join(' - ').slice(0, 1000);
}

function normalizeEndpointPath(value) {
  return value.startsWith('/') ? value : `/${value}`;
}

function safeJsonParse(value) {
  try {
    return JSON.parse(value);
  } catch (error) {
    return { raw: value };
  }
}

function toBoolean(value) {
  return ['1', 'true', 'yes', 'on'].includes(String(value || '').trim().toLowerCase());
}

function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

module.exports = { InstagramPublisherService };
