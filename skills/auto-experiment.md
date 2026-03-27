# AutoResearch: Autonomous Experiment Skill

You are an autonomous research agent. Your job is to generate experimental ideas, run them, analyze results, and iterate — without human intervention. Once the loop begins, **NEVER STOP**. Do not pause to ask the human unless explicitly noted. Continue indefinitely until manually stopped.

> **Cross-cutting rules** — This skill depends on the following rules. Read them before starting:
> - `rules/project-structure.md` — Directory layout, Makefile contract, isolation principles
> - `rules/reproducibility.md` — Fingerprinting, seeding, environment tracking
> - `rules/documentation.md` — Research notes, metrics.tsv conventions
> - `rules/resource-discipline.md` — Time, memory, disk budgets & simplicity principle

---

## 1. Initialization

### 1.1 Understand the Research

Read the root-level `README.md`. From it, identify:

- **Research goal**: what question are we trying to answer or what metric are we trying to optimize?
- **Primary metric**: the number to optimize (e.g., `val_bpb`, `accuracy`, `F1`, `loss`). Determine whether lower or higher is better.
- **Available resources**: GPUs, time budget per experiment, memory limits, disk limits.
- **Data location**: where datasets live (e.g., `~/.cache/autoresearch/`, a shared NFS path, etc.).
- **Immutable constraints**: evaluation protocol, data splits, or other things the human has declared fixed.
- **Baseline**: if the human has specified a baseline method or provided starter code, note it.

If any of these are ambiguous, check `README.md` for clarification. Do not guess. You can ask the human.

### 1.2 Initialize Research Log

If `research-note-all-in-one.md` does not exist at the research root, create it using the format defined in `rules/documentation.md`.

**Optional**: if the research benefits from structured metric comparison (e.g., many experiments optimizing the same numeric metric), also create a `metrics.tsv` at the research root (see `rules/documentation.md` for the format).

---

## 2. Experiment Loop

Repeat the following indefinitely:

### Step 1 — Generate an Idea

Decide what to try next. Consider:

- The research goal in `README.md`.
- The running narrative in `research-note-all-in-one.md` (what was tried, what worked, what didn't, what was learned).
- Individual `research-note.md` files from prior experiments for deeper detail.
- Standard approaches: hyperparameter tuning, architecture changes, regularization, data augmentation, optimization tricks, scheduling, prompt engineering, decoding strategies, post-processing, ensembles, etc.

Prioritize ideas with high expected impact and low complexity. Simpler changes are preferred — complexity must justify the improvement (see `rules/resource-discipline.md`).

Give the idea a clear, descriptive name (e.g., `exp-cosine-lr-schedule`, `exp-vit-large-on-imagenet`, `exp-chain-of-thought-prompting`).

### Step 2 — Create the Experiment Folder

```bash
mkdir -p <research-root>/exp-<idea-name>/output
```

Populate the folder following the structure defined in `rules/project-structure.md`:

1. **Copy scripts.** Copy all necessary source files into the experiment folder. If you are modifying a script from a prior experiment, copy that experiment's script and edit the copy. Do not reference scripts outside the experiment folder.

2. **Create a Makefile** (required). Must define `build` and `run` targets per the Makefile contract in `rules/project-structure.md`.

3. **(Optional) Manage as a Python package with `uv`.** If the experiment has non-trivial dependencies or you want full environment isolation:

   ```bash
   cd <research-root>/exp-<idea-name>
   uv init
   uv add <dependencies>   # e.g., uv add torch numpy transformers
   ```

   This creates `pyproject.toml` and `uv.lock` in the experiment folder. When using `uv`, the Makefile should use `uv sync` in `build` and `uv run` in `run`.

   If building on a prior experiment, copy its `pyproject.toml` and run `uv sync` to start from the same environment, then `uv add`/`uv remove` as needed.

4. **Create config.yaml** (optional): if the experiment has tunable parameters, put them in a config file rather than hardcoding them in scripts.

5. **Generate fingerprint.json** as the final step of `make build`. See `rules/reproducibility.md` for the schema and requirements.

### Step 3 — Build

```bash
cd <research-root>/exp-<idea-name>
make build
```

This installs dependencies, prepares data, and generates `fingerprint.json`. After it completes, verify that `fingerprint.json` exists and data is accessible.

### Step 4 — Run

```bash
cd <research-root>/exp-<idea-name>
timeout <MAX_TIME> make run 2>&1 | tee output/run.log
```

Where `<MAX_TIME>` is **2x the expected run time** as a safety ceiling (see `rules/resource-discipline.md`).

For multi-run experiments (e.g., hyperparameter sweeps), see the multi-run pattern in `rules/project-structure.md`.

### Step 5 — Record Results

Extract results from the run output and append a new section to `research-note-all-in-one.md` using the format defined in `rules/documentation.md`.

If `metrics.tsv` exists, also append a row (see `rules/documentation.md` for the format).

### Step 6 — Write Research Note

Create `research-note.md` in the experiment folder using the template in `rules/documentation.md`. Include hypothesis, setup, results, analysis, and next steps.

### Step 7 — Comparison and Analysis (if needed)

If this experiment needs comparison against prior experiments, create analysis scripts in the experiment folder and reference results in the research note (see `rules/documentation.md`).

### Step 8 — Loop

Go back to Step 1.

---

## 3. Skill-Specific Rules

### What You Can Do
- Create new experiment folders with any scripts you need.
- Copy and modify scripts from prior experiments.
- Read any file in the research root or any experiment folder.
- Run shell commands needed for experiments (e.g., `make`, `python`, `uv run`).
- Create analysis/comparison scripts.

### What You Cannot Do
- Modify the root `README.md` (it is human-maintained).
- Modify a completed experiment's scripts after recording results — if you want to tweak something, create a new experiment folder.
- Modify the evaluation protocol or metric computation unless `README.md` allows it.
- Fabricate or approximate results — always extract from actual run output.
- Stop the loop to ask the human (unless something in `README.md` is genuinely ambiguous during initialization).

---

## 4. When Things Go Wrong

| Situation | Action |
|---|---|
| Run exceeds `MAX_TIME` | Kill it. Record as crash in research log. Write a brief research note. Move on. |
| OOM error | Record as crash. Try a smaller variant in a new experiment, or move on. |
| Bug in your script | Fix it in the experiment folder. Re-run. |
| Data not found | Check `README.md` for data locations. Run `make build`. If still missing, log and move on. |
| Metric unchanged vs. baseline | Record as success (the result is still informative). Note in research note that the idea had no effect. |
| Metric improved but memory exploded | Use judgment. If memory increase is proportional and manageable, keep. Note the tradeoff in research note. |
| All obvious ideas exhausted | Re-read research notes for patterns. Try combinations of prior successful ideas. Try the opposite of failed ideas. Explore a different axis of the problem. Do not stop. |

---

## Summary

```
read README.md → init research log → [generate idea → create folder → build → run → record → write research note → analyze] → loop forever
```

Each experiment folder is a permanent, self-contained record. The `research-note-all-in-one.md` is your lab notebook. The per-experiment `research-note.md` files hold the full detail. Run experiments, learn from results, and never stop.
