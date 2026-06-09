# Research — 001 Warehouse Robot Navigation Agent

## 1. Problem Domain Overview
Warehouse automation is one of the fastest-growing applications of robotics. Companies like Amazon, Ocado, and DHL deploy fleets of mobile robots that must coordinate in real time. The core challenge is **multi-robot path planning in dynamic environments** — a problem well-suited to RL because rule-based planners struggle with unpredictability (humans, robot failures, congestion).

---

## 2. Relevant Prior Work

| Work | Key Contribution | Relevance |
|---|---|---|
| Amazon Kiva System | Shelf-to-person model using centralized control | Baseline architecture reference |
| PRIMAL (Sartoretti et al., 2019) | Multi-agent RL for path planning on grids | Direct algorithm inspiration |
| MAPPO (Yu et al., 2021) | Shared critic for cooperative MARL | Phase 2 algorithm |
| MiniGrid (Chevalier-Bellamare et al.) | Lightweight grid gym env | Environment design reference |
| FlowBot (2023) | RL for articulated object manipulation | Pickup/drop action modeling |

---

## 3. Key Challenges

**Sparse rewards** — deliveries are infrequent; shaped rewards needed to guide early learning.

**Partial observability** — robot sees only a local window; must infer global congestion from local signals.

**Multi-agent credit assignment** — in Phase 2, attributing team success to individual robot actions is non-trivial.

**Deadlocks** — two robots blocking each other head-on; requires emergent negotiation or explicit tie-breaking.

---

## 4. State-of-the-Art Benchmarks
- **Throughput**: Top systems achieve ~600 picks/hour per robot in real warehouses.
- **Collision rate**: Production systems target < 0.001 collisions per 1,000 moves.
- **RL baseline (PRIMAL)**: ~85% success rate in 40×40 grids with 10 agents.

Our Phase 1 target: **≥80% delivery success rate** in a 20×20 grid with 4 robots.

---

## 5. Environment & Tooling
- **Simulator**: Custom `gymnasium` env (grid-world, configurable layout)
- **Training**: Stable-Baselines3 for PPO; custom MAPPO implementation for Phase 2
- **Logging**: Weights & Biases (wandb)
- **Hardware**: Single GPU (RTX 3090) sufficient for Phase 1; multi-GPU for Phase 2

---

## 6. Open Questions for Future Research
- Can the agent generalize to unseen warehouse layouts zero-shot?
- Does communication between agents (e.g., sharing intended paths) significantly improve throughput?
- How does performance degrade as human density increases?