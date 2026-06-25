const API_BASE =
  (typeof process !== "undefined" && process.env?.VITE_API_URL) ||
  window.ENV_API_URL ||
  (["localhost", "127.0.0.1", ""].includes(window.location.hostname)
    ? "http://localhost:5000"
    : "https://stylewarehouse-robot-navigation-1.onrender.com");

let warehouseData = null;
let itemsPage = 1;
let itemsQuery = "";

const $ = (sel, ctx = document) => ctx.querySelector(sel);
const $$ = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];

function toast(msg, ok = true) {
  const el = $("#toast");
  el.textContent = msg;
  el.className = "toast";
  el.style.borderColor = ok ? "rgba(49, 196, 141, 0.35)" : "rgba(248, 113, 113, 0.35)";
  clearTimeout(window.__toastTimer);
  window.__toastTimer = setTimeout(() => el.classList.add("hidden"), 2600);
}

async function api(path, opts = {}) {
  const url = `${API_BASE}${path}`;
  try {
    const res = await fetch(url, {
      headers: { "Content-Type": "application/json" },
      ...opts
    });
    return await res.json();
  } catch (error) {
    console.error("API error:", error);
    return { success: false, error: error.message };
  }
}

function statusBadge(status) {
  const map = {
    idle: ["badge-ok", "Idle"],
    moving: ["badge-warn", "Moving"],
    picking: ["badge-warn", "Picking"],
    charging: ["badge-ok", "Charging"],
    error: ["badge-danger", "Error"],
    returning: ["badge-warn", "Returning"]
  };

  const [cls, label] = map[status] || ["badge-warn", status];
  return `<span class="badge ${cls}">${label}</span>`;
}

function batteryClass(pct) {
  if (pct > 50) return "high";
  if (pct > 20) return "medium";
  return "low";
}

function pointText(point) {
  return `${point[0]},${point[1]}`;
}

async function checkHealth() {
  const dot = $("#api-status");
  const label = $("#api-label");
  const res = await api("/health");

  if (res.success) {
    dot.className = "status-dot online";
    label.textContent = "API online";
  } else {
    dot.className = "status-dot offline";
    label.textContent = "API offline";
  }
}

async function loadDashboard() {
  const [robotRes, itemRes, lowRes, whRes] = await Promise.all([
    api("/api/robots"),
    api("/api/items?per_page=1"),
    api("/api/items/low-stock"),
    api("/api/warehouse")
  ]);

  if (robotRes.success) {
    const summary = robotRes.data.summary;
    $("#stat-robots").textContent = summary.total;
    $("#stat-idle").textContent = summary.idle;
    $("#stat-battery").textContent = `${summary.average_battery}%`;
    renderFleetList(robotRes.data.robots);
  }

  if (itemRes.success) {
    $("#stat-items").textContent = itemRes.data.total;
  }

  if (lowRes.success) {
    $("#stat-lowstock").textContent = lowRes.data.length;
  }

  if (whRes.success) {
    warehouseData = whRes.data;
    drawWarehouseMap("map-canvas", warehouseData, null);
    renderZoneAccess(warehouseData.zones || []);
  }
}

function renderFleetList(robots) {
  const el = $("#fleet-list");
  el.innerHTML = robots.map(robot => `
    <div class="robot-row">
      <div>
        <div class="robot-title">${robot.name}</div>
        <div class="robot-meta">${robot.id} | ${robot.x},${robot.y}</div>
      </div>
      <div style="display:flex;align-items:center;gap:10px">
        ${statusBadge(robot.status)}
        <span class="robot-meta" style="color:${robot.battery > 20 ? "#7ce3bb" : "#ffb0b0"}">${robot.battery}%</span>
      </div>
    </div>
  `).join("");
}

function renderZoneAccess(zones) {
  const el = $("#zone-access-list");
  el.innerHTML = zones.map(zone => `
    <div class="zone-row">
      <div>
        <div class="zone-title">Zone ${zone.id} <span class="zone-meta">${zone.name}</span></div>
        <div class="zone-gates">
          <span>Entry ${pointText(zone.entry)}</span>
          <span>Exit ${pointText(zone.exit)}</span>
        </div>
      </div>
      <span class="badge badge-warn">Gated</span>
    </div>
  `).join("");
}

