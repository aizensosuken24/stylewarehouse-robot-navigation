const API_BASE =
  (typeof process !== "undefined" && process.env?.VITE_API_URL) ||
  window.ENV_API_URL ||
  (["localhost", "127.0.0.1", ""].includes(window.location.hostname)
    ? "http://localhost:5000"
    : "https://stylewarehouse-robot-navigation-1.onrender.com");

const TRANSLATIONS = {
  en: {
    pageTitle: "Smart-Robo Nav | Warehouse Control",
    "brand.name": "Smart-Robo Nav",
    "brand.subtitle": "Warehouse control grid",
    "language.label": "Language",
    "nav.dashboard": "Dashboard",
    "nav.pathfinder": "Pathfinder",
    "nav.inventory": "Inventory",
    "nav.robots": "Robots",
    "status.connecting": "Connecting",
    "status.online": "API online",
    "status.offline": "API offline",
    "dashboard.eyebrow": "Ops overview",
    "dashboard.title": "Zone-gated warehouse routing",
    "dashboard.description":
      "Every zone uses one controlled entry and one controlled exit. Paths now respect those gates and the obstacle grid inside and outside each zone.",
    "dashboard.meta.app": "App",
    "dashboard.meta.routing": "Routing",
    "dashboard.meta.routingValue": "A* + gated zones",
    "stats.robotsOnline": "Robots online",
    "stats.idleNow": "Idle now",
    "stats.avgBattery": "Avg battery",
    "stats.trackedSkus": "Tracked SKUs",
    "stats.lowStock": "Low stock",
    "map.title": "Warehouse map",
    "map.description": "Zone entry and exit gates are shown directly on the grid.",
    "legend.zones": "Zones",
    "legend.obstacles": "Obstacles",
    "legend.entry": "Entry",
    "legend.exit": "Exit",
    "legend.robots": "Robots",
    "fleet.title": "Fleet status",
    "fleet.description": "Live robot state, battery, and location.",
    "zones.title": "Zone access",
    "zones.description": "Only these gates allow movement across zone boundaries.",
    "zones.zoneLabel": "Zone {id}",
    "zones.entryPoint": "Entry {point}",
    "zones.exitPoint": "Exit {point}",
    "zones.gated": "Gated",
    "pathfinder.eyebrow": "Routing",
    "pathfinder.title": "Pathfinder",
    "pathfinder.findTitle": "Find path",
    "pathfinder.findDescription": "The route respects zone gates and obstacles automatically.",
    "pathfinder.startX": "Start X",
    "pathfinder.startY": "Start Y",
    "pathfinder.goalX": "Goal X",
    "pathfinder.goalY": "Goal Y",
    "pathfinder.visualTitle": "Path visual",
    "pathfinder.visualDescription": "Start, goal, and routed cells are plotted on the same gated map.",
    "pick.title": "Pick route optimizer",
    "pick.description": "Orders stops using the live traversable distance, not straight-line distance.",
    "pick.itemIds": "Item IDs",
    "pick.placeholder": "ITM001, ITM003, ITM005",
    "inventory.eyebrow": "Stock",
    "inventory.title": "Inventory",
    "inventory.searchPlaceholder": "Search items",
    "robots.eyebrow": "Fleet",
    "robots.title": "Robot fleet",
    "table.id": "ID",
    "table.name": "Name",
    "table.category": "Category",
    "table.qty": "Qty",
    "table.reorder": "Reorder",
    "table.location": "Location",
    "table.status": "Status",
    "actions.reload": "Reload data",
    "actions.findPath": "Find path",
    "actions.optimizeRoute": "Optimize route",
    "actions.charge": "Charge",
    "robot.battery": "Battery",
    "robot.distance": "Distance",
    "robot.picks": "Picks",
    "item.low": "Low",
    "item.ok": "OK",
    "robotStatus.idle": "Idle",
    "robotStatus.moving": "Moving",
    "robotStatus.picking": "Picking",
    "robotStatus.charging": "Charging",
    "robotStatus.error": "Error",
    "robotStatus.returning": "Returning",
    "messages.pathFound": "Path found",
    "messages.steps": "Steps: {value}",
    "messages.length": "Length: {value} units",
    "messages.route": "Route: {value}",
    "messages.routeOrder": "Route order: {value}",
    "messages.error": "Error: {value}",
    "messages.enterItemId": "Enter at least one item ID",
    "messages.pickOptimized": "Pick route optimized",
    "messages.dashboardRefreshed": "Dashboard refreshed",
    "messages.robotLine": "Robot: {name} ({id})",
    "messages.stopsLine": "Stops: {value}",
    "messages.distanceLine": "Distance: {value} units",
    "messages.chargeSuccess": "{name} charged to 100%",
    "messages.pathRequestFailed": "Path request failed",
    "messages.routeRequestFailed": "Route request failed",
    "messages.chargeFailed": "Charge failed"
  },
  hi: {
    pageTitle: "Smart-Robo Nav | वेयरहाउस नियंत्रण",
    "brand.name": "स्मार्ट-रोबो नैव",
    "brand.subtitle": "वेयरहाउस नियंत्रण ग्रिड",
    "language.label": "भाषा",
    "nav.dashboard": "डैशबोर्ड",
    "nav.pathfinder": "पाथफाइंडर",
    "nav.inventory": "इन्वेंटरी",
    "nav.robots": "रोबोट",
    "status.connecting": "कनेक्ट हो रहा है",
    "status.online": "एपीआई ऑनलाइन है",
    "status.offline": "एपीआई ऑफलाइन है",
    "dashboard.eyebrow": "ऑप्स अवलोकन",
    "dashboard.title": "ज़ोन-गेटेड वेयरहाउस रूटिंग",
    "dashboard.description":
      "हर ज़ोन के लिए एक नियंत्रित प्रवेश और एक नियंत्रित निकास है। अब पाथ इन गेट्स और ज़ोन के अंदर-बाहर की बाधाओं का पालन करते हैं।",
    "dashboard.meta.app": "ऐप",
    "dashboard.meta.routing": "रूटिंग",
    "dashboard.meta.routingValue": "A* + गेटेड ज़ोन",
    "stats.robotsOnline": "ऑनलाइन रोबोट",
    "stats.idleNow": "अभी निष्क्रिय",
    "stats.avgBattery": "औसत बैटरी",
    "stats.trackedSkus": "ट्रैक किए गए SKU",
    "stats.lowStock": "कम स्टॉक",
    "map.title": "वेयरहाउस मैप",
    "map.description": "ज़ोन प्रवेश और निकास गेट्स ग्रिड पर सीधे दिखाए गए हैं।",
    "legend.zones": "ज़ोन",
    "legend.obstacles": "बाधाएँ",
    "legend.entry": "प्रवेश",
    "legend.exit": "निकास",
    "legend.robots": "रोबोट",
    "fleet.title": "फ्लीट स्थिति",
    "fleet.description": "रोबोट की लाइव स्थिति, बैटरी और लोकेशन।",
    "zones.title": "ज़ोन एक्सेस",
    "zones.description": "ज़ोन सीमाओं के पार केवल यही गेट्स आवागमन की अनुमति देते हैं।",
    "zones.zoneLabel": "ज़ोन {id}",
    "zones.entryPoint": "प्रवेश {point}",
    "zones.exitPoint": "निकास {point}",
    "zones.gated": "नियंत्रित",
    "pathfinder.eyebrow": "रूटिंग",
    "pathfinder.title": "पाथफाइंडर",
    "pathfinder.findTitle": "पाथ खोजें",
    "pathfinder.findDescription": "रूट अपने-आप ज़ोन गेट्स और बाधाओं का पालन करता है।",
    "pathfinder.startX": "प्रारंभ X",
    "pathfinder.startY": "प्रारंभ Y",
    "pathfinder.goalX": "लक्ष्य X",
    "pathfinder.goalY": "लक्ष्य Y",
    "pathfinder.visualTitle": "पाथ दृश्य",
    "pathfinder.visualDescription": "प्रारंभ, लक्ष्य और रूटेड सेल्स एक ही गेटेड मैप पर दिखाए जाते हैं।",
    "pick.title": "पिक रूट ऑप्टिमाइज़र",
    "pick.description": "स्टॉप्स का क्रम सीधी दूरी से नहीं, बल्कि वास्तविक चलने योग्य दूरी से तय होता है।",
    "pick.itemIds": "आइटम आईडी",
    "pick.placeholder": "ITM001, ITM003, ITM005",
    "inventory.eyebrow": "स्टॉक",
    "inventory.title": "इन्वेंटरी",
    "inventory.searchPlaceholder": "आइटम खोजें",
    "robots.eyebrow": "फ्लीट",
    "robots.title": "रोबोट फ्लीट",
    "table.id": "आईडी",
    "table.name": "नाम",
    "table.category": "श्रेणी",
    "table.qty": "मात्रा",
    "table.reorder": "रीऑर्डर",
    "table.location": "स्थान",
    "table.status": "स्थिति",
    "actions.reload": "डेटा पुनः लोड करें",
    "actions.findPath": "पाथ खोजें",
    "actions.optimizeRoute": "रूट ऑप्टिमाइज़ करें",
    "actions.charge": "चार्ज",
    "robot.battery": "बैटरी",
    "robot.distance": "दूरी",
    "robot.picks": "पिक्स",
    "item.low": "कम",
    "item.ok": "ठीक",
    "robotStatus.idle": "निष्क्रिय",
    "robotStatus.moving": "चल रहा है",
    "robotStatus.picking": "पिक कर रहा है",
    "robotStatus.charging": "चार्ज हो रहा है",
    "robotStatus.error": "त्रुटि",
    "robotStatus.returning": "वापस आ रहा है",
    "messages.pathFound": "पाथ मिल गया",
    "messages.steps": "कदम: {value}",
    "messages.length": "लंबाई: {value} यूनिट",
    "messages.route": "रूट: {value}",
    "messages.routeOrder": "रूट क्रम: {value}",
    "messages.error": "त्रुटि: {value}",
    "messages.enterItemId": "कम से कम एक आइटम आईडी दर्ज करें",
    "messages.pickOptimized": "पिक रूट ऑप्टिमाइज़ हो गया",
    "messages.dashboardRefreshed": "डैशबोर्ड रीफ्रेश हो गया",
    "messages.robotLine": "रोबोट: {name} ({id})",
    "messages.stopsLine": "स्टॉप्स: {value}",
    "messages.distanceLine": "दूरी: {value} यूनिट",
    "messages.chargeSuccess": "{name} को 100% तक चार्ज किया गया",
    "messages.pathRequestFailed": "पाथ अनुरोध विफल हुआ",
    "messages.routeRequestFailed": "रूट अनुरोध विफल हुआ",
    "messages.chargeFailed": "चार्ज विफल हुआ"
  },
  te: {
    pageTitle: "Smart-Robo Nav | గిడ్డంగి నియంత్రణ",
    "brand.name": "స్మార్ట్-రోబో నావ్",
    "brand.subtitle": "గిడ్డంగి నియంత్రణ గ్రిడ్",
    "language.label": "భాష",
    "nav.dashboard": "డాష్‌బోర్డ్",
    "nav.pathfinder": "పాత్‌ఫైండర్",
    "nav.inventory": "ఇన్వెంటరీ",
    "nav.robots": "రోబోలు",
    "status.connecting": "కనెక్ట్ అవుతోంది",
    "status.online": "API ఆన్‌లైన్‌లో ఉంది",
    "status.offline": "API ఆఫ్‌లైన్‌లో ఉంది",
    "dashboard.eyebrow": "ఆప్స్ అవలోకనం",
    "dashboard.title": "జోన్-గేటెడ్ గిడ్డంగి రూటింగ్",
    "dashboard.description":
      "ప్రతి జోన్‌కు ఒక నియంత్రిత ప్రవేశం, ఒక నియంత్రిత నిష్క్రమణ ఉంది. ఇప్పుడు మార్గాలు ఈ గేట్లు మరియు జోన్ లోపల, బయట ఉన్న అడ్డంకులను గౌరవిస్తాయి.",
    "dashboard.meta.app": "యాప్",
    "dashboard.meta.routing": "రూటింగ్",
    "dashboard.meta.routingValue": "A* + గేటెడ్ జోన్‌లు",
    "stats.robotsOnline": "ఆన్‌లైన్ రోబోలు",
    "stats.idleNow": "ప్రస్తుతం నిర్జీవం",
    "stats.avgBattery": "సగటు బ్యాటరీ",
    "stats.trackedSkus": "ట్రాక్ చేసిన SKUలు",
    "stats.lowStock": "తక్కువ స్టాక్",
    "map.title": "గిడ్డంగి మ్యాప్",
    "map.description": "జోన్ ప్రవేశ, నిష్క్రమణ గేట్లు గ్రిడ్‌పై నేరుగా చూపబడతాయి.",
    "legend.zones": "జోన్‌లు",
    "legend.obstacles": "అడ్డంకులు",
    "legend.entry": "ప్రవేశం",
    "legend.exit": "నిష్క్రమణ",
    "legend.robots": "రోబోలు",
    "fleet.title": "ఫ్లీట్ స్థితి",
    "fleet.description": "రోబో లైవ్ స్థితి, బ్యాటరీ, స్థానం.",
    "zones.title": "జోన్ యాక్సెస్",
    "zones.description": "జోన్ సరిహద్దులు దాటడానికి ఈ గేట్ల ద్వారానే అనుమతి ఉంటుంది.",
    "zones.zoneLabel": "జోన్ {id}",
    "zones.entryPoint": "ప్రవేశం {point}",
    "zones.exitPoint": "నిష్క్రమణ {point}",
    "zones.gated": "నియంత్రితం",
    "pathfinder.eyebrow": "రూటింగ్",
    "pathfinder.title": "పాత్‌ఫైండర్",
    "pathfinder.findTitle": "మార్గం కనుగొను",
    "pathfinder.findDescription": "మార్గం ఆటోమేటిక్‌గా జోన్ గేట్లు, అడ్డంకులను గౌరవిస్తుంది.",
    "pathfinder.startX": "ప్రారంభం X",
    "pathfinder.startY": "ప్రారంభం Y",
    "pathfinder.goalX": "లక్ష్యం X",
    "pathfinder.goalY": "లక్ష్యం Y",
    "pathfinder.visualTitle": "మార్గ దృశ్యం",
    "pathfinder.visualDescription": "ప్రారంభం, లక్ష్యం, మార్గ సెల్‌లు ఒకే గేటెడ్ మ్యాప్‌పై చూపబడతాయి.",
    "pick.title": "పిక్ రూట్ ఆప్టిమైజర్",
    "pick.description": "స్టాప్‌ల క్రమం సూటి దూరంతో కాదు, నిజమైన ప్రయాణ దూరంతో నిర్ణయించబడుతుంది.",
    "pick.itemIds": "ఐటమ్ ఐడీలు",
    "pick.placeholder": "ITM001, ITM003, ITM005",
    "inventory.eyebrow": "స్టాక్",
    "inventory.title": "ఇన్వెంటరీ",
    "inventory.searchPlaceholder": "ఐటమ్‌లు వెతకండి",
    "robots.eyebrow": "ఫ్లీట్",
    "robots.title": "రోబో ఫ్లీట్",
    "table.id": "ఐడి",
    "table.name": "పేరు",
    "table.category": "వర్గం",
    "table.qty": "పరిమాణం",
    "table.reorder": "రీఆర్డర్",
    "table.location": "స్థానం",
    "table.status": "స్థితి",
    "actions.reload": "డేటాను మళ్లీ లోడ్ చేయండి",
    "actions.findPath": "మార్గం కనుగొను",
    "actions.optimizeRoute": "రూట్ ఆప్టిమైజ్ చేయండి",
    "actions.charge": "చార్జ్",
    "robot.battery": "బ్యాటరీ",
    "robot.distance": "దూరం",
    "robot.picks": "పిక్స్",
    "item.low": "తక్కువ",
    "item.ok": "సరే",
    "robotStatus.idle": "నిర్జీవం",
    "robotStatus.moving": "కదులుతోంది",
    "robotStatus.picking": "పిక్ చేస్తోంది",
    "robotStatus.charging": "చార్జ్ అవుతోంది",
    "robotStatus.error": "లోపం",
    "robotStatus.returning": "తిరిగి వస్తోంది",
    "messages.pathFound": "మార్గం కనుగొనబడింది",
    "messages.steps": "దశలు: {value}",
    "messages.length": "పొడవు: {value} యూనిట్లు",
    "messages.route": "మార్గం: {value}",
    "messages.routeOrder": "రూట్ క్రమం: {value}",
    "messages.error": "లోపం: {value}",
    "messages.enterItemId": "కనీసం ఒక ఐటమ్ ఐడి ఇవ్వండి",
    "messages.pickOptimized": "పిక్ రూట్ ఆప్టిమైజ్ చేయబడింది",
    "messages.dashboardRefreshed": "డాష్‌బోర్డ్ రిఫ్రెష్ చేయబడింది",
    "messages.robotLine": "రోబో: {name} ({id})",
    "messages.stopsLine": "స్టాప్‌లు: {value}",
    "messages.distanceLine": "దూరం: {value} యూనిట్లు",
    "messages.chargeSuccess": "{name} ను 100% వరకు చార్జ్ చేశారు",
    "messages.pathRequestFailed": "మార్గ అభ్యర్థన విఫలమైంది",
    "messages.routeRequestFailed": "రూట్ అభ్యర్థన విఫలమైంది",
    "messages.chargeFailed": "చార్జ్ విఫలమైంది"
  }
};

