import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const workspaceRoot = path.resolve(__dirname, '..');
const publicDir = path.join(__dirname, 'public');
const dataDir = path.join(__dirname, 'data');
const logsDir = path.join(__dirname, 'logs');
const tasksFile = path.join(dataDir, 'tasks.json');
const stateFile = path.join(dataDir, 'state.json');
const ceoFile = path.join(dataDir, 'ceo_state.json');
const port = Number(process.env.PORT || 4310);

for (const dir of [dataDir, logsDir]) fs.mkdirSync(dir, { recursive: true });
if (!fs.existsSync(tasksFile)) fs.writeFileSync(tasksFile, '[]');
if (!fs.existsSync(stateFile)) fs.writeFileSync(stateFile, JSON.stringify({ youtubeRuns: [], taskRuns: [] }, null, 2));
if (!fs.existsSync(ceoFile)) fs.writeFileSync(ceoFile, JSON.stringify({
  projects: [
    { id: 'tournado-golf', name: 'TourNado Golf', stage: 'Validation', potentialSekMonth: 120000, timeToTestDays: 7, confidence: 68, strategicFit: 90, owner: 'boss', updatedAt: new Date().toISOString() },
    { id: 'ullebets', name: 'UlleBets', stage: 'Build', potentialSekMonth: 95000, timeToTestDays: 10, confidence: 62, strategicFit: 84, owner: 'codey', updatedAt: new Date().toISOString() },
    { id: 'hantverkarofferter', name: 'HantverkarOfferter', stage: 'Validation', potentialSekMonth: 80000, timeToTestDays: 5, confidence: 58, strategicFit: 88, owner: 'radar', updatedAt: new Date().toISOString() },
    { id: 'ai-visibility-audit', name: 'AI Visibility Audit', stage: 'Idea', potentialSekMonth: 65000, timeToTestDays: 4, confidence: 55, strategicFit: 82, owner: 'boss', updatedAt: new Date().toISOString() },
    { id: 'vilkenai', name: 'VilkenAI.se', stage: 'Monetize', potentialSekMonth: 45000, timeToTestDays: 3, confidence: 72, strategicFit: 78, owner: 'moneymaker', updatedAt: new Date().toISOString() }
  ],
  decisions: [
    { id: 'dec_offer_tournado', projectId: 'tournado-golf', title: 'Välj launch-offer: år vs månad', impact: 'H', reversibility: 'Low', deadline: '2026-03-15', recommended: 'Årsplan + early adopter bonus', status: 'open', createdAt: new Date().toISOString() },
    { id: 'dec_channel_hantverkar', projectId: 'hantverkarofferter', title: 'Primär kanal: SEO eller outbound först', impact: 'M', reversibility: 'High', deadline: '2026-03-18', recommended: 'Starta outbound för snabb signal', status: 'open', createdAt: new Date().toISOString() }
  ],
  nextBestAction: {
    primary: 'Lansera 1-sides waitlist för TourNado med tydlig pricing-hypotes idag.',
    backup: ['Skicka 20 riktade outreach till svenska golfgrupper', 'Sätt upp KPI-spårning för CTR och signup-rate'],
    antiNoise: ['Starta inga nya sidoprojekt idag', 'Undvik design-polish före första signal'],
    generatedAt: new Date().toISOString()
  },
  money: {
    opportunities: [
      { id: 'opp_tournado_offer', projectId: 'tournado-golf', title: 'Early adopter launch-offer', valueSek: 180000, probability: 0.35, etaDays: 21, stage: 'Validation' },
      { id: 'opp_hantverkar_leads', projectId: 'hantverkarofferter', title: 'SME leadgen pilot', valueSek: 95000, probability: 0.45, etaDays: 14, stage: 'Opportunity' }
    ],
    bets: [
      { id: 'bet_waitlist_tournado', title: 'Waitlist + pricing test', stakeHours: 8, targetMetric: 'Signup rate >= 8%', killIf: 'Under 3% efter 200 sessions', scaleIf: 'Over 8% and 30+ signups', status: 'active' },
      { id: 'bet_outbound_hantverkar', title: '20 outbound samtal', stakeHours: 6, targetMetric: 'Booked calls >= 4', killIf: '<2 calls inom 5 dagar', scaleIf: '>=4 calls och positiv intent', status: 'active' }
    ]
  }
}, null, 2));

