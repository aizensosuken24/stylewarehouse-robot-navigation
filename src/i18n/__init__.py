"""Simple i18n loader for the project."""
from __future__ import annotations
import json
import os
from typing import Dict

_CACHE: Dict[str, Dict[str, str]] = {}
_EN_TRANSLATIONS: Dict[str, str] = {
    "app_title": "StyleWarehouse Robot Navigation",
    "pygame_missing": "pygame is not installed: pip install pygame",
    "step_info": "Step {step}/{total}  position={pos}",
    "terminal_fallback": "Falling back to terminal mode.",
    "generate_error_no_ai": "No AI backend is available.",
    # UI translations
    "product_catalogue": "Product Catalogue",
    "search_products": "Search products",
    "search": "Search",
    "clear": "Clear",
    "order_simulation": "Order Simulation",
    "load_demo_order": "Load Demo Order",
    "simulate_order": "Simulate Order",
    "clear_order": "Clear Order",
    "selected_items": "Selected Items",
    "order_summary": "Order Summary",
    "warehouse_visualization": "Warehouse Visualization",
    "simulation_stats": "Simulation Stats",
    "total_distance": "Total Distance",
    "items_collected": "Items Collected",
    "waypoints": "Waypoints",
    "algorithm": "Algorithm",
    "pathfinding_details": "Pathfinding Details",
    "response_data": "Response Data",
    "connected": "Connected",
    "disconnected": "Disconnected",
    "no_items_selected": "No items selected",
    "select_items_summary": "Select items to see summary",
    "total_items": "Total Items",
    "locations": "Locations",
    "start_position": "Start Position",
    "end_position": "End Position",
    "execution_time": "Execution Time",
    # AI features
    "ai_insights": "AI Insights",
    "ai_backend": "AI Backend",
    "local_inference": "Local Inference (Ollama)",
    "remote_inference": "Remote Inference",
    "byok_token": "BYOK Token",
    "route_optimization": "Route Optimization",
    "warehouse_analysis": "Warehouse Analysis",
    "ask_ai": "Ask AI",
    "ai_processing": "AI Processing...",
    "ai_unavailable": "AI service unavailable",
    "language": "Language",
    "english": "English",
    "hindi": "हिंदी",
    "telugu": "తెలుగు",
}


def _load_lang(lang: str) -> Dict[str, str]:
    if lang in _CACHE:
        return _CACHE[lang]
    base = os.path.dirname(__file__)
    path = os.path.join(base, "translations", f"{lang}.json")
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        data = {}
    _CACHE[lang] = data
    return data


def translate(key: str, lang: str = "en") -> str:
    """Return the translated string for ``key`` with English fallback."""
    if lang == "en":
        return _EN_TRANSLATIONS.get(key, key)
    data = _load_lang(lang)
    return data.get(key, _EN_TRANSLATIONS.get(key, key))
