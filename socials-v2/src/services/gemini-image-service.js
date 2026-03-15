const fs = require('fs/promises');
const path = require('path');
const { AppError } = require('../lib/app-error');
const { ensureDir, toProjectRelative } = require('../lib/filesystem');
const { slugify } = require('../lib/string-utils');

class GeminiImageService {
  constructor({ rootDir }) {
    this.rootDir = rootDir;
  }

  isConfigured() {
    return Boolean(process.env.GEMINI_API_KEY);
  }

  getModel() {
    return process.env.GEMINI_IMAGE_MODEL || 'gemini-2.5-flash-image';
  }

  async generateImage({
    postId,
    company,
    platformConfig,
    imagePrompt,
    knowledgeBundle,
  }) {
    if (!this.isConfigured()) {
      throw new AppError('GEMINI_API_KEY is missing.', { statusCode: 500 });
    }

    const aspectRatio = platformConfig.default_aspect_ratio || '4:5';
    const finalPrompt = buildPrompt({
      company,
      imagePrompt,
      knowledgeBundle,
      aspectRatio,
    });

    const response = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/${this.getModel()}:generateContent`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-goog-api-key': process.env.GEMINI_API_KEY,
        },
        body: JSON.stringify({
          contents: [
            {
              parts: [{ text: finalPrompt }],
            },
          ],
          generationConfig: {
            responseModalities: ['TEXT', 'IMAGE'],
            imageConfig: {
              aspectRatio,
            },
          },
        }),
      },
    );

    if (!response.ok) {
      const errorText = await response.text();
      throw new AppError(`Gemini image generation failed: ${errorText}`, {
        statusCode: 502,
      });
    }

    const payload = await response.json();
    const parts = payload.candidates
      ?.flatMap((candidate) => candidate.content?.parts || [])
      .filter(Boolean) || [];

    const inlineDataPart = parts.find((part) => (part.inlineData || part.inline_data)?.data);
    const modelText = parts
      .map((part) => part.text)
      .filter(Boolean)
      .join('\n')
      .trim();

    if (!inlineDataPart) {
      throw new AppError(
        `Gemini did not return an image.${modelText ? ` Response text: ${modelText}` : ''}`,
        {
          statusCode: 502,
          details: payload,
        },
      );
    }

    const inlineData = inlineDataPart.inlineData || inlineDataPart.inline_data;
    const mimeType = inlineData.mimeType || inlineData.mime_type || 'image/png';
    const extension = mimeTypeToExtension(mimeType);
    const outputDir = path.join(this.rootDir, 'output', 'images');
    const fileName = `${slugify(postId)}-${Date.now()}${extension}`;
    const absolutePath = path.join(outputDir, fileName);
    const buffer = Buffer.from(inlineData.data, 'base64');

    await ensureDir(outputDir);
    await fs.writeFile(absolutePath, buffer);

    return {
      absolutePath,
      imagePath: toProjectRelative(this.rootDir, absolutePath),
      mimeType,
      providerText: modelText,
      finalPrompt,
    };
  }
}

function buildPrompt({ company, imagePrompt, knowledgeBundle, aspectRatio }) {
  return `
Create a branded social media image for ${company.name || 'the company'}.

Creative brief:
${imagePrompt}

Constraints:
- Target aspect ratio: ${aspectRatio}
- No text overlay
- No logo
- No watermark
- Image should feel specific to the company, not generic stock imagery

Company context:
${JSON.stringify(company, null, 2)}

Knowledge bank:
${knowledgeBundle.slice(0, 12000)}
`.trim();
}

function mimeTypeToExtension(mimeType) {
  if (mimeType.includes('jpeg')) {
    return '.jpg';
  }

  if (mimeType.includes('webp')) {
    return '.webp';
  }

  return '.png';
}

module.exports = { GeminiImageService };