const runtime = {
  activeRuns: new Map(),
};

function json(res, code, payload) {
  res.writeHead(code, { 'Content-Type': 'application/json; charset=utf-8' });
  res.end(JSON.stringify(payload, null, 2));
}

function readJson(file, fallback) {
  try { return JSON.parse(fs.readFileSync(file, 'utf8')); } catch { return fallback; }
}

function writeJson(file, data) {
  fs.writeFileSync(file, JSON.stringify(data, null, 2), 'utf8');
}

function id(prefix) {
  return `${prefix}_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
}

function parseBody(req) {
  return new Promise((resolve, reject) => {
    let raw = '';
    req.on('data', c => raw += c.toString('utf8'));
    req.on('end', () => {
      if (!raw.trim()) return resolve({});
      try { resolve(JSON.parse(raw)); } catch (e) { reject(e); }
    });
  });
}

function listWorkspaceTree(root, maxDepth = 2, depth = 0) {
  const skip = new Set(['node_modules', '.git', '.openclaw', '.venv', '__pycache__']);
  const name = path.basename(root);
  const node = { name, path: root.replace(workspaceRoot + path.sep, ''), type: 'dir', children: [] };
  if (depth >= maxDepth) return node;
  let entries = [];
  try { entries = fs.readdirSync(root, { withFileTypes: true }); } catch { return node; }
  entries = entries.filter(e => !skip.has(e.name)).slice(0, 80);
  for (const e of entries) {
    const full = path.join(root, e.name);
    if (e.isDirectory()) node.children.push(listWorkspaceTree(full, maxDepth, depth + 1));
    else node.children.push({ name: e.name, path: full.replace(workspaceRoot + path.sep, ''), type: 'file' });
  }
  return node;
}

function parseAgentModels() {
  const file = path.join(workspaceRoot, 'AGENT_MODELS.md');
  const text = fs.existsSync(file) ? fs.readFileSync(file, 'utf8') : '';
  const rows = text.split('\n').filter(l => l.trim().startsWith('- `'));
  return rows.map((line) => {
    const match = line.match(/- `([^`]+)`: `([^`]+)`/);
    if (!match) return null;
    const [, agent, model] = match;
    return { agent, model };
  }).filter(Boolean);
}

function collectUsageFromSessions() {
  const agentsRoot = path.resolve(workspaceRoot, '..', 'agents');
  const result = [];
  if (!fs.existsSync(agentsRoot)) return result;
  for (const agentName of fs.readdirSync(agentsRoot)) {
    const sessionsDir = path.join(agentsRoot, agentName, 'sessions');
    if (!fs.existsSync(sessionsDir)) continue;
    let input = 0, output = 0, total = 0, cost = 0;
    const files = fs.readdirSync(sessionsDir).filter(f => f.endsWith('.jsonl')).slice(-15);
    for (const file of files) {
      const full = path.join(sessionsDir, file);
      const lines = fs.readFileSync(full, 'utf8').split('\n').filter(Boolean).slice(-800);
      for (const line of lines) {
        try {
          const row = JSON.parse(line);
          const usage = row?.message?.usage;
          if (!usage) continue;
          input += usage.input || 0;
          output += usage.output || 0;
          total += usage.totalTokens || 0;
          cost += usage?.cost?.total || 0;
        } catch {}
      }
    }
    result.push({ agent: agentName, input, output, totalTokens: total, totalCost: Number(cost.toFixed(4)) });
  }
  return result;
}

