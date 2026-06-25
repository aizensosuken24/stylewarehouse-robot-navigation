/* ── Config ────────────────────────────────────────────────── */
// In production, Vercel injects VITE_API_URL at build time.
// For plain HTML/JS we fall back to the env comment below;
// replace the localhost URL with your Render service URL.
const API_BASE =
  (typeof process !== "undefined" && process.env?.VITE_API_URL) ||
  window.ENV_API_URL ||
  (["localhost", "127.0.0.1", ""].includes(window.location.hostname)
    ? "http://localhost:5000"
    : "https://speckit-api.onrender.com");

/* ── State ─────────────────────────────────────────────────── */
let warehouseData  = null;
let itemsPage      = 1;
let itemsQuery     = "";
let pathData       = null;

/* ── Utility ────────────────────────────────────────────────── */
const $  = (sel, ctx = document) => ctx.querySelector(sel);
const $$ = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];

function toast(msg, ok = true) {
  const el = $("#toast");
  el.textContent = msg;
  el.className = "toast";
  el.style.borderColor = ok ? "var(--accent2)" : "var(--danger)";
  setTimeout(() => el.classList.add("hidden"), 3000);
}

async function api(path, opts = {}) {
  const url = `${API_BASE}${path}`;
  try {
    const res = await fetch(url, {
      headers: { "Content-Type": "application/json" },
      ...opts
    });
    return await res.json();
  } catch (e) {
    console.error("API error:", e);
    return { success: false, error: e.message };
  }
}

function statusBadge(status) {
  const map = {
    idle:      ["badge-ok",    "Idle"],
    moving:    ["badge-warn",  "Moving"],
    picking:   ["badge-warn",  "Picking"],
    charging:  ["badge-ok",    "Charging"],
    error:     ["badge-danger","Error"],
    returning: ["badge-warn",  "Returning"]
  };
  const [cls, label] = map[status] || ["badge-warn", status];
  return `<span class="badge ${cls}">${label}</span>`;
}

function batteryClass(pct) {
  if (pct > 50) return "high";
  if (pct > 20) return "medium";
  return "low";
}

/* ── Health check ───────────────────────────────────────────── */
async function checkHealth() {
  const dot   = $("#api-status");
  const label = $("#api-label");
  const res   = await api("/health");
  if (res.success) {
    dot.className   = "status-dot online";
    label.textContent = "API Online";
  } else {
    dot.className   = "status-dot offline";
    label.textContent = "API Offline";
  }
}

/* ── Dashboard ──────────────────────────────────────────────── */
async function loadDashboard() {
  const [robotRes, itemRes, lowRes, whRes] = await Promise.all([
    api("/api/robots"),
    api("/api/items?per_page=1"),
    api("/api/items/low-stock"),
    api("/api/warehouse")
  ]);

  if (robotRes.success) {
    const s = robotRes.data.summary;
    $("#stat-robots").textContent  = s.total;
    $("#stat-idle").textContent    = s.idle;
    $("#stat-battery").textContent = `${s.average_battery}%`;
    renderFleetList(robotRes.data.robots);
  }
  if (itemRes.success)  $("#stat-items").textContent    = itemRes.data.total;
  if (lowRes.success)   $("#stat-lowstock").textContent = lowRes.data.length;

  if (whRes.success) {
    warehouseData = whRes.data;
    drawWarehouseMap("map-canvas", warehouseData, null);
  }
}

function renderFleetList(robots) {
  const el = $("#fleet-list");
  el.innerHTML = robots.map(r => `
    <div class="robot-row">
      <div>
        <div style="font-weight:600">${r.name}</div>
        <div style="color:var(--muted);font-size:11px">${r.id} · ${r.x},${r.y}</div>
      </div>
      <div style="display:flex;align-items:center;gap:10px">
        ${statusBadge(r.status)}
        <span style="font-size:12px;color:${r.battery>20?'var(--accent2)':'var(--danger)'}">${r.battery}%</span>
      </div>
    </div>
  `).join("");
}

