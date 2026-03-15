const OpenAI = require('openai');
const { AppError } = require('../lib/app-error');

class OpenAICopyService {
  constructor() {
    this.client = null;
  }

  isConfigured() {
    return Boolean(process.env.OPENAI_API_KEY);
  }

  getClient() {
    if (!this.isConfigured()) {
      throw new AppError('OPENAI_API_KEY is missing.', { statusCode: 500 });
    }

    if (!this.client) {
      this.client = new OpenAI({
        apiKey: process.env.OPENAI_API_KEY,
      });
    }

    return this.client;
  }

  getModel() {
    return process.env.OPENAI_MODEL || 'gpt-4o-mini';
  }

  async generateDraft({ topic, company, platformKey, platformConfig, knowledgeBundle }) {
    const client = this.getClient();
    const maxCaptionLength = platformConfig.max_caption_length || 2200;
    const hashtagCount = platformConfig.hashtag_count || 0;
    const language = platformConfig.language || 'sv';

    const response = await client.chat.completions.create({
      model: this.getModel(),
      temperature: 0.8,
      response_format: { type: 'json_object' },
      messages: [
        {
          role: 'system',
          content: [
            'You are a senior social media strategist and copywriter.',
            'Return valid JSON only.',
            'Do not include markdown fences.',
            'Respect the provided company context, offer, audience, tone, CTA direction, and no-go rules.',
            'Do not invent facts or claims that are not supported by the provided context.',
            'Output keys must be exactly: title, hook, caption, image_prompt.',
          ].join(' '),
        },
        {
          role: 'user',
          content: `
Create an ${platformKey} post draft in language "${language}".

Topic:
${topic}

Platform rules:
- Max caption length: ${maxCaptionLength}
- Default aspect ratio: ${platformConfig.default_aspect_ratio || '4:5'}
- Include up to ${hashtagCount} relevant hashtags at the end of the caption if it improves the result.

Company profile:
${JSON.stringify(company, null, 2)}

Knowledge bank:
${knowledgeBundle.slice(0, 16000)}

Return JSON with:
- title: short post title
- hook: strong first-line opener
- caption: full Instagram-ready caption
- image_prompt: a specific visual prompt for the image model
`.trim(),
        },
      ],
    });

    const content = response.choices?.[0]?.message?.content;

    if (!content) {
      throw new AppError('OpenAI did not return copy content.', { statusCode: 502 });
    }

    let parsed;

    try {
      parsed = JSON.parse(content);
    } catch (error) {
      throw new AppError('OpenAI returned invalid JSON.', {
        statusCode: 502,
        cause: error,
        details: content,
      });
    }

    return sanitizeDraft(parsed, maxCaptionLength);
  }
}

function sanitizeDraft(rawDraft, maxCaptionLength) {
  const draft = {
    title: String(rawDraft.title || '').trim(),
    hook: String(rawDraft.hook || '').trim(),
    caption: String(rawDraft.caption || '').trim(),
    image_prompt: String(rawDraft.image_prompt || '').trim(),
  };

  for (const [key, value] of Object.entries(draft)) {
    if (!value) {
      throw new AppError(`OpenAI draft is missing "${key}".`, { statusCode: 502 });
    }
  }

  if (draft.caption.length > maxCaptionLength) {
    draft.caption = draft.caption.slice(0, maxCaptionLength).trim();
  }

  return draft;
}

module.exports = { OpenAICopyService };