function getTodayHistory(days = 7) {
  const now = new Date();
  const buckets = new Map();
  for (let i = 0; i < days; i++) {
    const d = new Date(now);
    d.setDate(now.getDate() - i);
    const key = d.toISOString().slice(0, 10);
    buckets.set(key, { date: key, changedFiles: 0, latest: [] });
  }

  function scan(dir) {
    let entries = [];
    try { entries = fs.readdirSync(dir, { withFileTypes: true }); } catch { return; }
    for (const e of entries) {
      if (['node_modules', '.git', '.openclaw', '__pycache__'].includes(e.name)) continue;
      const full = path.join(dir, e.name);
      if (e.isDirectory()) scan(full);
      else {
        let stat;
        try { stat = fs.statSync(full); } catch { continue; }
        const key = stat.mtime.toISOString().slice(0, 10);
        if (!buckets.has(key)) continue;
        const item = buckets.get(key);
        item.changedFiles += 1;
        if (item.latest.length < 12) item.latest.push(full.replace(workspaceRoot + path.sep, ''));
      }
    }
  }
  scan(workspaceRoot);
  return [...buckets.values()];
}

function appendRun(kind, payload) {
  const state = readJson(stateFile, { youtubeRuns: [], taskRuns: [] });
  if (kind === 'youtube') state.youtubeRuns.unshift(payload);
  if (kind === 'task') state.taskRuns.unshift(payload);
  state.youtubeRuns = state.youtubeRuns.slice(0, 100);
  state.taskRuns = state.taskRuns.slice(0, 200);
  writeJson(stateFile, state);
}

function clamp(n, min = 0, max = 100) {
  return Math.max(min, Math.min(max, n));
}

function scoreProjects(rawProjects = []) {
  if (!rawProjects.length) return [];
  const potentials = rawProjects.map(p => Number(p.potentialSekMonth) || 0);
  const ttts = rawProjects.map(p => Math.max(1, Number(p.timeToTestDays) || 1));
  const pMin = Math.min(...potentials), pMax = Math.max(...potentials);
  const tMin = Math.min(...ttts), tMax = Math.max(...ttts);

  return rawProjects.map((p) => {
    const potential = Number(p.potentialSekMonth) || 0;
    const ttt = Math.max(1, Number(p.timeToTestDays) || 1);
    const roi = pMax === pMin ? 70 : ((potential - pMin) / (pMax - pMin)) * 100;
    const speed = tMax === tMin ? 70 : ((tMax - ttt) / (tMax - tMin)) * 100;
    const confidence = clamp(Number(p.confidence) || 0);
    const fit = clamp(Number(p.strategicFit) || 0);
    const score = clamp((0.40 * roi) + (0.25 * speed) + (0.20 * confidence) + (0.15 * fit));
    const status = score >= 75 ? 'Go Now' : score >= 50 ? 'Validate' : 'Park';
    return { ...p, score: Number(score.toFixed(1)), status };
  }).sort((a, b) => b.score - a.score);
}

function ceoOverview(ceo = {}, tasks = []) {
  const projects = scoreProjects(ceo.projects || []);
  const openDecisions = (ceo.decisions || []).filter(d => d.status !== 'closed');
  const inProgress = tasks.filter(t => t.status === 'In Progress').length;

  const stageOrder = ['Idea', 'Validation', 'Build', 'Monetize'];
  const funnel = stageOrder.map(stage => ({
    stage,
    count: projects.filter(p => (p.stage || '').toLowerCase() === stage.toLowerCase()).length,
  }));

  const leakage = funnel.slice(0, -1).map((row, i) => ({
    from: row.stage,
    to: funnel[i + 1].stage,
    drop: Math.max(0, row.count - funnel[i + 1].count),
  })).sort((a, b) => b.drop - a.drop)[0] || null;

  return {
    kpis: {
      activeProjects: projects.length,
      goNow: projects.filter(p => p.status === 'Go Now').length,
      runningExperiments: inProgress,
      openBlockers: openDecisions.length,
    },
    nextBestAction: ceo.nextBestAction || { primary: 'Sätt dagens huvudsteg', backup: [], antiNoise: [] },
    topProjects: projects.slice(0, 5),
    topBlockers: openDecisions.slice(0, 5),
    funnel,
    leakage,
  };
}

