# Tasks — 001 Warehouse Robot Navigation Agent

## Status Legend
- `[ ]` To Do
- `[x]` Done
- `[~]` In Progress

---

## Week 1 — Environment

- [ ] Create `WarehouseEnv` class inheriting `gymnasium.Env`
- [ ] Define grid representation (numpy array, cell types)
- [ ] Implement `reset()` — random robot + task spawn
- [ ] Implement `step()` — action execution + collision detection
- [ ] Implement `_get_obs()` — extract 5×5 local window + scalars
- [ ] Implement `_compute_reward()` — all reward cases
- [ ] Add rule-based robot controller (BFS shortest path)
- [ ] Add random-walk human agents
- [ ] Implement ASCII render mode
- [ ] Write unit tests: collision, pickup, drop, timeout
- [ ] Verify random agent runs 1000 episodes without crash

---

## Week 2 — Baseline Training

- [ ] Set up wandb project `warehouse-rl`
- [ ] Write training script `train.py` with SB3 PPO
- [ ] Define eval callback (every 50k steps, 20 episodes)
- [ ] Run 1M timestep baseline training
- [ ] Log: mean reward, success rate, collision rate
- [ ] Visualize 5 rollout episodes (render to video)
- [ ] Record baseline metrics in `research.md`

---

## Week 3 — Tuning

- [ ] Run lr sweep: [1e-4, 3e-4, 1e-3]
- [ ] Run entropy coeff sweep: [0.0, 0.01, 0.05]
- [ ] Test observation window: 3×3 vs 5×5 vs 7×7
- [ ] Add shaped reward (+1 per step toward target)
- [ ] Train best config to 5M timesteps
- [ ] Eval on 3 held-out warehouse layouts
- [ ] Compare results vs Phase 1 targets in `spec.md`

---

## Week 4 — Evaluation & Wrap-up

- [ ] Final eval: 100 episodes × 3 random seeds
- [ ] Compute: success rate, avg steps/delivery, collision rate
- [ ] Record demo video of trained agent (pygame render)
- [ ] Update `research.md` with final findings
- [ ] Tag repo release `v1.0-phase1`
- [ ] Write Phase 2 kickoff notes (MAPPO setup)

---

## Backlog (Phase 2+)
- [ ] Implement MAPPO with shared critic
- [ ] Train all 4 robots simultaneously
- [ ] Add inter-robot communication channel
- [ ] Model battery depletion
- [ ] Sim-to-real transfer experiments