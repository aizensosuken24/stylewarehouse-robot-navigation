/* ── app.js — StyleWarehouse Robot Navigation ───────── */

// ── STATE ──────────────────────────────────────────────
const state = {
  rows: 10,
  cols: 10,
  obstacles: new Set(),   // "r,c" strings
  start: [0, 0],
  end: [9, 9],
  path: [],
  apiUrl: localStorage.getItem('swApiUrl') || '',
};

// ── DOM REFS ───────────────────────────────────────────
const gridCanvas    = document.getElementById('gridCanvas');
const rowsInput     = document.getElementById('rows');
const colsInput     = document.getElementById('cols');
const startRowInput = document.getElementById('startRow');
const startColInput = document.getElementById('startCol');
const endRowInput   = document.getElementById('endRow');
const endColInput   = document.getElementById('endCol');
const algorithmSel  = document.getElementById('algorithm');
const diagCheck     = document.getElementById('allowDiagonal');
const apiUrlInput   = document.getElementById('apiUrl');
const btnRun        = document.getElementById('btnRun');
const btnReset      = document.getElementById('btnReset');
const btnPing       = document.getElementById('btnPing');
const apiStatus     = document.getElementById('apiStatus');
const statSteps     = document.getElementById('statSteps');
const statCost      = document.getElementById('statCost');
const statTime      = document.getElementById('statTime');
const pathList      = document.getElementById('pathList');
const jsonBox       = document.getElementById('jsonBox');
const heroSteps     = document.getElementById('heroSteps');
const toastEl       = document.getElementById('toast');

// ── INIT ───────────────────────────────────────────────
apiUrlInput.value = state.apiUrl;
buildGrid();

// ── GRID BUILDER ───────────────────────────────────────
function buildGrid() {
  state.rows = parseInt(rowsInput.value) || 10;
  state.cols = parseInt(colsInput.value) || 10;

  // clamp waypoints
  state.start[0] = Math.min(state.start[0], state.rows - 1);
  state.start[1] = Math.min(state.start[1], state.cols - 1);
  state.end[0]   = Math.min(state.end[0],   state.rows - 1);
  state.end[1]   = Math.min(state.end[1],   state.cols - 1);

  // remove out-of-bounds obstacles
  state.obstacles.forEach(k => {
    const [r, c] = k.split(',').map(Number);
    if (r >= state.rows || c >= state.cols) state.obstacles.delete(k);
  });

  gridCanvas.style.gridTemplateColumns = `repeat(${state.cols}, 34px)`;
  gridCanvas.innerHTML = '';

  for (let r = 0; r < state.rows; r++) {
    for (let c = 0; c < state.cols; c++) {
      const cell = document.createElement('div');
      cell.className = 'cell';
      cell.dataset.r = r;
      cell.dataset.c = c;
      cell.addEventListener('click', onCellClick);
      gridCanvas.appendChild(cell);
    }
  }

  renderGrid();
}

function renderGrid() {
  const [sr, sc] = state.start;
  const [er, ec] = state.end;
  const pathSet  = new Set(state.path.map(([r, c]) => `${r},${c}`));

  document.querySelectorAll('.cell').forEach(cell => {
    const r = +cell.dataset.r;
    const c = +cell.dataset.c;
    const key = `${r},${c}`;
    cell.className = 'cell';
    if (r === sr && c === sc)          cell.classList.add('start');
    else if (r === er && c === ec)     cell.classList.add('end');
    else if (state.obstacles.has(key)) cell.classList.add('obstacle');
    else if (pathSet.has(key))         cell.classList.add('path');
  });
}

// ── CELL INTERACTION ────────────────────────────────────
function onCellClick(e) {
  const r = +e.currentTarget.dataset.r;
  const c = +e.currentTarget.dataset.c;
  const [sr, sc] = state.start;
  const [er, ec] = state.end;
  if ((r === sr && c === sc) || (r === er && c === ec)) return;
  const key = `${r},${c}`;
  state.obstacles.has(key) ? state.obstacles.delete(key) : state.obstacles.add(key);
  state.path = [];
  renderGrid();
}

// ── INPUT SYNC ─────────────────────────────────────────
startRowInput.addEventListener('change', () => { state.start[0] = +startRowInput.value; state.path=[]; renderGrid(); });
startColInput.addEventListener('change', () => { state.start[1] = +startColInput.value; state.path=[]; renderGrid(); });
endRowInput.addEventListener('change',   () => { state.end[0]   = +endRowInput.value;   state.path=[]; renderGrid(); });
endColInput.addEventListener('change',   () => { state.end[1]   = +endColInput.value;   state.path=[]; renderGrid(); });
rowsInput.addEventListener('change', buildGrid);
colsInput.addEventListener('change', buildGrid);
btnReset.addEventListener('click', () => { state.obstacles.clear(); state.path=[]; renderGrid(); toast('Grid cleared'); });