function drawWarehouseMap(canvasId, wh, path, start, goal) {
  const canvas = $(`#${canvasId}`);
  const ctx = canvas.getContext("2d");
  const width = canvas.width;
  const height = canvas.height;
  const cols = wh.width || 20;
  const rows = wh.height || 20;
  const cellWidth = width / cols;
  const cellHeight = height / rows;

  ctx.clearRect(0, 0, width, height);
  ctx.fillStyle = "#09111a";
  ctx.fillRect(0, 0, width, height);

  ctx.strokeStyle = "rgba(133, 164, 203, 0.16)";
  ctx.lineWidth = 1;
  for (let x = 0; x <= cols; x += 1) {
    ctx.beginPath();
    ctx.moveTo(x * cellWidth, 0);
    ctx.lineTo(x * cellWidth, height);
    ctx.stroke();
  }
  for (let y = 0; y <= rows; y += 1) {
    ctx.beginPath();
    ctx.moveTo(0, y * cellHeight);
    ctx.lineTo(width, y * cellHeight);
    ctx.stroke();
  }

  (wh.zones || []).forEach(zone => {
    ctx.fillStyle = `${zone.color}22`;
    ctx.fillRect(zone.x * cellWidth, zone.y * cellHeight, zone.width * cellWidth, zone.height * cellHeight);
    ctx.strokeStyle = `${zone.color}aa`;
    ctx.lineWidth = 1.4;
    ctx.strokeRect(zone.x * cellWidth, zone.y * cellHeight, zone.width * cellWidth, zone.height * cellHeight);
    ctx.fillStyle = zone.color;
    ctx.font = `bold ${Math.max(10, cellWidth * 0.62)}px sans-serif`;
    ctx.fillText(zone.id, zone.x * cellWidth + 6, zone.y * cellHeight + 14);
  });

  ctx.fillStyle = "#4b5563";
  (wh.obstacles || []).forEach(obstacle => {
    ctx.fillRect(
      obstacle.x * cellWidth + 2,
      obstacle.y * cellHeight + 2,
      cellWidth - 4,
      cellHeight - 4
    );
  });

  ctx.fillStyle = "rgba(94, 166, 255, 0.48)";
  (wh.shelves || []).forEach(shelf => {
    ctx.fillRect(
      shelf.x * cellWidth + 3,
      shelf.y * cellHeight + 3,
      cellWidth - 6,
      cellHeight - 6
    );
  });

  (wh.zones || []).forEach(zone => {
    const [entryX, entryY] = zone.entry;
    const [exitX, exitY] = zone.exit;

    ctx.fillStyle = "#31c48d";
    ctx.fillRect(entryX * cellWidth + 4, entryY * cellHeight + 4, cellWidth - 8, cellHeight - 8);
    ctx.fillStyle = "#f4b860";
    ctx.fillRect(exitX * cellWidth + 4, exitY * cellHeight + 4, cellWidth - 8, cellHeight - 8);
  });

  ctx.fillStyle = "#f4b860";
  (wh.charging_stations || []).forEach(station => {
    ctx.beginPath();
    ctx.arc(
      station.x * cellWidth + cellWidth / 2,
      station.y * cellHeight + cellHeight / 2,
      cellWidth * 0.26,
      0,
      Math.PI * 2
    );
    ctx.fill();
  });

  if (path && path.length > 1) {
    ctx.strokeStyle = "rgba(123, 193, 255, 0.95)";
    ctx.lineWidth = Math.max(4, cellWidth * 0.2);
    ctx.lineCap = "round";
    ctx.lineJoin = "round";
    ctx.beginPath();
    ctx.moveTo(path[0][0] * cellWidth + cellWidth / 2, path[0][1] * cellHeight + cellHeight / 2);
    path.forEach(([px, py]) => {
      ctx.lineTo(px * cellWidth + cellWidth / 2, py * cellHeight + cellHeight / 2);
    });
    ctx.stroke();
  }

  (wh.robots || []).forEach(robot => {
    ctx.fillStyle = "#7bc1ff";
    ctx.beginPath();
    ctx.arc(
      robot.x * cellWidth + cellWidth / 2,
      robot.y * cellHeight + cellHeight / 2,
      cellWidth * 0.28,
      0,
      Math.PI * 2
    );
    ctx.fill();

    ctx.fillStyle = "#06111c";
    ctx.font = `bold ${Math.max(8, cellWidth * 0.44)}px sans-serif`;
    ctx.textAlign = "center";
    ctx.fillText(
      robot.id.replace(/^\D+/g, "") || robot.id,
      robot.x * cellWidth + cellWidth / 2,
      robot.y * cellHeight + cellHeight / 2 + 3
    );
    ctx.textAlign = "left";
  });

  if (start) {
    ctx.strokeStyle = "#31c48d";
    ctx.lineWidth = 2;
    ctx.strokeRect(start[0] * cellWidth + 3, start[1] * cellHeight + 3, cellWidth - 6, cellHeight - 6);
  }

  if (goal) {
    ctx.strokeStyle = "#f87171";
    ctx.lineWidth = 2;
    ctx.strokeRect(goal[0] * cellWidth + 3, goal[1] * cellHeight + 3, cellWidth - 6, cellHeight - 6);
  }
}

