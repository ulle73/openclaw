const { escapeHtml, formatDate, truncate } = require('../lib/string-utils');

function renderHomePage({ template, diagnostics, posts, flash, pipelineSummary, calendar }) {
  const companyName = template.company.name || 'Unnamed company';
  const activePlatforms = template.activePlatforms.length
    ? template.activePlatforms.join(', ')
    : 'None';
  const activeBrandKey = template.brand?.key || 'default';
  const activeBrandName = template.brand?.name || activeBrandKey;
  const availableBrands = template.availableBrands || [];
  const knowledgeCards = template.knowledgeDocs.length
    ? template.knowledgeDocs
        .map(
          (doc) => `
            <article class="knowledge-card">
              <div class="knowledge-meta">${escapeHtml(doc.category)}</div>
              <h3>${escapeHtml(doc.fileName)}</h3>
              <p>${escapeHtml(doc.preview)}</p>
              <div class="knowledge-path">${escapeHtml(doc.relativePath)}</div>
            </article>
          `,
        )
        .join('')
    : '<p class="empty-state">No knowledge files found.</p>';

  const postCards = posts.length
    ? posts.map((post) => renderPostCard(post, activeBrandKey)).join('')
    : `
      <div class="empty-state large">
        <h3>No posts loaded yet</h3>
        <p>Set up your Google Sheet and click "Process Next Post" when you have rows with status <code>new</code>.</p>
      </div>
    `;

  const pipelineCards = renderPipelineCards(pipelineSummary || {});
  const calendarGrid = renderCalendar(calendar);
  const brandDescription = template.brand?.description
    ? `<p class="brand-description">${escapeHtml(template.brand.description)}</p>`
    : '';

  return `
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Social Media Manager</title>
    <link rel="stylesheet" href="/public/styles.css" />
  </head>
  <body>
    <main class="shell">
      <section class="hero panel">
        <div>
          <div class="eyebrow">Template dashboard</div>
          <h1>Socials V2 Control Room</h1>
          <p class="lede">
            White-label content workflow with brand profiles, knowledge bank, pipeline tracking, and planner-ready calendar.
          </p>
        </div>
        <div class="hero-badges">
          <div class="badge">
            <span class="badge-label">Brand</span>
            <strong>${escapeHtml(activeBrandName)}</strong>
          </div>
          <div class="badge">
            <span class="badge-label">Company</span>
            <strong>${escapeHtml(companyName)}</strong>
          </div>
          <div class="badge">
            <span class="badge-label">Active platform</span>
            <strong>${escapeHtml(activePlatforms)}</strong>
          </div>
          <div class="badge">
            <span class="badge-label">Knowledge docs</span>
            <strong>${template.knowledgeDocs.length}</strong>
          </div>
        </div>
      </section>

      ${renderFlash(flash)}

      <section class="grid">
        <section class="panel">
          <div class="section-head">
            <h2>Brand Switch</h2>
            <p>Switch instantly between brand profiles without touching core code.</p>
          </div>
          <form method="get" action="/" class="brand-switch-form">
            <label for="brand-select">Active brand</label>
            <div class="inline-form-row">
              <select id="brand-select" name="brand">
                ${availableBrands
                  .map(
                    (brand) => `
                      <option value="${escapeHtml(brand.key)}" ${
                      brand.key === activeBrandKey ? 'selected' : ''
                    }>
                        ${escapeHtml(brand.name || brand.key)}
                      </option>
                    `,
                  )
                  .join('')}
              </select>
              <button type="submit" class="primary">Load Brand</button>
            </div>
          </form>
          ${brandDescription}
        </section>

        <section class="panel">
          <div class="section-head">
            <h2>Actions</h2>
            <p>Run queue actions for the currently selected brand.</p>
          </div>
          <div class="button-row">
            <form method="post" action="/actions/bootstrap-sheet">
              <input type="hidden" name="brand" value="${escapeHtml(activeBrandKey)}" />
              <button type="submit">Bootstrap Sheet</button>
            </form>
            <form method="post" action="/actions/process-next">
              <input type="hidden" name="brand" value="${escapeHtml(activeBrandKey)}" />
              <button type="submit" class="primary">Process Next Post</button>
            </form>
          </div>
        </section>
      </section>

      <section class="grid">
        <section class="panel">
          <div class="section-head">
            <h2>Pipeline Overview</h2>
            <p>Status distribution for this brand in the current sheet.</p>
          </div>
          <div class="pipeline-grid">
            ${pipelineCards}
          </div>
        </section>

        <section class="panel">
          <div class="section-head">
            <h2>Integration Status</h2>
            <p>Configuration and dependencies for the active flow.</p>
          </div>
          <dl class="status-list">
            <div>
              <dt>Brand config files</dt>
              <dd>${renderStatus(
                diagnostics.template.companyConfigExists && diagnostics.template.platformsConfigExists,
              )}</dd>
            </div>
            <div>
              <dt>Knowledge bank</dt>
              <dd>${renderStatus(diagnostics.template.knowledgeExists)}</dd>
            </div>
            <div>
              <dt>Google Sheets</dt>
              <dd>${renderStatus(diagnostics.integrations.sheetsConfigured)}</dd>
            </div>
            <div>
              <dt>OpenAI</dt>
              <dd>${renderStatus(diagnostics.integrations.openAiConfigured)}</dd>
            </div>
            <div>
              <dt>Gemini</dt>
              <dd>${renderStatus(diagnostics.integrations.geminiConfigured)}</dd>
            </div>
            <div>
              <dt>Instagram Publish</dt>
              <dd>${renderStatus(diagnostics.integrations.instagramConfigured)}</dd>
            </div>
            <div>
              <dt>Auto Publish</dt>
              <dd>${renderStatus(diagnostics.integrations.instagramAutoPublishEnabled)}</dd>
            </div>
          </dl>
          ${
            diagnostics.sheetError
              ? `<p class="inline-error">${escapeHtml(diagnostics.sheetError)}</p>`
              : ''
          }
        </section>
      </section>

      <section class="panel">
        <div class="section-head">
          <h2>Content Calendar</h2>
          <p>Planner base for scheduled posts. Queue worker can auto-publish due scheduled content.</p>
        </div>
        <div class="calendar-wrap">
          <h3 class="calendar-title">${escapeHtml(calendar?.monthLabel || '')}</h3>
          ${calendarGrid}
        </div>
      </section>

      <section class="panel">
        <div class="section-head">
          <h2>Template Editable Surface</h2>
          <p>These are the files each new client edits instead of touching core code.</p>
        </div>
        <ul class="editable-list">
          ${diagnostics.template.editablePaths
            .map((item) => `<li><code>${escapeHtml(item)}</code></li>`)
            .join('')}
        </ul>
      </section>

      <section class="panel">
        <div class="section-head">
          <h2>Knowledge Bank</h2>
          <p>The content engine uses these files as business context for copy and images.</p>
        </div>
        <div class="knowledge-grid">
          ${knowledgeCards}
        </div>
      </section>

      <section class="panel">
        <div class="section-head">
          <h2>Posts</h2>
          <p>Rows from Google Sheets filtered by active brand.</p>
        </div>
        <div class="posts-grid">
          ${postCards}
        </div>
      </section>
    </main>
  </body>
</html>
`;
}

