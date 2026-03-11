const $ = (s) => document.querySelector(s);
const $$ = (s) => [...document.querySelectorAll(s)];

$$('.tab').forEach(btn => btn.onclick = () => {
  $$('.tab').forEach(x => x.classList.remove('active'));
  $$('.panel').forEach(x => x.classList.remove('active'));
  btn.classList.add('active');
  document.getElementById(btn.dataset.tab).classList.add('active');
});

async function api(url, options = {}) {
  const res = await fetch(url, { headers: { 'content-type': 'application/json' }, ...options });
  return res.json();
}

function money(n) { return new Intl.NumberFormat('sv-SE', { style: 'currency', currency: 'USD' }).format(n || 0); }

async function renderOverview() {
  const data = await api('/api/overview');
  $('#overview').innerHTML = `
    <h2>Översikt</h2>
    <div class="cards">
      <div class="card"><h3>Tasks totalt</h3><div class="big">${data.tasks.total}</div></div>
      <div class="card"><h3>In Progress</h3><div class="big">${data.tasks.inProgress}</div></div>
      <div class="card"><h3>Tokens (alla agenter)</h3><div class="big">${(data.usage.totalTokens || 0).toLocaleString('sv-SE')}</div></div>
      <div class="card"><h3>Total kostnad</h3><div class="big">${money(data.usage.totalCost)}</div></div>
    </div>
    <div class="card" style="margin-top:12px">
      <h3>Aktiva körningar</h3>
      ${data.running.length ? data.running.map(r => `<div>${r.kind} · <span class="status running">running</span> · ${r.command}</div>`).join('') : '<div class="small">Inga aktiva körningar just nu.</div>'}
    </div>
  `;
}

async function renderAgents() {
  const data = await api('/api/agents');
  $('#agents').innerHTML = `
    <h2>Agenter & modell</h2>
    <table class="table"><thead><tr><th>Agent</th><th>Model</th><th>Lane</th><th>Tokens</th><th>Kostnad</th></tr></thead><tbody>
      ${data.map(a => `<tr><td>${a.agent}</td><td>${a.model}</td><td>${a.lane}</td><td>${(a.usage.totalTokens||0).toLocaleString('sv-SE')}</td><td>${money(a.usage.totalCost)}</td></tr>`).join('')}
    </tbody></table>
    <p class="small">Token/kostnad hämtas från sessions .jsonl i ~/.openclaw/agents/*/sessions.</p>
  `;
}