/* ── Warehouse map canvas ───────────────────────────────────── */
function drawWarehouseMap(canvasId, wh, path, start, goal) {
  const canvas = $(`#${canvasId}`);
  const ctx    = canvas.getContext("2d");
  const W      = canvas.width;
  const H      = canvas.height;
  const COLS   = wh.width  || 20;
  const ROWS   = wh.height || 20;
  const cw     = W / COLS;
  const ch     = H / ROWS;

  ctx.clearRect(0, 0, W, H);

  // Grid
  ctx.strokeStyle = "#1e242c";
  ctx.lineWidth   = 0.5;
  for (let x = 0; x <= COLS; x++) {
    ctx.beginPath(); ctx.moveTo(x*cw, 0); ctx.lineTo(x*cw, H); ctx.stroke();
  }
  for (let y = 0; y <= ROWS; y++) {
    ctx.beginPath(); ctx.moveTo(0, y*ch); ctx.lineTo(W, y*ch); ctx.stroke();
  }

  // Zones
  (wh.zones || []).forEach(z => {
    ctx.fillStyle = z.color + "22";
    ctx.fillRect(z.x*cw, z.y*ch, z.width*cw, z.height*ch);
    ctx.strokeStyle = z.color + "88";
    ctx.lineWidth   = 1;
    ctx.strokeRect(z.x*cw, z.y*ch, z.width*cw, z.height*ch);
    ctx.fillStyle   = z.color;
    ctx.font        = `bold ${Math.max(9, cw*0.7)}px monospace`;
    ctx.fillText(z.id, z.x*cw + 4, z.y*ch + 13);
  });

  // Obstacles
  ctx.fillStyle = "#30363d";
  (wh.obstacles || []).forEach(o => {
    ctx.fillRect(o.x*cw + 1, o.y*ch + 1, cw - 2, ch - 2);
  });

  // Shelves
  ctx.fillStyle = "#58a6ff44";
  (wh.shelves || []).forEach(s => {
    ctx.fillRect(s.x*cw + 2, s.y*ch + 2, cw - 4, ch - 4);
  });

  // Charging stations
  ctx.fillStyle = "#f59e0b";
  (wh.charging_stations || []).forEach(cs => {
    ctx.beginPath();
    ctx.arc(cs.x*cw + cw/2, cs.y*ch + ch/2, cw*0.35, 0, Math.PI*2);
    ctx.fill();
  });

  // Robots
  (wh.robots || []).forEach(r => {
    ctx.fillStyle = "#3fb950";
    ctx.beginPath();
    ctx.arc(r.x*cw + cw/2, r.y*ch + ch/2, cw*0.38, 0, Math.PI*2);
    ctx.fill();
    ctx.fillStyle = "#0d1117";
    ctx.font = `bold ${Math.max(8, cw*0.55)}px monospace`;
    ctx.textAlign = "center";
    ctx.fillText(r.id.replace(/^\D+/g, '') || r.id, r.x*cw + cw/2, r.y*ch + ch/2 + 3);
    ctx.textAlign = "left";
  });

  // Path
  if (path && path.length > 1) {
    ctx.strokeStyle = "#58a6ffcc";
    ctx.lineWidth   = cw * 0.25;
    ctx.lineCap     = "round";
    ctx.lineJoin    = "round";
    ctx.beginPath();
    ctx.moveTo(path[0][0]*cw + cw/2, path[0][1]*ch + ch/2);
    path.forEach(([px, py]) => ctx.lineTo(px*cw + cw/2, py*ch + ch/2));
    ctx.stroke();
  }

  // Start / Goal markers
  if (start) {
    ctx.fillStyle = "#3fb950";
    ctx.fillRect(start[0]*cw + 2, start[1]*ch + 2, cw - 4, ch - 4);
  }
  if (goal) {
    ctx.fillStyle = "#f85149";
    ctx.fillRect(goal[0]*cw + 2, goal[1]*ch + 2, cw - 4, ch - 4);
  }
}

/* ── Pathfinder panel ────────────────────────────────────────── */
async function findPath() {
  const sx = parseInt($("#sx").value);
  const sy = parseInt($("#sy").value);
  const gx = parseInt($("#gx").value);
  const gy = parseInt($("#gy").value);

  const res = await api("/api/path", {
    method: "POST",
    body: JSON.stringify({ start: [sx, sy], goal: [gx, gy] })
  });

  const box = $("#path-result");
  if (res.success) {
    pathData = res.data;
    box.textContent = `Path found!\nSteps: ${res.data.steps}  |  Length: ${res.data.length.toFixed(2)} units\nRoute: ${res.data.path.map(p => `(${p[0]},${p[1]})`).join(" → ")}`;
    box.classList.remove("hidden");
    if (warehouseData) {
      drawWarehouseMap("path-canvas", warehouseData, res.data.path, [sx, sy], [gx, gy]);
    }
    toast("Path found!");
  } else {
    box.textContent = `Error: ${res.error}`;
    box.classList.remove("hidden");
    toast(res.error, false);
  }
}

async function optimisePickRoute() {
  const raw = $("#pick-items").value;
  const ids = raw.split(",").map(s => s.trim()).filter(Boolean);
  if (!ids.length) { toast("Enter at least one item ID", false); return; }

  const res = await api("/api/pick", {
    method: "POST",
    body: JSON.stringify({ item_ids: ids })
  });

  const box = $("#pick-result");
  if (res.success) {
    const d = res.data;
    box.textContent = [
      `Robot: ${d.robot.name} (${d.robot.id})`,
      `Stops: ${d.stops.map(s => `${s.item_id}@${s.shelf_id}`).join(", ")}`,
      `Optimised distance: ${d.total_distance} units`,
      `Route: ${d.optimised_route.route.map(p => `(${p[0]},${p[1]})`).join(" → ")}`
    ].join("\n");
    box.classList.remove("hidden");
    toast("Route optimised!");
  } else {
    box.textContent = `Error: ${res.error}`;
    box.classList.remove("hidden");
    toast(res.error, false);
  }
}

