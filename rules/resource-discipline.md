# Resource Discipline

This rule defines time, memory, and disk budgets, the simplicity principle, and throughput guidelines.

---

## Budgets

### Time
- Respect the per-experiment time budget specified in the project `README.md`.
- Kill runs that exceed `MAX_TIME` (set to **2x the expected run time** as a safety ceiling).
- Use `timeout <MAX_TIME> make run 2>&1 | tee output/run.log` to enforce the ceiling.

### Memory
- Monitor peak memory usage.
- Some increase is acceptable for meaningful metric gains, but do not let memory usage grow unboundedly.
- Record peak memory in the research note and metrics.tsv (if used).

### Disk
- Do not duplicate large data files. Reference data at the paths specified in `README.md`.
- Only copy scripts and configs into experiment folders.
- Clean up intermediate artifacts (e.g., checkpoints from early epochs) when they are no longer needed, unless the research requires them.

---

## Simplicity Principle

Prefer the simpler of two approaches that yield similar improvements. A 0.01 metric gain from a 3-line change is better than a 0.02 gain from a 200-line rewrite, unless the research goal explicitly values pushing the metric above all else.

Complexity must justify the improvement.

---

## Throughput

Maximize throughput by:

- Keeping each experiment focused on a single idea.
- Not deliberating excessively — run the experiment and let the metric decide.
- Fixing simple bugs quickly rather than abandoning the experiment.
- Reusing scripts from prior experiments as starting points.
- Prioritizing ideas with high expected impact and low complexity.
