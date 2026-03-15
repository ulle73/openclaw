const path = require('path');
const { TemplateService } = require('./services/template-service');
const { GoogleSheetsService } = require('./services/google-sheets-service');
const { OpenAICopyService } = require('./services/openai-copy-service');
const { GeminiImageService } = require('./services/gemini-image-service');
const { InstagramPublisherService } = require('./services/instagram-publisher-service');
const { ExportService } = require('./services/export-service');
const { PostWorkflowService } = require('./services/post-workflow-service');
const { QueueWorkerService } = require('./services/queue-worker-service');

function createRuntime({ rootDir }) {
  const resolvedRootDir = path.resolve(rootDir);
  const template = new TemplateService({ rootDir: resolvedRootDir });
  const sheets = new GoogleSheetsService({ rootDir: resolvedRootDir });
  const copy = new OpenAICopyService({ rootDir: resolvedRootDir });
  const images = new GeminiImageService({ rootDir: resolvedRootDir });
  const instagram = new InstagramPublisherService({ rootDir: resolvedRootDir });
  const exporter = new ExportService({ rootDir: resolvedRootDir });

  const workflow = new PostWorkflowService({
    rootDir: resolvedRootDir,
    template,
    sheets,
    copy,
    images,
    instagram,
    exporter,
  });
  const queueWorker = new QueueWorkerService({ workflow });

  return {
    rootDir: resolvedRootDir,
    template,
    sheets,
    copy,
    images,
    instagram,
    exporter,
    workflow,
    queueWorker,
    getPort() {
      return Number(process.env.PORT || 3000);
    },
  };
}

module.exports = { createRuntime };
