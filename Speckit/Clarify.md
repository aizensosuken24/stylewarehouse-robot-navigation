# Clarify

## Project Name
**Speckit** — Warehouse Robot Navigation & Management System

## Problem Statement
Warehouse operations require robots to navigate complex grid-based floor plans efficiently,
pick multiple items in optimal order, and manage battery life across a fleet. Manual routing
leads to wasted movement, collisions, and missed pick orders.

## What We're Building
A full-stack system that:
- Computes shortest paths for robots using A* on a 20×20 grid
- Optimises multi-stop pick routes using TSP (nearest-neighbour + 2-opt)
- Tracks robot state (position, battery, status) across a fleet
- Exposes a REST API consumed by a browser-based dashboard

## Key Constraints
- Grid is 20×20 cells; obstacles are walls between zones
- Robots carry battery (100%) that drains 0.5% per cell moved, 1% per pick
- Low-battery threshold: 20% → robot must return to charge station
- No real-time comms needed (polling is fine for MVP)
- Backend deploys on Render (free tier); frontend on Vercel (free tier)
