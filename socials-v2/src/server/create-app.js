const express = require('express');
const path = require('path');
const { renderHomePage } = require('./render-home-page');

function createApp({ runtime }) {
  const app = express();

  app.use(express.urlencoded({ extended: true }));
  app.use('/public', express.static(path.join(runtime.rootDir, 'public')));
  app.use('/output', express.static(path.join(runtime.rootDir, 'output')));

  app.get('/', async (req, res, next) => {
    try {
      const brandKey = resolveBrand(req);
      const data = await runtime.workflow.getDashboardData({ brandKey });
      res.type('html').send(
        renderHomePage({
          ...data,
          flash: {
            message: req.query.message || '',
            error: req.query.error || '',
          },
        }),
      );
    } catch (error) {
      next(error);
    }
  });

  app.get('/health', async (req, res, next) => {
    try {
      const brandKey = resolveBrand(req);
      const data = await runtime.workflow.getDashboardData({ brandKey });
      res.json({
        ok: !data.diagnostics.sheetError,
        brand: data.template.brand,
        integrations: data.diagnostics.integrations,
        company: data.template.company.name || null,
        activePlatforms: data.template.activePlatforms,
      });
    } catch (error) {
      next(error);
    }
  });

  app.get('/api/posts', async (req, res, next) => {
    try {
      const brandKey = resolveBrand(req);
      const posts = await runtime.workflow.listPosts({ brandKey });
      res.json(posts);
    } catch (error) {
      next(error);
    }
  });

  app.post('/actions/bootstrap-sheet', async (req, res) => {
    const brandKey = resolveBrand(req);
    try {
      const headers = await runtime.workflow.bootstrapSheet();
      res.redirect(withFlash(`Sheet is ready with ${headers.length} headers.`, '', brandKey));
    } catch (error) {
      res.redirect(withFlash('', error.message, brandKey));
    }
  });

  app.post('/actions/process-next', async (req, res) => {
    const brandKey = resolveBrand(req);
    try {
      const result = await runtime.workflow.processNext({ brandKey });

      if (!result) {
        res.redirect(withFlash('No post with status "new" was found.', '', brandKey));
        return;
      }

      res.redirect(withFlash(`Processed ${result.id || result.topic}.`, '', brandKey));
    } catch (error) {
      res.redirect(withFlash('', error.message, brandKey));
    }
  });

  app.post('/posts/:id/review-notes', async (req, res) => {
    const brandKey = resolveBrand(req);
    try {
      await runtime.workflow.saveReviewNotes(req.params.id, req.body.review_notes || '', { brandKey });
      res.redirect(withFlash(`Saved notes for ${req.params.id}.`, '', brandKey));
    } catch (error) {
      res.redirect(withFlash('', error.message, brandKey));
    }
  });

  app.post('/posts/:id/regenerate-copy', async (req, res) => {
    const brandKey = resolveBrand(req);
    try {
      await runtime.workflow.regenerateCopy(req.params.id, { brandKey });
      res.redirect(withFlash(`Regenerated copy for ${req.params.id}.`, '', brandKey));
    } catch (error) {
      res.redirect(withFlash('', error.message, brandKey));
    }
  });

  app.post('/posts/:id/regenerate-image', async (req, res) => {
    const brandKey = resolveBrand(req);
    try {
      await runtime.workflow.regenerateImage(req.params.id, { brandKey });
      res.redirect(withFlash(`Regenerated image for ${req.params.id}.`, '', brandKey));
    } catch (error) {
      res.redirect(withFlash('', error.message, brandKey));
    }
  });

  app.post('/posts/:id/approve', async (req, res) => {
    const brandKey = resolveBrand(req);
    try {
      await runtime.workflow.approvePost(req.params.id, req.body.review_notes || undefined, { brandKey });
      res.redirect(withFlash(`Approved ${req.params.id}.`, '', brandKey));
    } catch (error) {
      res.redirect(withFlash('', error.message, brandKey));
    }
  });

  app.post('/posts/:id/schedule', async (req, res) => {
    const brandKey = resolveBrand(req);
    try {
      await runtime.workflow.schedulePost(req.params.id, req.body.scheduled_for, { brandKey });
      res.redirect(withFlash(`Scheduled ${req.params.id}.`, '', brandKey));
    } catch (error) {
      res.redirect(withFlash('', error.message, brandKey));
    }
  });

  app.post('/posts/:id/publish', async (req, res) => {
    const brandKey = resolveBrand(req);
    try {
      await runtime.workflow.publishPost(req.params.id, { brandKey });
      res.redirect(withFlash(`Published ${req.params.id} to Instagram.`, '', brandKey));
    } catch (error) {
      res.redirect(withFlash('', error.message, brandKey));
    }
  });

  app.post('/posts/:id/export', async (req, res) => {
    const brandKey = resolveBrand(req);
    try {
      const exportResult = await runtime.workflow.exportPost(req.params.id, { brandKey });
      res.redirect(withFlash(`Exported ${req.params.id} to ${exportResult.exportPath}.`, '', brandKey));
    } catch (error) {
      res.redirect(withFlash('', error.message, brandKey));
    }
  });

  app.use((error, req, res, next) => {
    if (res.headersSent) {
      next(error);
      return;
    }

    res.status(error.statusCode || 500).type('html').send(`
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Social Media Manager Error</title>
    <link rel="stylesheet" href="/public/styles.css" />
  </head>
  <body class="error-page">
    <main class="error-shell">
      <h1>Application error</h1>
      <p>${escapeForHtml(error.message || 'Unknown error')}</p>
      <a class="button-link" href="/">Back to dashboard</a>
    </main>
  </body>
</html>
`);
  });

  return app;
}

function withFlash(message, error, brandKey) {
  const params = new URLSearchParams();

  if (message) {
    params.set('message', message);
  }

  if (error) {
    params.set('error', error);
  }

  if (brandKey) {
    params.set('brand', brandKey);
  }

  const query = params.toString();
  return query ? `/?${query}` : '/';
}

function resolveBrand(req) {
  return String(req.body?.brand || req.query?.brand || '').trim() || undefined;
}

function escapeForHtml(value) {
  return String(value || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

module.exports = { createApp };