async function findPath() {
  const sx = parseInt($("#sx").value, 10);
  const sy = parseInt($("#sy").value, 10);
  const gx = parseInt($("#gx").value, 10);
  const gy = parseInt($("#gy").value, 10);

  const res = await api("/api/path", {
    method: "POST",
    body: JSON.stringify({ start: [sx, sy], goal: [gx, gy] })
  });

  const box = $("#path-result");
  if (res.success) {
    box.textContent = [
      "Path found",
      `Steps: ${res.data.steps}`,
      `Length: ${res.data.length.toFixed(2)} units`,
      `Route: ${res.data.path.map(point => `(${point[0]},${point[1]})`).join(" -> ")}`
    ].join("\n");
    box.classList.remove("hidden");
    if (warehouseData) {
      drawWarehouseMap("path-canvas", warehouseData, res.data.path, [sx, sy], [gx, gy]);
    }
    toast("Path found");
  } else {
    box.textContent = `Error: ${res.error}`;
    box.classList.remove("hidden");
    if (warehouseData) {
      drawWarehouseMap("path-canvas", warehouseData, null, [sx, sy], [gx, gy]);
    }
    toast(res.error || "Path request failed", false);
  }
}

async function optimisePickRoute() {
  const raw = $("#pick-items").value;
  const ids = raw.split(",").map(item => item.trim()).filter(Boolean);

  if (!ids.length) {
    toast("Enter at least one item ID", false);
    return;
  }

  const res = await api("/api/pick", {
    method: "POST",
    body: JSON.stringify({ item_ids: ids })
  });

  const box = $("#pick-result");
  if (res.success) {
    const data = res.data;
    box.textContent = [
      `Robot: ${data.robot.name} (${data.robot.id})`,
      `Stops: ${data.stops.map(stop => `${stop.item_id}@${stop.shelf_id}`).join(", ")}`,
      `Distance: ${data.total_distance} units`,
      `Route order: ${data.optimised_route.route.map(point => `(${point[0]},${point[1]})`).join(" -> ")}`
    ].join("\n");
    box.classList.remove("hidden");
    toast("Pick route optimized");
  } else {
    box.textContent = `Error: ${res.error}`;
    box.classList.remove("hidden");
    toast(res.error || "Route request failed", false);
  }
}