async function renderCEO() {
  const [overview, projects, decisions, radar] = await Promise.all([
    api('/api/ceo/overview'),
    api('/api/ceo/projects'),
    api('/api/ceo/decisions'),
    api('/api/ceo/radar')
  ]);

  $('#ceo').innerHTML = `
    <h2>CEO-vy</h2>
    <div class="cards">
      <div class="card"><h3>Aktiva projekt</h3><div class="big">${overview.kpis.activeProjects}</div></div>
      <div class="card"><h3>Go Now</h3><div class="big">${overview.kpis.goNow}</div></div>
      <div class="card"><h3>Pågående execution</h3><div class="big">${overview.kpis.runningExperiments}</div></div>
      <div class="card"><h3>Öppna blockerare</h3><div class="big">${overview.kpis.openBlockers}</div></div>
    </div>

    <div class="card" style="margin-top:12px;">
      <h3>Next Best Action</h3>
      <div><strong>${overview.nextBestAction.primary || 'Saknas'}</strong></div>
      <div class="small" style="margin-top:8px;">Backup:</div>
      <ul class="small">${(overview.nextBestAction.backup || []).map(x => `<li>${x}</li>`).join('') || '<li>-</li>'}</ul>
      <div class="small">Do NOT do today:</div>
      <ul class="small">${(overview.nextBestAction.antiNoise || []).map(x => `<li>${x}</li>`).join('') || '<li>-</li>'}</ul>
      <div class="row" style="margin-top:10px; grid-template-columns: 1fr;">
        <input class="input" id="nba-primary" placeholder="Uppdatera primary action" value="${overview.nextBestAction.primary || ''}" />
        <input class="input" id="nba-backup" placeholder="Backup (separera med |)" value="${(overview.nextBestAction.backup || []).join(' | ')}" />
        <input class="input" id="nba-anti" placeholder="Anti-noise (separera med |)" value="${(overview.nextBestAction.antiNoise || []).join(' | ')}" />
        <button class="btn" id="save-nba">Spara Next Action</button>
      </div>
    </div>

    <div class="card" style="margin-top:12px;">
      <h3>Project Scoreboard</h3>
      <table class="table"><thead><tr><th>Projekt</th><th>Stage</th><th>Potential</th><th>TTT</th><th>Confidence</th><th>Fit</th><th>Score</th><th>Status</th><th>Owner</th></tr></thead><tbody>
      ${projects.map(p => `<tr><td>${p.name}</td><td>${p.stage}</td><td>${(p.potentialSekMonth||0).toLocaleString('sv-SE')} SEK</td><td>${p.timeToTestDays}d</td><td>${p.confidence}</td><td>${p.strategicFit}</td><td><strong>${p.score}</strong></td><td>${p.status}</td><td>${p.owner || '-'}</td></tr>`).join('')}
      </tbody></table>
      <div class="row" style="margin-top:10px;">
        <input class="input" id="new-proj-name" placeholder="Nytt projekt" />
        <select class="select" id="new-proj-stage"><option>Idea</option><option>Validation</option><option>Build</option><option>Monetize</option></select>
      </div>
      <div class="row" style="margin-top:8px;">
        <input class="input" id="new-proj-potential" placeholder="Potential SEK/mån" />
        <input class="input" id="new-proj-ttt" placeholder="Time-to-test dagar" />
      </div>
      <div class="row" style="margin-top:8px;">
        <input class="input" id="new-proj-confidence" placeholder="Confidence 0-100" />
        <input class="input" id="new-proj-fit" placeholder="Strategic fit 0-100" />
      </div>
      <button class="btn" id="add-project" style="margin-top:8px;">Lägg till projekt</button>
    </div>

    <div class="card" style="margin-top:12px;">
      <h3>Decision Queue</h3>
      <table class="table"><thead><tr><th>Beslut</th><th>Projekt</th><th>Impact</th><th>Reversibility</th><th>Deadline</th><th>Rekommendation</th><th>Aging</th><th></th></tr></thead><tbody>
      ${decisions.map(d => `<tr><td>${d.title}</td><td>${d.projectId}</td><td>${d.impact}</td><td>${d.reversibility}</td><td>${d.deadline || '-'}</td><td>${d.recommended || '-'}</td><td>${d.agingDays}d</td><td><button class="btn secondary" data-close-decision="${d.id}">Stäng</button></td></tr>`).join('') || '<tr><td colspan="8" class="small">Inga öppna beslut.</td></tr>'}
      </tbody></table>
      <div class="row" style="margin-top:10px; grid-template-columns: 2fr 1fr;">
        <input class="input" id="new-decision-title" placeholder="Nytt blockerande beslut" />
        <select class="select" id="new-decision-impact"><option>H</option><option selected>M</option><option>L</option></select>
      </div>
      <div class="row" style="margin-top:8px; grid-template-columns: 1fr 1fr;">
        <input class="input" id="new-decision-project" placeholder="projectId" />
        <input class="input" id="new-decision-deadline" placeholder="YYYY-MM-DD" />
      </div>
      <input class="input" id="new-decision-reco" style="margin-top:8px;" placeholder="Rekommenderat val" />
      <button class="btn" id="add-decision" style="margin-top:8px;">Lägg till beslut</button>
    </div>

    <div class="card" style="margin-top:12px;">
      <h3>Pipeline Funnel</h3>
      <div class="row">${(overview.funnel || []).map(f => `<div class="card"><h3>${f.stage}</h3><div class="big">${f.count}</div></div>`).join('')}</div>
      <div class="small" style="margin-top:8px;">Största tapp: ${overview.leakage ? `${overview.leakage.from} → ${overview.leakage.to} (${overview.leakage.drop})` : '-'}</div>
    </div>

    <div class="card" style="margin-top:12px;">
      <h3>Execution Radar</h3>
      <table class="table"><thead><tr><th>Task</th><th>Agent</th><th>Status</th><th>Impact</th><th>Reusable</th><th>Lead time</th></tr></thead><tbody>
      ${(radar || []).slice(0, 10).map(r => `<tr><td>${r.title}</td><td>${r.agent}</td><td>${r.status}</td><td>${r.impact}</td><td>${r.reusable ? 'Yes' : 'No'}</td><td>${r.leadTimeHours}h</td></tr>`).join('') || '<tr><td colspan="6" class="small">Inga execution-poster ännu.</td></tr>'}
      </tbody></table>
    </div>
  `;

  $('#save-nba').onclick = async () => {
    await api('/api/ceo/next-action', {
      method: 'POST',
      body: JSON.stringify({
        primary: $('#nba-primary').value,
        backup: $('#nba-backup').value.split('|').map(x => x.trim()).filter(Boolean),
        antiNoise: $('#nba-anti').value.split('|').map(x => x.trim()).filter(Boolean),
      })
    });
    await renderCEO();
  };

  $('#add-project').onclick = async () => {
    await api('/api/ceo/project', {
      method: 'POST',
      body: JSON.stringify({
        name: $('#new-proj-name').value,
        stage: $('#new-proj-stage').value,
        potentialSekMonth: Number($('#new-proj-potential').value || 0),
        timeToTestDays: Number($('#new-proj-ttt').value || 7),
        confidence: Number($('#new-proj-confidence').value || 50),
        strategicFit: Number($('#new-proj-fit').value || 50),
      })
    });
    await renderCEO();
  };

  $('#add-decision').onclick = async () => {
    await api('/api/ceo/decision', {
      method: 'POST',
      body: JSON.stringify({
        title: $('#new-decision-title').value,
        impact: $('#new-decision-impact').value,
        projectId: $('#new-decision-project').value || null,
        deadline: $('#new-decision-deadline').value || null,
        recommended: $('#new-decision-reco').value || '',
      })
    });
    await renderCEO();
  };

  $$('[data-close-decision]').forEach(btn => btn.onclick = async () => {
    await api(`/api/ceo/decision/${btn.dataset.closeDecision}/close`, { method: 'POST' });
    await renderCEO();
  });
}