// ── PING ───────────────────────────────────────────────
btnPing.addEventListener('click', async () => {
  const url = apiUrlInput.value.trim();
  if (!url) { toast('Enter a backend URL first', 'error'); return; }
  state.apiUrl = url;
  localStorage.setItem('swApiUrl', url);
  try {
    const res = await fetch(`${url}/health`, { signal: AbortSignal.timeout(4000) });
    if (res.ok) {
      setApiStatus(true);
      toast('Backend reachable ✓', 'success');
    } else {
      setApiStatus(false);
      toast(`Backend responded ${res.status}`, 'error');
    }
  } catch {
    setApiStatus(false);
    toast('Cannot reach backend', 'error');
  }
});

function setApiStatus(online) {
  apiStatus.textContent = '';
  const dot = document.createElement('span');
  dot.className = 'dot';
  apiStatus.appendChild(dot);
  apiStatus.appendChild(document.createTextNode(online ? ' Backend online' : ' Backend offline'));
  apiStatus.className = 'status-pill' + (online ? ' online' : '');
}

// ── RUN PATH FINDING ───────────────────────────────────
btnRun.addEventListener('click', async () => {
  const url = (apiUrlInput.value || state.apiUrl).trim();

  const payload = {
    grid: {
      rows:      state.rows,
      cols:      state.cols,
      obstacles: [...state.obstacles].map(k => k.split(',').map(Number)),
    },
    start:          state.start,
    end:            state.end,
    algorithm:      algorithmSel.value,
    allow_diagonal: diagCheck.checked,
  };

  if (!url) {
    // ── LOCAL FALLBACK (BFS) when no backend configured
    toast('No backend URL — running local BFS', 'error');
    const t0 = performance.now();
    const path = localBFS(payload);
    const ms = (performance.now() - t0).toFixed(1);
    showResult({ path, cost: path.length - 1, algorithm: 'bfs-local' }, ms);
    return;
  }

  btnRun.disabled = true;
  btnRun.querySelector('span').textContent = 'Computing…';

  const t0 = performance.now();
  try {
    state.apiUrl = url;
    localStorage.setItem('swApiUrl', url);

    const res = await fetch(`${url}/navigate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
      signal: AbortSignal.timeout(10000),
    });

    const ms = (performance.now() - t0).toFixed(1);

    if (!res.ok) {
      const err = await res.text();
      toast(`API error ${res.status}: ${err}`, 'error');
      return;
    }

    const data = await res.json();
    setApiStatus(true);
    showResult(data, ms);

  } catch (err) {
    toast('Request failed — running local BFS fallback', 'error');
    const path = localBFS(payload);
    const ms = (performance.now() - t0).toFixed(1);
    showResult({ path, cost: path.length - 1, algorithm: 'bfs-local' }, ms);
  } finally {
    btnRun.disabled = false;
    btnRun.querySelector('span').textContent = 'Find Path';
  }
});

// ── DISPLAY RESULTS ────────────────────────────────────
function showResult(data, ms) {
  const path = data.path || [];
  state.path = path;
  renderGrid();

  const steps = path.length;
  statSteps.textContent = steps || '—';
  statCost.textContent  = data.cost != null ? data.cost : steps - 1 || '—';
  statTime.textContent  = ms;
  heroSteps.textContent = steps || '—';

  pathList.innerHTML = path.length
    ? path.map((([r, c], i) => `<div class="step">${String(i).padStart(2,'0')} → [${r}, ${c}]</div>`)).join('')
    : '<p class="muted">No path found.</p>';

  jsonBox.textContent = JSON.stringify(data, null, 2);

  if (path.length) {
    toast(`Path found — ${steps} steps`, 'success');
  } else {
    toast('No path found — blocked?', 'error');
  }
}

// ── LOCAL BFS FALLBACK ─────────────────────────────────
function localBFS({ grid, start, end, allow_diagonal }) {
  const { rows, cols, obstacles } = grid;
  const obsSet = new Set(obstacles.map(([r, c]) => `${r},${c}`));
  const [sr, sc] = start;
  const [er, ec] = end;

  const dirs = [[-1,0],[1,0],[0,-1],[0,1]];
  if (allow_diagonal) dirs.push([-1,-1],[-1,1],[1,-1],[1,1]);

  const queue   = [[sr, sc]];
  const visited = new Set([`${sr},${sc}`]);
  const parent  = {};

  while (queue.length) {
    const [r, c] = queue.shift();
    if (r === er && c === ec) {
      const path = [];
      let cur = `${er},${ec}`;
      while (cur) {
        const [pr, pc] = cur.split(',').map(Number);
        path.unshift([pr, pc]);
        cur = parent[cur];
      }
      return path;
    }
    for (const [dr, dc] of dirs) {
      const nr = r + dr, nc = c + dc;
      const key = `${nr},${nc}`;
      if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
      if (obsSet.has(key) || visited.has(key)) continue;
      visited.add(key);
      parent[key] = `${r},${c}`;
      queue.push([nr, nc]);
    }
  }
  return [];
}

// ── TOAST ──────────────────────────────────────────────
let toastTimer;
function toast(msg, type = '') {
  toastEl.textContent = msg;
  toastEl.className   = 'toast show' + (type ? ' ' + type : '');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { toastEl.className = 'toast'; }, 3000);
}