async function loadItems() {
  const res = await api(`/api/items?q=${encodeURIComponent(itemsQuery)}&page=${itemsPage}&per_page=15`);
  if (!res.success) return;

  $("#items-tbody").innerHTML = res.data.items.map(item => {
    const low = item.quantity <= item.reorder_point;
    return `
      <tr>
        <td style="font-family:var(--font-mono);color:var(--muted)">${item.id}</td>
        <td>${item.name}</td>
        <td>${item.category}</td>
        <td>${item.quantity}</td>
        <td>${item.reorder_point}</td>
        <td style="font-family:var(--font-mono)">${item.location_id}</td>
        <td><span class="badge ${low ? "badge-danger" : "badge-ok"}">${low ? "Low" : "OK"}</span></td>
      </tr>
    `;
  }).join("");

  renderPagination(res.data);
}

function renderPagination(data) {
  const el = $("#items-pagination");
  el.innerHTML = Array.from({ length: data.pages }, (_, index) => index + 1)
    .map(page => `<button class="${page === itemsPage ? "active" : ""}" data-page="${page}">${page}</button>`)
    .join("");

  el.querySelectorAll("button").forEach(btn => {
    btn.addEventListener("click", () => {
      itemsPage = parseInt(btn.dataset.page, 10);
      loadItems();
    });
  });
}

async function loadRobots() {
  const res = await api("/api/robots");
  if (!res.success) return;

  $("#robot-cards").innerHTML = res.data.robots.map(robot => {
    const barClass = batteryClass(robot.battery);
    return `
      <div class="robot-card">
        <div class="robot-card-header">
          <div>
            <div class="robot-card-name">${robot.name}</div>
            <div class="robot-card-id">${robot.id} | (${robot.x}, ${robot.y})</div>
          </div>
          ${statusBadge(robot.status)}
        </div>

        <div class="battery-bar-wrap">
          <div class="battery-bar-label">
            <span>Battery</span>
            <span>${robot.battery}%</span>
          </div>
          <div class="battery-bar">
            <div class="battery-fill ${barClass}" style="width:${robot.battery}%"></div>
          </div>
        </div>

        <div class="robot-stats">
          <span>Distance <b>${robot.total_distance}</b></span>
          <span>Picks <b>${robot.total_picks}</b></span>
        </div>

        <div class="card-actions">
          <button class="btn btn-ghost btn-sm" onclick="chargeRobot('${robot.id}')">Charge</button>
        </div>

        ${robot.error_message ? `<div style="margin-top:12px;color:#ffb0b0;font-size:12px">${robot.error_message}</div>` : ""}
      </div>
    `;
  }).join("");
}

async function chargeRobot(id) {
  const res = await api(`/api/robots/${id}/charge`, { method: "POST" });
  if (res.success) {
    toast(`${res.data.name} charged to 100%`);
    loadRobots();
    loadDashboard();
  } else {
    toast(res.error || "Charge failed", false);
  }
}

window.chargeRobot = chargeRobot;

function switchPanel(name) {
  $$(".nav-btn").forEach(btn => btn.classList.toggle("active", btn.dataset.panel === name));
  $$(".panel").forEach(panel => panel.classList.toggle("active", panel.id === `panel-${name}`));

  if (name === "dashboard") {
    loadDashboard();
  }

  if (name === "inventory") {
    itemsPage = 1;
    loadItems();
  }

  if (name === "robots") {
    loadRobots();
  }

  if (name === "pathfinder" && warehouseData) {
    drawWarehouseMap("path-canvas", warehouseData, null);
  }
}

document.addEventListener("DOMContentLoaded", async () => {
  $$(".nav-btn").forEach(btn => {
    btn.addEventListener("click", () => switchPanel(btn.dataset.panel));
  });

  $("#find-path-btn").addEventListener("click", findPath);
  $("#pick-btn").addEventListener("click", optimisePickRoute);
  $("#refresh-btn").addEventListener("click", async () => {
    await checkHealth();
    await loadDashboard();
    toast("Dashboard refreshed");
  });

  let searchTimer;
  $("#item-search").addEventListener("input", event => {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(() => {
      itemsQuery = event.target.value;
      itemsPage = 1;
      loadItems();
    }, 250);
  });

  await checkHealth();
  await loadDashboard();

  setInterval(checkHealth, 30000);
});