function loadCEO() {
  return readJson(ceoFile, { projects: [], decisions: [], experiments: [], nextBestAction: {}, money: { opportunities: [], bets: [] } });
}

function saveCEO(ceo) {
  const payload = {
    projects: Array.isArray(ceo.projects) ? ceo.projects : [],
    decisions: Array.isArray(ceo.decisions) ? ceo.decisions : [],
    experiments: Array.isArray(ceo.experiments) ? ceo.experiments : [],
    nextBestAction: ceo.nextBestAction || {},
    money: {
      opportunities: Array.isArray(ceo.money?.opportunities) ? ceo.money.opportunities : [],
      bets: Array.isArray(ceo.money?.bets) ? ceo.money.bets : [],
    },
  };
  writeJson(ceoFile, payload);
  return payload;
}

function buildExecutionRadar(tasks = []) {
  const rows = tasks.map((t) => {
    const createdAt = new Date(t.createdAt || Date.now()).getTime();
    const updatedAt = new Date(t.updatedAt || Date.now()).getTime();
    const leadTimeHours = Math.max(0, (updatedAt - createdAt) / 3600000);
    const impact = t.impact || (t.status === 'Done' ? 'High' : t.status === 'Review' ? 'Medium' : 'Low');
    return {
      id: t.id,
      title: t.title,
      agent: t.agent || 'unassigned',
      status: t.status,
      impact,
      reusable: Boolean(t.reusable),
      leadTimeHours: Number(leadTimeHours.toFixed(1)),
      updatedAt: t.updatedAt,
    };
  }).sort((a, b) => new Date(b.updatedAt || 0).getTime() - new Date(a.updatedAt || 0).getTime());

  return rows.slice(0, 20);
}

function startBackgroundRun({ runId, taskId, kind, command, args, cwd, onDone }) {
  const child = spawn(command, args, { cwd, shell: false });
  const start = Date.now();
  let stdout = '';
  let stderr = '';
  runtime.activeRuns.set(runId, { runId, taskId, kind, command: [command, ...args].join(' '), status: 'running', startedAt: start });

  child.stdout.on('data', (d) => { stdout += d.toString(); });
  child.stderr.on('data', (d) => { stderr += d.toString(); });

  child.on('close', (code) => {
    const status = code === 0 ? 'completed' : 'failed';
    const rec = {
      runId,
      taskId,
      kind,
      status,
      code,
      startedAt: new Date(start).toISOString(),
      endedAt: new Date().toISOString(),
      stdout: stdout.slice(-8000),
      stderr: stderr.slice(-4000),
      command: [command, ...args].join(' '),
    };
    appendRun(kind, rec);
    runtime.activeRuns.delete(runId);
    if (onDone) onDone(rec);
  });
}

function serveStatic(req, res) {
  const reqPath = req.url === '/' ? '/index.html' : req.url;
  const safe = path.normalize(reqPath).replace(/^([.][.][/\\])+/, '');
  const file = path.join(publicDir, safe);
  if (!file.startsWith(publicDir) || !fs.existsSync(file)) {
    res.writeHead(404); res.end('Not found'); return;
  }
  const ext = path.extname(file);
  const type = {
    '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.js': 'application/javascript; charset=utf-8', '.json': 'application/json; charset=utf-8'
  }[ext] || 'text/plain; charset=utf-8';
  res.writeHead(200, { 'Content-Type': type });
  fs.createReadStream(file).pipe(res);
}