async function renderMoney() {
  const data = await api('/api/money/overview');
  $('#money').innerHTML = `
    <h2>Money Mode</h2>
    <div class="cards">
      <div class="card"><h3>Weighted value</h3><div class="big">${(data.kpis.weightedValueSek || 0).toLocaleString('sv-SE')} SEK</div></div>
      <div class="card"><h3>Aktiva bets</h3><div class="big">${data.kpis.activeBets || 0}</div></div>
      <div class="card"><h3>Snitt ETA</h3><div class="big">${data.kpis.avgEtaDays || 0} d</div></div>
    </div>

    <div class="card" style="margin-top:12px;">
      <h3>Revenue Pipeline</h3>
      <table class="table"><thead><tr><th>Titel</th><th>Projekt</th><th>Värde</th><th>Prob</th><th>ETA</th><th>Stage</th></tr></thead><tbody>
      ${(data.opportunities || []).map(o => `<tr><td>${o.title}</td><td>${o.projectId || '-'}</td><td>${(o.valueSek||0).toLocaleString('sv-SE')} SEK</td><td>${Math.round((o.probability||0)*100)}%</td><td>${o.etaDays}d</td><td>${o.stage}</td></tr>`).join('') || '<tr><td colspan="6" class="small">Inga opportunities ännu.</td></tr>'}
      </tbody></table>
      <div class="row" style="margin-top:10px;">
        <input class="input" id="opp-title" placeholder="Ny opportunity" />
        <input class="input" id="opp-project" placeholder="projectId" />
      </div>
      <div class="row" style="margin-top:8px;">
        <input class="input" id="opp-value" placeholder="Värde SEK" />
        <input class="input" id="opp-prob" placeholder="Sannolikhet 0-1" />
      </div>
      <div class="row" style="margin-top:8px;">
        <input class="input" id="opp-eta" placeholder="ETA dagar" />
        <input class="input" id="opp-stage" placeholder="Stage" value="Opportunity" />
      </div>
      <button class="btn" id="add-opp" style="margin-top:8px;">Lägg till opportunity</button>
    </div>

    <div class="card" style="margin-top:12px;">
      <h3>Weekly Bet Board</h3>
      <table class="table"><thead><tr><th>Bet</th><th>Stake</th><th>Target</th><th>Kill if</th><th>Scale if</th><th>Status</th><th></th></tr></thead><tbody>
      ${(data.bets || []).map(b => `<tr><td>${b.title}</td><td>${b.stakeHours}h</td><td>${b.targetMetric || '-'}</td><td>${b.killIf || '-'}</td><td>${b.scaleIf || '-'}</td><td>${b.status}</td><td><button class="btn secondary" data-bet-status="${b.id}" data-next="${b.status === 'active' ? 'won' : 'active'}">${b.status === 'active' ? 'Mark won' : 'Reactivate'}</button></td></tr>`).join('') || '<tr><td colspan="7" class="small">Inga bets ännu.</td></tr>'}
      </tbody></table>

      <input class="input" id="bet-title" placeholder="Ny bet" style="margin-top:8px;" />
      <div class="row" style="margin-top:8px;">
        <input class="input" id="bet-stake" placeholder="Stake timmar" />
        <input class="input" id="bet-target" placeholder="Target metric" />
      </div>
      <input class="input" id="bet-kill" placeholder="Kill if..." style="margin-top:8px;" />
      <input class="input" id="bet-scale" placeholder="Scale if..." style="margin-top:8px;" />
      <button class="btn" id="add-bet" style="margin-top:8px;">Lägg till bet</button>
    </div>
  `;

  $('#add-opp').onclick = async () => {
    await api('/api/money/opportunity', {
      method: 'POST',
      body: JSON.stringify({
        title: $('#opp-title').value,
        projectId: $('#opp-project').value || null,
        valueSek: Number($('#opp-value').value || 0),
        probability: Number($('#opp-prob').value || 0),
        etaDays: Number($('#opp-eta').value || 14),
        stage: $('#opp-stage').value || 'Opportunity',
      })
    });
    await renderMoney();
  };

  $('#add-bet').onclick = async () => {
    await api('/api/money/bet', {
      method: 'POST',
      body: JSON.stringify({
        title: $('#bet-title').value,
        stakeHours: Number($('#bet-stake').value || 4),
        targetMetric: $('#bet-target').value,
        killIf: $('#bet-kill').value,
        scaleIf: $('#bet-scale').value,
      })
    });
    await renderMoney();
  };

  $$('[data-bet-status]').forEach(btn => btn.onclick = async () => {
    await api(`/api/money/bet/${btn.dataset.betStatus}`, { method: 'POST', body: JSON.stringify({ status: btn.dataset.next }) });
    await renderMoney();
  });
}