function renderFlash(flash) {
  if (!flash?.message && !flash?.error) {
    return '';
  }

  return `
    <section class="flash-stack">
      ${flash.message ? `<div class="flash success">${escapeHtml(flash.message)}</div>` : ''}
      ${flash.error ? `<div class="flash error">${escapeHtml(flash.error)}</div>` : ''}
    </section>
  `;
}

function renderStatus(isReady) {
  return `<span class="status-pill ${isReady ? 'ready' : 'missing'}">${
    isReady ? 'Ready' : 'Missing'
  }</span>`;
}

function renderPipelineCards(summary) {
  const byStatus = summary.byStatus || {};
  const statuses = [
    'new',
    'processing',
    'generated',
    'approved',
    'scheduled',
    'publishing',
    'published',
    'error',
  ];

  return statuses
    .map((statusKey) => {
      const value = byStatus[statusKey] || 0;
      return `
        <article class="pipeline-card">
          <div class="pipeline-label">${escapeHtml(statusKey)}</div>
          <strong>${value}</strong>
        </article>
      `;
    })
    .join('');
}

function renderCalendar(calendar) {
  if (!calendar) {
    return '<p class="empty-state">No calendar data.</p>';
  }

  const weekdays = (calendar.weekdays || [])
    .map((weekday) => `<div class="calendar-weekday">${escapeHtml(weekday)}</div>`)
    .join('');

  const dayCells = (calendar.days || [])
    .map((day) => {
      if (day.empty) {
        return '<div class="calendar-day empty"></div>';
      }

      const items = (day.items || [])
        .slice(0, 3)
        .map(
          (item) => `
            <div class="calendar-item status-${escapeHtml(String(item.status || '').toLowerCase())}">
              <span>${escapeHtml(item.topic)}</span>
            </div>
          `,
        )
        .join('');

      const overflowCount = (day.items || []).length > 3 ? (day.items || []).length - 3 : 0;
      const overflow = overflowCount
        ? `<div class="calendar-item overflow">+${overflowCount} more</div>`
        : '';

      return `
        <div class="calendar-day ${day.isToday ? 'today' : ''}">
          <div class="calendar-day-head">${day.dayNumber}</div>
          <div class="calendar-day-items">
            ${items || '<div class="calendar-item empty-note">No posts</div>'}
            ${overflow}
          </div>
        </div>
      `;
    })
    .join('');

  return `
    <div class="calendar-grid">
      ${weekdays}
      ${dayCells}
    </div>
  `;
}