/* ── Inventory panel ─────────────────────────────────────────── */
async function loadItems() {
  const res = await api(`/api/items?q=${encodeURIComponent(itemsQuery)}&page=${itemsPage}&per_page=15`);
  if (!res.success) return;

  const tbody = $("#items-tbody");
  const items = res.data.items;

  tbody.innerHTML = items.map(item => {
    const low = item.quantity <= item.reorder_point;
    return `<tr>
      <td style="font-family:var(--font);color:var(--muted)">${item.id}</td>
      <td>${item.name}</td>
      <td>${item.category}</td>
      <td>${item.quantity}</td>
      <td>${item.reorder_point}</td>
      <td style="font-family:var(--font)">${item.location_id}</td>
      <td><span class="badge ${low ? "badge-danger" : "badge-ok"}">${low ? "Low" : "OK"}</span></td>
    </tr>`;
  }).join("");

  renderPagination(res.data);
}

function renderPagination(data) {
  const el = $("#items-pagination");
  const pages = data.pages;
  el.innerHTML = Array.from({ length: pages }, (_, i) => i + 1)
    .map(p => `<button class="${p === itemsPage ? "active" : ""}" data-page="${p}">${p}</button>`)
    .join("");
  el.querySelectorAll("button").forEach(btn => {
    btn.addEventListener("click", () => {
      itemsPage = parseInt(btn.dataset.page);
      loadItems();
    });
  });
}

/* ── Robot panel ─────────────────────────────────────────────── */
async function loadRobots() {
  const res = await api("/api/robots");
  if (!res.success) return;

  const el = $("#robot-cards");
  el.innerHTML = res.data.robots.map(r => {
    const bc = batteryClass(r.battery);
    return `
      <div class="robot-card">
        <div class="robot-card-header">
          <div>
            <div class="robot-card-name">${r.name}</div>
            <div class="robot-card-id">${r.id} · (${r.x}, ${r.y})</div>
          </div>
          ${statusBadge(r.status)}
        </div>
        <div class="battery-bar-wrap">
          <div class="battery-bar-label">
            <span>Battery</span><span>${r.battery}%</span>
          </div>
          <div class="battery-bar">
            <div class="battery-fill ${bc}" style="width:${r.battery}%"></div>
          </div>
        </div>
        <div class="robot-stats">
          <span>Distance <b>${r.total_distance}</b></span>
          <span>Picks <b>${r.total_picks}</b></span>
        </div>
        <div style="margin-top:12px;display:flex;gap:8px">
          <button class="btn btn-ghost btn-sm" onclick="chargeRobot('${r.id}')">⚡ Charge</button>
        </div>
        ${r.error_message ? `<div style="color:var(--danger);font-size:11px;margin-top:8px">⚠ ${r.error_message}</div>` : ""}
      </div>
    `;
  }).join("");
}

async function chargeRobot(id) {
  const res = await api(`/api/robots/${id}/charge`, { method: "POST" });
  if (res.success) {
    toast(`${res.data.name} charged to 100%`);
    loadRobots();
  } else {
    toast(res.error, false);
  }
}

/* ── Panel navigation ────────────────────────────────────────── */
function switchPanel(name) {
  $$(".nav-btn").forEach(b => b.classList.toggle("active", b.dataset.panel === name));
  $$(".panel").forEach(p => p.classList.toggle("active", p.id === `panel-${name}`));

  if (name === "dashboard")  loadDashboard();
  if (name === "inventory")  { itemsPage = 1; loadItems(); }
  if (name === "robots")     loadRobots();
  if (name === "pathfinder" && warehouseData) {
    drawWarehouseMap("path-canvas", warehouseData, null);
  }
}

/* ── Init ────────────────────────────────────────────────────── */
document.addEventListener("DOMContentLoaded", async () => {
  // Navigation
  $$(".nav-btn").forEach(btn =>
    btn.addEventListener("click", () => switchPanel(btn.dataset.panel))
  );

  // Pathfinder
  $("#find-path-btn").addEventListener("click", findPath);
  $("#pick-btn").addEventListener("click", optimisePickRoute);
  $("#refresh-btn").addEventListener("click", loadDashboard);

  // Item search (debounced)
  let searchTimer;
  $("#item-search").addEventListener("input", e => {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(() => {
      itemsQuery = e.target.value;
      itemsPage  = 1;
      loadItems();
    }, 300);
  });

  // Startup
  await checkHealth();
  await loadDashboard();

  // Auto-refresh health every 30s
  setInterval(checkHealth, 30_000);
});
