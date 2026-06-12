"""
AI Service Module for StyleWarehouse Robot Navigation

Provides AI-powered features including:
- Route optimization suggestions
- Warehouse layout analysis
- Order prediction
- Natural language query processing

Supports:
- Local AI Inference (Ollama)
- BYOK (Bring Your Own Key) for remote AI services
"""
from __future__ import annotations
import os
from typing import Dict, List, Optional, Any
from .inference import generate_text, get_env_token


class AIService:
    """AI service for warehouse robot navigation features."""
    
    def __init__(
        self,
        backend: str = "local",
        model: str = "llama2",
        token: Optional[str] = None,
        remote_url: Optional[str] = None
    ):
        """
        Initialize AI service.
        
        Args:
            backend: 'local' for Ollama or 'remote' for cloud AI
            model: Model name (e.g., 'llama2', 'mistral', 'gpt-3.5-turbo')
            token: Optional BYOK token for remote services
            remote_url: Optional custom URL for remote AI endpoint
        """
        self.backend = backend
        self.model = model
        self.token = token or get_env_token()
        self.remote_url = remote_url or os.environ.get("REMOTE_AI_URL")
        
    def optimize_route_suggestion(
        self,
        items: List[Dict[str, Any]],
        current_path: List[tuple]
    ) -> str:
        """
        Generate AI-powered route optimization suggestions.
        
        Args:
            items: List of items to pick
            current_path: Current planned path
            
        Returns:
            AI-generated optimization suggestion
        """
        prompt = f"""Analyze this warehouse picking route and suggest optimizations:

Items to pick: {len(items)}
Current path length: {len(current_path)} waypoints

Item locations: {', '.join([f"{item.get('location', 'N/A')}" for item in items[:5]])}

Provide a brief optimization suggestion (2-3 sentences) focusing on:
1. Route efficiency
2. Potential bottlenecks
3. Alternative sequencing

Keep response concise and actionable."""

        try:
            return generate_text(
                prompt=prompt,
                backend=self.backend,
                model=self.model,
                token=self.token,
                remote_url=self.remote_url
            )
        except Exception as e:
            return f"AI optimization unavailable: {str(e)}"
    
    def analyze_warehouse_layout(
        self,
        warehouse_data: Dict[str, Any]
    ) -> str:
        """
        Analyze warehouse layout and provide insights.
        
        Args:
            warehouse_data: Warehouse configuration data
            
        Returns:
            AI-generated layout analysis
        """
        prompt = f"""Analyze this warehouse layout:

Dimensions: {warehouse_data.get('rows', 'N/A')} rows × {warehouse_data.get('cols', 'N/A')} columns
Depot position: {warehouse_data.get('depot', 'N/A')}
Total items: {warehouse_data.get('total_items', 'N/A')}

Provide a brief analysis (2-3 sentences) covering:
1. Layout efficiency
2. Potential congestion areas
3. Improvement suggestions

Keep response concise."""

        try:
            return generate_text(
                prompt=prompt,
                backend=self.backend,
                model=self.model,
                token=self.token,
                remote_url=self.remote_url
            )
        except Exception as e:
            return f"AI analysis unavailable: {str(e)}"
    
    def predict_order_patterns(
        self,
        order_history: List[Dict[str, Any]]
    ) -> str:
        """
        Predict order patterns based on history.
        
        Args:
            order_history: List of previous orders
            
        Returns:
            AI-generated pattern prediction
        """
        if not order_history:
            return "Insufficient order history for pattern analysis."
        
        prompt = f"""Analyze these warehouse order patterns:

Total orders: {len(order_history)}
Sample items: {', '.join([str(order.get('items', [])[0] if order.get('items') else 'N/A') for order in order_history[:3]])}

Identify patterns and predict:
1. Most frequently picked items
2. Peak order times
3. Optimization opportunities

Provide 2-3 sentences."""

        try:
            return generate_text(
                prompt=prompt,
                backend=self.backend,
                model=self.model,
                token=self.token,
                remote_url=self.remote_url
            )
        except Exception as e:
            return f"AI prediction unavailable: {str(e)}"
    
    def process_natural_query(self, query: str) -> str:
        """
        Process natural language queries about warehouse operations.
        
        Args:
            query: User's natural language question
            
        Returns:
            AI-generated response
        """
        prompt = f"""You are a warehouse robot navigation assistant. Answer this question concisely:

Question: {query}

Provide a helpful, brief answer (2-3 sentences) related to:
- Warehouse navigation
- Order picking
- Route optimization
- Robot operations

Keep response practical and actionable."""

        try:
            return generate_text(
                prompt=prompt,
                backend=self.backend,
                model=self.model,
                token=self.token,
                remote_url=self.remote_url
            )
        except Exception as e:
            return f"AI query processing unavailable: {str(e)}"
    
    def generate_order_summary(
        self,
        order_data: Dict[str, Any]
    ) -> str:
        """
        Generate a natural language summary of an order execution.
        
        Args:
            order_data: Order execution data
            
        Returns:
            AI-generated summary
        """
        prompt = f"""Summarize this warehouse order execution:

Order ID: {order_data.get('order_id', 'N/A')}
Items picked: {len(order_data.get('items', []))}
Total distance: {order_data.get('total_distance', 0)} units
Algorithm: {order_data.get('algorithm', 'N/A')}

Provide a brief, professional summary (2-3 sentences) highlighting:
1. Execution efficiency
2. Key metrics
3. Overall performance

Keep response concise."""

        try:
            return generate_text(
                prompt=prompt,
                backend=self.backend,
                model=self.model,
                token=self.token,
                remote_url=self.remote_url
            )
        except Exception as e:
            return f"AI summary unavailable: {str(e)}"


def create_ai_service(
    backend: Optional[str] = None,
    model: Optional[str] = None,
    token: Optional[str] = None
) -> AIService:
    """
    Factory function to create an AI service instance.
    
    Args:
        backend: 'local' or 'remote' (defaults to env var AI_BACKEND or 'local')
        model: Model name (defaults to env var AI_MODEL or 'llama2')
        token: BYOK token (defaults to env var AI_BEARER_TOKEN)
        
    Returns:
        Configured AIService instance
    """
    backend = backend or os.environ.get("AI_BACKEND", "local")
    model = model or os.environ.get("AI_MODEL", "llama2")
    token = token or get_env_token()
    
    return AIService(backend=backend, model=model, token=token)