function renderPostCard(post, activeBrandKey) {
  const imageUrl = normalizeOutputUrl(post.image_path);
  const actionId = encodeURIComponent(post.id || `row-${post.rowIndex}`);
  const notesFieldId = `review-notes-${escapeHtml(post.id || `row-${post.rowIndex}`)}`;
  const scheduledInputId = `scheduled-for-${escapeHtml(post.id || `row-${post.rowIndex}`)}`;
  const scheduledValue = toDateTimeLocalValue(post.scheduled_for);

  return `
    <article class="post-card">
      <div class="post-head">
        <div>
          <div class="post-id">${escapeHtml(post.id || 'Untitled')}</div>
          <h3>${escapeHtml(post.topic || post.title || 'Untitled topic')}</h3>
        </div>
        <span class="status-pill ${escapeHtml((post.status || 'unknown').toLowerCase())}">
          ${escapeHtml(post.status || 'unknown')}
        </span>
      </div>

      <dl class="post-meta">
        <div><dt>Platform</dt><dd>${escapeHtml(post.platform || 'instagram')}</dd></div>
        <div><dt>Updated</dt><dd>${escapeHtml(formatDate(post.updated_at || post.created_at))}</dd></div>
        <div><dt>Scheduled</dt><dd>${escapeHtml(formatDate(post.scheduled_for || ''))}</dd></div>
      </dl>

      ${
        post.instagram_permalink
          ? `<p class="post-permalink"><a href="${escapeHtml(
              post.instagram_permalink,
            )}" target="_blank" rel="noreferrer">Open published Instagram post</a></p>`
          : ''
      }

      ${
        imageUrl
          ? `<div class="post-image-wrap"><img src="${escapeHtml(imageUrl)}" alt="${escapeHtml(
              post.title || post.topic || 'Generated image',
            )}" class="post-image" /></div>`
          : '<div class="post-image-placeholder">No generated image yet</div>'
      }

      <div class="post-copy">
        <div>
          <h4>Title</h4>
          <p>${escapeHtml(post.title || 'N/A')}</p>
        </div>
        <div>
          <h4>Hook</h4>
          <p>${escapeHtml(post.hook || 'N/A')}</p>
        </div>
        <div>
          <h4>Caption</h4>
          <pre>${escapeHtml(post.caption || 'N/A')}</pre>
        </div>
        <div>
          <h4>Image Prompt</h4>
          <pre>${escapeHtml(truncate(post.image_prompt || 'N/A', 800))}</pre>
        </div>
        <div>
          <h4>Publish</h4>
          <p>Media ID: ${escapeHtml(post.instagram_media_id || 'N/A')}</p>
          <p>Permalink: ${escapeHtml(post.instagram_permalink || 'N/A')}</p>
          <p>Error: ${escapeHtml(truncate(post.publish_error || 'N/A', 400))}</p>
        </div>
      </div>

      <form method="post" action="/posts/${actionId}/review-notes" class="notes-form">
        <input type="hidden" name="brand" value="${escapeHtml(activeBrandKey)}" />
        <label for="${notesFieldId}">Review notes</label>
        <textarea id="${notesFieldId}" name="review_notes">${escapeHtml(
          post.review_notes || '',
        )}</textarea>
        <button type="submit">Save Notes</button>
      </form>

      <form method="post" action="/posts/${actionId}/schedule" class="schedule-form">
        <input type="hidden" name="brand" value="${escapeHtml(activeBrandKey)}" />
        <label for="${scheduledInputId}">Schedule for</label>
        <div class="inline-form-row">
          <input id="${scheduledInputId}" type="datetime-local" name="scheduled_for" value="${escapeHtml(
            scheduledValue,
          )}" />
          <button type="submit">Save Schedule</button>
        </div>
      </form>

      <div class="button-row dense">
        <form method="post" action="/posts/${actionId}/regenerate-copy">
          <input type="hidden" name="brand" value="${escapeHtml(activeBrandKey)}" />
          <button type="submit">Regenerate Copy</button>
        </form>
        <form method="post" action="/posts/${actionId}/regenerate-image">
          <input type="hidden" name="brand" value="${escapeHtml(activeBrandKey)}" />
          <button type="submit">Regenerate Image</button>
        </form>
        <form method="post" action="/posts/${actionId}/approve">
          <input type="hidden" name="brand" value="${escapeHtml(activeBrandKey)}" />
          <input type="hidden" name="review_notes" value="${escapeHtml(post.review_notes || '')}" />
          <button type="submit" class="primary">Approve</button>
        </form>
        <form method="post" action="/posts/${actionId}/publish">
          <input type="hidden" name="brand" value="${escapeHtml(activeBrandKey)}" />
          <button type="submit" class="primary">Publish Now</button>
        </form>
        <form method="post" action="/posts/${actionId}/export">
          <input type="hidden" name="brand" value="${escapeHtml(activeBrandKey)}" />
          <button type="submit">Export Package</button>
        </form>
      </div>
    </article>
  `;
}

function normalizeOutputUrl(imagePath) {
  if (!imagePath) {
    return '';
  }

  const normalizedPath = String(imagePath).replace(/\\/g, '/');
  if (normalizedPath.startsWith('output/')) {
    return `/${normalizedPath}`;
  }

  return normalizedPath;
}

function toDateTimeLocalValue(value) {
  if (!value) {
    return '';
  }

  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return '';
  }

  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');
  return `${year}-${month}-${day}T${hours}:${minutes}`;
}

module.exports = { renderHomePage };