const server = http.createServer(async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Headers', 'content-type');
  if (req.method === 'OPTIONS') { res.writeHead(204); return res.end(); }

  try {
    if (req.url === '/api/overview' && req.method === 'GET') {
      const tasks = readJson(tasksFile, []);
      const usage = collectUsageFromSessions();
      const totalCost = usage.reduce((a, b) => a + b.totalCost, 0);
      return json(res, 200, {
        workspace: workspaceRoot,
        tasks: { total: tasks.length, inProgress: tasks.filter(t => t.status === 'In Progress').length, done: tasks.filter(t => t.status === 'Done').length },
        agents: parseAgentModels(),
        usage: { agents: usage, totalCost: Number(totalCost.toFixed(4)), totalTokens: usage.reduce((a, b) => a + b.totalTokens, 0) },
        running: [...runtime.activeRuns.values()],
      });
    }

    if (req.url.startsWith('/api/workspace/tree') && req.method === 'GET') {
      const depth = Number(new URL(req.url, 'http://localhost').searchParams.get('depth') || '2');
      return json(res, 200, listWorkspaceTree(workspaceRoot, Math.max(1, Math.min(depth, 4))));
    }

    if (req.url === '/api/agents' && req.method === 'GET') {
      const usage = collectUsageFromSessions();
      const modelMap = new Map(parseAgentModels().map(a => [a.agent, a.model]));
      const agents = ['boss', 'radar', 'codey', 'moneymaker', 'main'].map((a) => ({
        agent: a,
        model: modelMap.get(a) || 'unknown',
        lane: ({ boss: 'boss-desk', radar: 'radar-feed', codey: 'codey-shipping', moneymaker: 'money-maker', main: 'main' })[a],
        usage: usage.find(u => u.agent === a) || { totalTokens: 0, totalCost: 0, input: 0, output: 0 },
      }));
      return json(res, 200, agents);
    }

    if (req.url === '/api/kanban' && req.method === 'GET') {
      return json(res, 200, readJson(tasksFile, []));
    }

    if (req.url === '/api/history' && req.method === 'GET') {
      const state = readJson(stateFile, { youtubeRuns: [], taskRuns: [] });
      return json(res, 200, { daily: getTodayHistory(10), runs: state });
    }

    if (req.url === '/api/knowledge' && req.method === 'GET') {
      const picks = [
        'knowledge/companies/DEFAULT/PROFILE.md',
        'knowledge/companies/DEFAULT/YOUTUBE.md',
        'knowledge/companies/DEFAULT/CONTEXT.md',
        'knowledge/projects/PROJECT_INDEX.md',
        'MEMORY.md',
      ];
      const out = picks.map(rel => {
        const full = path.join(workspaceRoot, rel);
        const exists = fs.existsSync(full);
        return { file: rel, exists, size: exists ? fs.statSync(full).size : 0, updatedAt: exists ? fs.statSync(full).mtime.toISOString() : null };
      });
      return json(res, 200, out);
    }

    if (req.url === '/api/ceo/projects' && req.method === 'GET') {
      const ceo = loadCEO();
      return json(res, 200, scoreProjects(ceo.projects || []));
    }

    if (req.url === '/api/ceo/project' && req.method === 'POST') {
      const body = await parseBody(req);
      const ceo = loadCEO();
      const item = {
        id: body.id || id('proj'),
        name: body.name || 'Untitled project',
        stage: body.stage || 'Idea',
        potentialSekMonth: Number(body.potentialSekMonth) || 0,
        timeToTestDays: Math.max(1, Number(body.timeToTestDays) || 7),
        confidence: clamp(Number(body.confidence) || 50),
        strategicFit: clamp(Number(body.strategicFit) || 50),
        owner: body.owner || 'boss',
        updatedAt: new Date().toISOString(),
      };
      ceo.projects.unshift(item);
      saveCEO(ceo);
      return json(res, 201, item);
    }

    if (req.url.startsWith('/api/ceo/project/') && req.method === 'POST') {
      const projectId = req.url.split('/').pop();
      const body = await parseBody(req);
      const ceo = loadCEO();
      const p = (ceo.projects || []).find(x => x.id === projectId);
      if (!p) return json(res, 404, { error: 'project not found' });
      p.name = body.name ?? p.name;
      p.stage = body.stage ?? p.stage;
      p.potentialSekMonth = body.potentialSekMonth != null ? Number(body.potentialSekMonth) || 0 : p.potentialSekMonth;
      p.timeToTestDays = body.timeToTestDays != null ? Math.max(1, Number(body.timeToTestDays) || 1) : p.timeToTestDays;
      p.confidence = body.confidence != null ? clamp(Number(body.confidence) || 0) : p.confidence;
      p.strategicFit = body.strategicFit != null ? clamp(Number(body.strategicFit) || 0) : p.strategicFit;
      p.owner = body.owner ?? p.owner;
      p.updatedAt = new Date().toISOString();
      saveCEO(ceo);
      return json(res, 200, p);
    }

    if (req.url === '/api/ceo/decisions' && req.method === 'GET') {
      const ceo = loadCEO();
      const now = Date.now();
      const rows = (ceo.decisions || [])
        .filter(d => d.status !== 'closed')
        .map(d => ({
          ...d,
          agingDays: Math.max(0, Math.floor((now - new Date(d.createdAt || now).getTime()) / 86400000)),
        }))
        .sort((a, b) => {
          const impactRank = { H: 3, M: 2, L: 1 };
          return (impactRank[b.impact] || 0) - (impactRank[a.impact] || 0) || b.agingDays - a.agingDays;
        });
      return json(res, 200, rows);
    }

    if (req.url === '/api/ceo/decision' && req.method === 'POST') {
      const body = await parseBody(req);
      const ceo = loadCEO();
      const item = {
        id: body.id || id('dec'),
        projectId: body.projectId || null,
        title: body.title || 'Untitled decision',
        impact: ['H', 'M', 'L'].includes(body.impact) ? body.impact : 'M',
        reversibility: body.reversibility || 'High',
        deadline: body.deadline || null,
        recommended: body.recommended || '',
        status: 'open',
        createdAt: new Date().toISOString(),
      };
      ceo.decisions.unshift(item);
      saveCEO(ceo);
      return json(res, 201, item);
    }

    if (req.url.startsWith('/api/ceo/decision/') && req.url.endsWith('/close') && req.method === 'POST') {
      const parts = req.url.split('/');
      const decisionId = parts[parts.length - 2];
      const ceo = loadCEO();
      const d = (ceo.decisions || []).find(x => x.id === decisionId);
      if (!d) return json(res, 404, { error: 'decision not found' });
      d.status = 'closed';
      d.closedAt = new Date().toISOString();
      saveCEO(ceo);
      return json(res, 200, d);
    }

    if (req.url === '/api/ceo/overview' && req.method === 'GET') {
      const ceo = loadCEO();
      const tasks = readJson(tasksFile, []);
      return json(res, 200, ceoOverview(ceo, tasks));
    }

    if (req.url === '/api/ceo/radar' && req.method === 'GET') {
      const tasks = readJson(tasksFile, []);
      return json(res, 200, buildExecutionRadar(tasks));
    }

    if (req.url === '/api/ceo/experiments' && req.method === 'GET') {
      const ceo = loadCEO();
      const items = Array.isArray(ceo.experiments) ? ceo.experiments : [];
      const closed = items.filter(x => x.result === 'won' || x.result === 'lost');
      const won = closed.filter(x => x.result === 'won').length;
      const winRate = closed.length ? Number(((won / closed.length) * 100).toFixed(1)) : 0;
      return json(res, 200, { items, winRate, totalClosed: closed.length, won });
    }

    if (req.url === '/api/ceo/next-action' && req.method === 'POST') {
      const body = await parseBody(req);
      const ceo = loadCEO();
      ceo.nextBestAction = {
        primary: body.primary || ceo.nextBestAction?.primary || '',
        backup: Array.isArray(body.backup) ? body.backup : (ceo.nextBestAction?.backup || []),
        antiNoise: Array.isArray(body.antiNoise) ? body.antiNoise : (ceo.nextBestAction?.antiNoise || []),
        generatedAt: new Date().toISOString(),
      };
      saveCEO(ceo);
      return json(res, 200, ceo.nextBestAction);
    }

    if (req.url === '/api/money/overview' && req.method === 'GET') {
      const ceo = loadCEO();
      ceo.money = ceo.money || { opportunities: [], bets: [] };
      if ((ceo.money.opportunities || []).length === 0 && (ceo.money.bets || []).length === 0) {
        ceo.money.opportunities = [
          { id: 'opp_tournado_offer', projectId: 'tournado-golf', title: 'Early adopter launch-offer', valueSek: 180000, probability: 0.35, etaDays: 21, stage: 'Validation' },
          { id: 'opp_hantverkar_leads', projectId: 'hantverkarofferter', title: 'SME leadgen pilot', valueSek: 95000, probability: 0.45, etaDays: 14, stage: 'Opportunity' }
        ];
        ceo.money.bets = [
          { id: 'bet_waitlist_tournado', title: 'Waitlist + pricing test', stakeHours: 8, targetMetric: 'Signup rate >= 8%', killIf: 'Under 3% efter 200 sessions', scaleIf: 'Over 8% and 30+ signups', status: 'active' },
          { id: 'bet_outbound_hantverkar', title: '20 outbound samtal', stakeHours: 6, targetMetric: 'Booked calls >= 4', killIf: '<2 calls inom 5 dagar', scaleIf: '>=4 calls och positiv intent', status: 'active' }
        ];
        saveCEO(ceo);
      }
      const opportunities = ceo.money?.opportunities || [];
      const bets = ceo.money?.bets || [];
      const weightedValue = opportunities.reduce((a, o) => a + ((Number(o.valueSek) || 0) * (Number(o.probability) || 0)), 0);
      const activeBets = bets.filter(b => b.status === 'active').length;
      return json(res, 200, {
        opportunities,
        bets,
        kpis: {
          weightedValueSek: Math.round(weightedValue),
          activeBets,
          avgEtaDays: opportunities.length ? Number((opportunities.reduce((a, o) => a + (Number(o.etaDays) || 0), 0) / opportunities.length).toFixed(1)) : 0,
        }
      });
    }

    if (req.url === '/api/money/opportunity' && req.method === 'POST') {
      const body = await parseBody(req);
      const ceo = loadCEO();
      const item = {
        id: body.id || id('opp'),
        projectId: body.projectId || null,
        title: body.title || 'Untitled opportunity',
        valueSek: Number(body.valueSek) || 0,
        probability: clamp(Number(body.probability) || 0, 0, 1),
        etaDays: Math.max(1, Number(body.etaDays) || 14),
        stage: body.stage || 'Opportunity',
      };
      ceo.money = ceo.money || { opportunities: [], bets: [] };
      ceo.money.opportunities.unshift(item);
      saveCEO(ceo);
      return json(res, 201, item);
    }

    if (req.url === '/api/money/bet' && req.method === 'POST') {
      const body = await parseBody(req);
      const ceo = loadCEO();
      const item = {
        id: body.id || id('bet'),
        title: body.title || 'Untitled bet',
        stakeHours: Math.max(1, Number(body.stakeHours) || 4),
        targetMetric: body.targetMetric || '',
        killIf: body.killIf || '',
        scaleIf: body.scaleIf || '',
        status: body.status || 'active',
      };
      ceo.money = ceo.money || { opportunities: [], bets: [] };
      ceo.money.bets.unshift(item);
      saveCEO(ceo);
      return json(res, 201, item);
    }

    if (req.url.startsWith('/api/money/bet/') && req.method === 'POST') {
      const betId = req.url.split('/').pop();
      const body = await parseBody(req);
      const ceo = loadCEO();
      const b = (ceo.money?.bets || []).find(x => x.id === betId);
      if (!b) return json(res, 404, { error: 'bet not found' });
      b.status = body.status || b.status;
      saveCEO(ceo);
      return json(res, 200, b);
    }

    if (req.url === '/api/kanban/task' && req.method === 'POST') {
      const body = await parseBody(req);
      const tasks = readJson(tasksFile, []);
      const item = {
        id: id('task'),
        title: body.title || 'Untitled task',
        description: body.description || '',
        status: body.status || 'Inbox',
        agent: body.agent || null,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      };
      tasks.unshift(item);
      writeJson(tasksFile, tasks);
      return json(res, 201, item);
    }

    if (req.url === '/api/youtube/ingest' && req.method === 'POST') {
      const body = await parseBody(req);
      if (!body.url) return json(res, 400, { error: 'url required' });
      const runId = id('yt');
      startBackgroundRun({
        runId,
        kind: 'youtube',
        taskId: null,
        command: 'python',
        args: ['-X', 'utf8', 'scripts/ingest_youtube_url.py', body.url],
        cwd: workspaceRoot,
      });
      return json(res, 202, { ok: true, runId });
    }

    if (req.url.startsWith('/api/kanban/assign/') && req.method === 'POST') {
      const taskId = req.url.split('/').pop();
      const body = await parseBody(req);
      const agent = (body.agent || '').toLowerCase();
      if (!['boss', 'radar', 'codey', 'moneymaker'].includes(agent)) return json(res, 400, { error: 'invalid agent' });
      const tasks = readJson(tasksFile, []);
      const t = tasks.find(x => x.id === taskId);
      if (!t) return json(res, 404, { error: 'task not found' });
      t.agent = agent;
      t.status = 'In Progress';
      t.updatedAt = new Date().toISOString();
      writeJson(tasksFile, tasks);

      const runId = id('taskrun');
      const message = `${t.title}\n\n${t.description || ''}\n\nReturnera kort status när klart.`;
      startBackgroundRun({
        runId,
        kind: 'task',
        taskId,
        command: 'python',
        args: ['-X', 'utf8', 'scripts/delegate_agent_message.py', '--agent', agent, '--message', message],
        cwd: workspaceRoot,
        onDone: (rec) => {
          const tasksNow = readJson(tasksFile, []);
          const current = tasksNow.find(x => x.id === taskId);
          if (!current) return;
          current.status = rec.status === 'completed' ? 'Review' : 'Blocked';
          current.lastRunId = runId;
          current.updatedAt = new Date().toISOString();
          writeJson(tasksFile, tasksNow);
        }
      });
      return json(res, 202, { ok: true, runId });
    }

    if (req.url === '/api/runs' && req.method === 'GET') {
      const state = readJson(stateFile, { youtubeRuns: [], taskRuns: [] });
      return json(res, 200, { active: [...runtime.activeRuns.values()], ...state });
    }

    if (req.url.startsWith('/api/kanban/move/') && req.method === 'POST') {
      const taskId = req.url.split('/').pop();
      const body = await parseBody(req);
      const tasks = readJson(tasksFile, []);
      const t = tasks.find(x => x.id === taskId);
      if (!t) return json(res, 404, { error: 'task not found' });
      t.status = body.status || t.status;
      t.updatedAt = new Date().toISOString();
      writeJson(tasksFile, tasks);
      return json(res, 200, t);
    }

    return serveStatic(req, res);
  } catch (err) {
    json(res, 500, { error: String(err) });
  }
});

server.listen(port, () => {
  console.log(`Coastworks Command Center running on http://localhost:${port}`);
});