const API_ERROR_KEYS = {
  "Provide at least one item_id in 'item_ids'": "messages.enterItemId",
  "Path request failed": "messages.pathRequestFailed",
  "Route request failed": "messages.routeRequestFailed",
  "Charge failed": "messages.chargeFailed"
};

let warehouseData = null;
let itemsPage = 1;
let itemsQuery = "";
let currentLanguage = localStorage.getItem("smart-robo-nav-language") || "en";

const $ = (sel, ctx = document) => ctx.querySelector(sel);
const $$ = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];

function t(key, vars = {}) {
  const dict = TRANSLATIONS[currentLanguage] || TRANSLATIONS.en;
  const fallback = TRANSLATIONS.en[key] || key;
  const template = dict[key] || fallback;
  return template.replace(/\{(\w+)\}/g, (_, name) => String(vars[name] ?? ""));
}

function applyTranslations() {
  document.documentElement.lang = currentLanguage;
  document.title = t("pageTitle");

  $$("[data-i18n]").forEach(node => {
    node.textContent = t(node.dataset.i18n);
  });

  $$("[data-i18n-placeholder]").forEach(node => {
    node.placeholder = t(node.dataset.i18nPlaceholder);
  });
}

function localizeApiError(message) {
  if (!message) return "";
  const key = API_ERROR_KEYS[message];
  return key ? t(key) : message;
}

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
    idle: ["badge-ok", t("robotStatus.idle")],
    moving: ["badge-warn", t("robotStatus.moving")],
    picking: ["badge-warn", t("robotStatus.picking")],
    charging: ["badge-ok", t("robotStatus.charging")],
    error: ["badge-danger", t("robotStatus.error")],
    returning: ["badge-warn", t("robotStatus.returning")]
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
    label.textContent = t("status.online");
  } else {
    dot.className = "status-dot offline";
    label.textContent = t("status.offline");
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
        <div class="zone-title">${t("zones.zoneLabel", { id: zone.id })} <span class="zone-meta">${zone.name}</span></div>
        <div class="zone-gates">
          <span>${t("zones.entryPoint", { point: pointText(zone.entry) })}</span>
          <span>${t("zones.exitPoint", { point: pointText(zone.exit) })}</span>
        </div>
      </div>
      <span class="badge badge-warn">${t("zones.gated")}</span>
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
      t("messages.pathFound"),
      t("messages.steps", { value: res.data.steps }),
      t("messages.length", { value: res.data.length.toFixed(2) }),
      t("messages.route", {
        value: res.data.path.map(point => `(${point[0]},${point[1]})`).join(" -> ")
      })
    ].join("\n");
    box.classList.remove("hidden");
    if (warehouseData) {
      drawWarehouseMap("path-canvas", warehouseData, res.data.path, [sx, sy], [gx, gy]);
    }
    toast(t("messages.pathFound"));
  } else {
    const message = localizeApiError(res.error || t("messages.pathRequestFailed"));
    box.textContent = t("messages.error", { value: message });
    box.classList.remove("hidden");
    if (warehouseData) {
      drawWarehouseMap("path-canvas", warehouseData, null, [sx, sy], [gx, gy]);
    }
    toast(message, false);
  }
}