async function renderKanban() {
  const statuses = ['Inbox', 'Ready', 'In Progress', 'Review', 'Done'];
  const tasks = await api('/api/kanban');
  const host = document.createElement('div');
  host.className = 'kanban';
  const template = document.getElementById('kanban-col-template');
  statuses.forEach(status => {
    const col = template.content.firstElementChild.cloneNode(true);
    col.querySelector('h3').textContent = status;
    const list = col.querySelector('.kanban-list');
    tasks.filter(t => t.status === status).forEach(t => {
      const item = document.createElement('div');
      item.className = 'kanban-item';
      item.innerHTML = `
        <strong>${t.title}</strong>
        <div class="small">${t.agent || 'Ej tilldelad'} · ${new Date(t.updatedAt).toLocaleString('sv-SE')}</div>
        <p class="small">${t.description || ''}</p>
        <div class="row">
          <select class="select" data-move="${t.id}">
            ${statuses.map(s => `<option ${s===t.status?'selected':''}>${s}</option>`).join('')}
          </select>
          <select class="select" data-assign="${t.id}">
            <option value="">Assign</option><option>boss</option><option>radar</option><option>codey</option><option>moneymaker</option>
          </select>
        </div>
      `;
      list.appendChild(item);
    });
    host.appendChild(col);
  });

  $('#kanban').innerHTML = `
    <h2>Kanban</h2>
    <div class="card" style="margin-bottom:10px;">
      <div class="row">
        <input class="input" id="new-title" placeholder="Tasktitel" />
        <input class="input" id="new-agent" placeholder="Förvald agent (valfritt)" />
      </div>
      <textarea class="textarea" id="new-desc" placeholder="Beskrivning"></textarea>
      <button class="btn" id="create-task">Skapa task</button>
    </div>
  `;
  $('#kanban').appendChild(host);

  $('#create-task').onclick = async () => {
    await api('/api/kanban/task', { method: 'POST', body: JSON.stringify({ title: $('#new-title').value, description: $('#new-desc').value, agent: $('#new-agent').value || null, status: 'Inbox' }) });
    await refresh();
  };

  $$('[data-move]').forEach(el => el.onchange = async () => {
    await api(`/api/kanban/move/${el.dataset.move}`, { method: 'POST', body: JSON.stringify({ status: el.value }) });
    await refresh();
  });

  $$('[data-assign]').forEach(el => el.onchange = async () => {
    if (!el.value) return;
    await api(`/api/kanban/assign/${el.dataset.assign}`, { method: 'POST', body: JSON.stringify({ agent: el.value }) });
    await refresh();
  });
}

