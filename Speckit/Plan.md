# Plan — 001 Warehouse Robot Navigation Agent

## Goal
Deliver a trained RL agent achieving ≥80% delivery success in a 20×20 warehouse grid by end of Phase 1.

---

## Milestones

### Milestone 1 — Environment Ready
**Due:** Week 1
- Build `WarehouseEnv` as a `gymnasium.Env` subclass
- Implement grid rendering (ASCII + optional pygame)
- Add rule-based robots and random-walk humans
- Write unit tests for all environment transitions

**Done when:** `env.step()` and `env.reset()` pass all tests; random agent runs 1000 episodes without crash.

---

### Milestone 2 — Baseline Agent Trained
**Due:** Week 2
- Integrate Stable-Baselines3 PPO
- Run 1M timestep training with default hyperparams
- Log reward curves to wandb
- Visualize 5 rollout episodes

**Done when:** Agent achieves >40% delivery success (better than random ~10%).

---

### Milestone 3 — Tuned Agent
**Due:** Week 3
- Hyperparameter sweep (lr, entropy coeff, network size)
- Add shaped reward (step-toward-target)
- Experiment with observation window size (3×3 vs 5×5 vs 7×7)
- Train to 5M timesteps

**Done when:** Agent achieves ≥80% delivery success rate over 100 eval episodes.

---

### Milestone 4 — Evaluation & Documentation
**Due:** Week 4
- Run final eval suite (100 episodes × 3 seeds)
- Record collision rate, avg steps per delivery, success rate
- Write findings into `research.md`
- Create demo video of trained agent

**Done when:** All success criteria in `spec.md` are met and documented.

---

## Risks & Mitigations

| Risk | Mitigation |
|---|---|
| Sparse rewards slow learning | Shaped reward added from day 1 |
| Deadlocks between robots | Add `WAIT` action + timeout penalty |
| Overfitting to one layout | Train on 3 layout variants, eval on held-out |
| Training instability | Clip gradients, reduce lr if diverging |

---

## Tools & Stack
- Python 3.11
- `gymnasium` — environment interface
- `stable-baselines3` — PPO implementation
- `pygame` — optional visual rendering
- `wandb` — experiment tracking
- `pytest` — environment unit tests