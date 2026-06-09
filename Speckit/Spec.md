# Spec — 001 Warehouse Robot Navigation Agent

## Overview
Train a reinforcement learning agent to control a mobile warehouse robot that picks items from shelves and delivers them to packing stations, efficiently and safely, in the presence of other robots and humans.

---

## System Architecture

```
┌─────────────────────────────────────────────┐
│              Warehouse Simulator             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │  Robot   │  │  Humans  │  │  Shelves │  │
│  │  Agent   │  │ (random) │  │ + Items  │  │
│  └────┬─────┘  └──────────┘  └──────────┘  │
│       │ obs / reward                         │
└───────┼─────────────────────────────────────┘
        │
   ┌────▼────┐
   │   PPO   │  ← Policy Network (MLP, 2 hidden layers)
   │  Agent  │
   └─────────┘
```

---

## Environment Specification

| Parameter | Value |
|---|---|
| Grid size | 20 × 20 |
| Shelves | 40 (fixed positions) |
| Packing stations | 4 (fixed, corners) |
| Robots (Phase 1) | 1 RL agent + 3 rule-based |
| Humans | 2 (random walk) |
| Timestep | 1 action per step |
| Max episode length | 200 steps |
| Observation space | 5×5 local grid + 5 scalars = 130 dims |
| Action space | Discrete(6) |

---

## Observation Vector
```
[
  local_grid (5×5×3 one-hot: empty/shelf/robot/human/obstacle),  # 75 values
  target_shelf_id_normalized,      # 1 value
  target_station_id_normalized,    # 1 value
  battery_level,                   # 1 value (v2.0)
  cargo_status,                    # 1 value (0 or 1)
  steps_remaining_normalized       # 1 value
]
```
Total: **80-dimensional** flat observation vector.

---

## Reward Function

| Event | Reward |
|---|---|
| Successful delivery | +20 |
| Step toward current target | +1 |
| Collision | -10 |
| Per timestep | -1 |
| Episode timeout | -5 |

---

## Policy Network
- **Architecture**: MLP — Input(80) → Dense(256) → ReLU → Dense(128) → ReLU → Output(6)
- **Algorithm**: PPO (clip ε=0.2, entropy coeff=0.01, GAE λ=0.95)
- **Training**: 5M timesteps, batch size 2048, 10 epochs per update

---

## Success Criteria

| Metric | Phase 1 Target |
|---|---|
| Delivery success rate | ≥ 80% |
| Avg steps per delivery | ≤ 60 |
| Collision rate | < 5% of episodes |
| Training convergence | < 5M timesteps |

---

## Phase Roadmap

**Phase 1 (current):** Single RL agent, rule-based rivals, static layout, dry run.

**Phase 2:** Multi-agent RL (MAPPO), all robots learn simultaneously, shared critic.

**Phase 3:** Real-world sim-to-real transfer on a physical robot platform.

---

## Out of Scope (v1.0)
- Battery management
- Multi-item carrying
- Inter-robot communication
- Wet/damaged floor conditions
- Dynamic shelf repositioning