async function renderYoutube() {
  const runs = await api('/api/runs');
  $('#youtube').innerHTML = `
    <h2>YouTube Full Ingest</h2>
    <div class="card">
      <input id="yt-url" class="input" placeholder="Klistra in YouTube-URL" />
      <button id="yt-go" class="btn" style="margin-top:8px">Digesta och skriv till knowledge</button>
      <div class="small" style="margin-top:8px">Triggerar scripts/ingest_youtube_url.py direkt.</div>
    </div>
    <div class="card" style="margin-top:12px">
      <h3>Senaste YouTube-runs</h3>
      ${(runs.youtubeRuns||[]).slice(0,8).map(r => `<div><span class="status ${r.status}">${r.status}</span> ${r.startedAt}<div class="mono">${(r.stdout||r.stderr||'').slice(0,350)}</div></div>`).join('') || '<div class="small">Inga körningar ännu.</div>'}
    </div>
  `;

  $('#yt-go').onclick = async () => {
    const url = $('#yt-url').value.trim();
    if (!url) return alert('Lägg till URL först.');
    await api('/api/youtube/ingest', { method: 'POST', body: JSON.stringify({ url }) });
    setTimeout(refresh, 1200);
  };
}

async function renderKnowledge() {
  const data = await api('/api/knowledge');
  $('#knowledge').innerHTML = `
    <h2>Kunskapsbank</h2>
    <table class="table"><thead><tr><th>Fil</th><th>Status</th><th>Storlek</th><th>Uppdaterad</th></tr></thead><tbody>
      ${data.map(r => `<tr><td>${r.file}</td><td>${r.exists ? '✅' : '❌'}</td><td>${(r.size/1024).toFixed(1)} KB</td><td>${r.updatedAt ? new Date(r.updatedAt).toLocaleString('sv-SE') : '-'}</td></tr>`).join('')}
    </tbody></table>
  `;
}

function renderTree(node) {
  if (!node) return '';
  if (node.type === 'file') return `<li>📄 ${node.name}</li>`;
  const children = (node.children || []).map(renderTree).join('');
  return `<li>📁 ${node.name}${children ? `<ul>${children}</ul>` : ''}</li>`;
}

async function renderWorkspace() {
  const tree = await api('/api/workspace/tree?depth=2');
  $('#workspace').innerHTML = `
    <h2>Workspace Mirror</h2>
    <div class="card tree"><ul>${renderTree(tree)}</ul></div>
  `;
}

async function renderHistory() {
  const h = await api('/api/history');
  $('#history').innerHTML = `
    <h2>Daglig historik</h2>
    <div class="cards">
      ${h.daily.map(d => `<div class="card"><h3>${d.date}</h3><div class="big">${d.changedFiles}</div><div class="small">ändrade filer</div></div>`).join('')}
    </div>
    <div class="card" style="margin-top:12px">
      <h3>Task runs</h3>
      ${(h.runs.taskRuns||[]).slice(0,10).map(r => `<div><span class="status ${r.status}">${r.status}</span> ${r.taskId || ''} ${r.startedAt}<div class="mono">${(r.stdout||r.stderr||'').slice(0,260)}</div></div>`).join('') || '<div class="small">Inga task runs ännu.</div>'}
    </div>
  `;
}

async function refresh() {
  await Promise.all([renderOverview(), renderAgents(), renderCEO(), renderMoney(), renderKanban(), renderYoutube(), renderKnowledge(), renderHistory(), renderWorkspace()]);
}

refresh();
setInterval(renderOverview, 8000);
setInterval(renderYoutube, 12000);
