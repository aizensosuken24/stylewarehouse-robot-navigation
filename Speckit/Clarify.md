# Clarify — 001 Warehouse Robot Navigation Agent

## Purpose
Capture the key questions and assumptions that shaped this spec before any design decisions were made.

---

## Q&A

### Q1: What is the core problem?
**Answer:** A mobile robot must navigate a dynamic warehouse floor — picking items from shelves and delivering them to packing stations — without colliding with other robots, humans, or obstacles.

---

### Q2: What actions can the robot take?
**Answer:** Discrete action space:
- `MOVE_FORWARD`
- `TURN_LEFT` (45°)
- `TURN_RIGHT` (45°)
- `WAIT` — hold position for one timestep
- `PICK` — collect item at current shelf location
- `DROP` — deposit item at packing station

---

### Q3: What does the robot observe?
**Answer:** Local observation window (5×5 grid around robot):
- Cell occupancy (empty / shelf / robot / human / obstacle)
- Current task: target shelf ID + target packing station ID
- Battery level (0–100%)
- Cargo status (carrying / empty)
- Steps remaining in current episode

---

### Q4: How is success measured?
**Answer:** Successful delivery = robot picks correct item and reaches correct packing station within the time limit. A full episode is 200 timesteps. Success rate across 100 episodes is the primary metric.

---

### Q5: What is the reward signal?
**Answer:**
- `+20` — successful delivery
- `+1` — each step closer to current target (shaped reward)
- `-10` — collision with any entity
- `-1` — per timestep (encourages efficiency)
- `-5` — episode timeout without delivery

---

### Q6: How are other robots modeled?
**Answer:** Other robots follow a **rule-based shortest-path policy** in Phase 1, creating realistic dynamic obstacles. Phase 2 introduces multi-agent RL where all robots train simultaneously.

---

### Q7: What RL algorithm is used?
**Answer:** **PPO** as the baseline. Multi-agent extension uses **MAPPO** (Multi-Agent PPO with shared critic).

---

### Q8: What simulator is used?
**Answer:** A custom `gymnasium`-compatible grid-world environment. Warehouse layout is configurable (size, shelf density, number of robots, number of humans).

---

## Key Assumptions
1. Warehouse map is known and static (shelves don't move).
2. Humans move randomly (uniform random walk) in Phase 1.
3. Battery depletion is not modeled in v1.0 — deferred to v2.0.
4. One item per trip (no multi-item carrying).
5. Communication between robots is not modeled in Phase 1.