async function optimisePickRoute() {
  const raw = $("#pick-items").value;
  const ids = raw.split(",").map(item => item.trim()).filter(Boolean);

  if (!ids.length) {
    toast(t("messages.enterItemId"), false);
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
      t("messages.robotLine", { name: data.robot.name, id: data.robot.id }),
      t("messages.stopsLine", {
        value: data.stops.map(stop => `${stop.item_id}@${stop.shelf_id}`).join(", ")
      }),
      t("messages.distanceLine", { value: data.total_distance }),
      t("messages.routeOrder", {
        value: data.optimised_route.route.map(point => `(${point[0]},${point[1]})`).join(" -> ")
      })
    ].join("\n");
    box.classList.remove("hidden");
    toast(t("messages.pickOptimized"));
  } else {
    const message = localizeApiError(res.error || t("messages.routeRequestFailed"));
    box.textContent = t("messages.error", { value: message });
    box.classList.remove("hidden");
    toast(message, false);
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
        <td><span class="badge ${low ? "badge-danger" : "badge-ok"}">${low ? t("item.low") : t("item.ok")}</span></td>
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
            <span>${t("robot.battery")}</span>
            <span>${robot.battery}%</span>
          </div>
          <div class="battery-bar">
            <div class="battery-fill ${barClass}" style="width:${robot.battery}%"></div>
          </div>
        </div>

        <div class="robot-stats">
          <span>${t("robot.distance")} <b>${robot.total_distance}</b></span>
          <span>${t("robot.picks")} <b>${robot.total_picks}</b></span>
        </div>

        <div class="card-actions">
          <button class="btn btn-ghost btn-sm" onclick="chargeRobot('${robot.id}')">${t("actions.charge")}</button>
        </div>

        ${robot.error_message ? `<div style="margin-top:12px;color:#ffb0b0;font-size:12px">${localizeApiError(robot.error_message)}</div>` : ""}
      </div>
    `;
  }).join("");
}

async function chargeRobot(id) {
  const res = await api(`/api/robots/${id}/charge`, { method: "POST" });
  if (res.success) {
    toast(t("messages.chargeSuccess", { name: res.data.name }));
    loadRobots();
    loadDashboard();
  } else {
    toast(localizeApiError(res.error || t("messages.chargeFailed")), false);
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

function setLanguage(language) {
  currentLanguage = TRANSLATIONS[language] ? language : "en";
  localStorage.setItem("smart-robo-nav-language", currentLanguage);
  $("#language-select").value = currentLanguage;
  applyTranslations();
  checkHealth();
  if (warehouseData) {
    renderZoneAccess(warehouseData.zones || []);
  }
  loadDashboard();
  loadItems();
  loadRobots();
}

document.addEventListener("DOMContentLoaded", async () => {
  if (!TRANSLATIONS[currentLanguage]) {
    currentLanguage = "en";
  }

  applyTranslations();
  $("#language-select").value = currentLanguage;

  $$(".nav-btn").forEach(btn => {
    btn.addEventListener("click", () => switchPanel(btn.dataset.panel));
  });

  $("#language-select").addEventListener("change", event => {
    setLanguage(event.target.value);
  });

  $("#find-path-btn").addEventListener("click", findPath);
  $("#pick-btn").addEventListener("click", optimisePickRoute);
  $("#refresh-btn").addEventListener("click", async () => {
    await checkHealth();
    await loadDashboard();
    toast(t("messages.dashboardRefreshed"));
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
