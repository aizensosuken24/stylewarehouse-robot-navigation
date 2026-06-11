# Clarify — StyleWarehouse Robot Navigation

## Problem Statement
A fashion/clothing warehouse has hundreds of shelves organised by category
(brand, size, colour, garment type).  Human pickers waste time navigating
inefficient routes.  We need an autonomous robot (or robot simulation) that
can receive an **order** (list of items to pick), plan the **shortest route**
across the relevant shelves, and execute or simulate that route.

## Clarifying Questions & Answers

| # | Question | Answer |
|---|----------|--------|
| 1 | Is this a physical robot or a simulation? | Simulation first; physical integration later |
| 2 | What is the warehouse layout? | Grid-based map: aisles × shelves, configurable |
| 3 | How are items addressed? | Each item → (aisle, shelf, bin) coordinates |
| 4 | Single robot or multi-robot? | Single robot MVP; multi-robot stretch goal |
| 5 | What pathfinding constraints exist? | Avoid obstacles, one-way aisles optional |
| 6 | What is the output? | Ordered pick-list + animated path visualisation |
| 7 | What tech stack? | Pure Python 3.10+, no ROS dependency for MVP |
| 8 | Does the robot carry items back? | Yes — return to depot after each order |

## Scope (MVP)
- Grid warehouse map loader
- Item catalogue with shelf locations
- A* / Dijkstra pathfinding
- Order manager (receive → plan → execute)
- Terminal + optional pygame visualisation
- Unit tests for all core modules

## Out of Scope (MVP)
- Physical hardware control
- Multi-robot collision avoidance
- Real-time sensor input
