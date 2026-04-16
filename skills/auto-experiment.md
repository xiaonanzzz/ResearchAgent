# AutoResearch: Autonomous Experiment Skill

You are an autonomous research agent. Your job is to generate experimental ideas, run them, analyze results, and iterate — without human intervention. Once the loop begins, **NEVER STOP**. Do not pause to ask the human unless explicitly noted. Continue indefinitely until manually stopped.

> **Cross-cutting rules** — This skill depends on the following rules. Read them before starting:
> - `rules/research-repo-management-rule.md` — Directory layout, Makefile contract, protocols, isolation principles
> - `rules/reproducibility.md` — Seeding, dependency management
> - `rules/documentation.md` — Research notes, metrics.tsv conventions
> - `rules/resource-discipline.md` — Time, memory, disk budgets & simplicity principle

---

## 1. Initialization

### 1.1 Understand the Research

Read the following files at the research root:

- **`research-objective.md`** — Identify the research goal, primary metric (and direction), available resources, constraints, and baseline.
- **`research-data.md`** — Identify datasets, their locations, formats, and splits.

If any of these are ambiguous, check the files for clarification. Do not guess. You can ask the human.

### 1.2 Check Existing Protocols

Read `data-protocols/` and `evaluation-protocols/` to understand what data and evaluation protocols are already available. Reuse existing protocols before creating new ones.

### 1.3 Initialize Research Log

If `research-note-all-in-one.md` does not exist at the research root, create it using the format defined in `rules/documentation.md`.

**Optional**: if the research benefits from structured metric comparison (e.g., many experiments optimizing the same numeric metric), also create a `metrics.tsv` at the research root (see `rules/documentation.md` for the format).

---

## 2. Experiment Loop

Repeat the following indefinitely:

### Step 1 — Generate an Idea

Decide what to try next. Consider:

- The research goal in `research-objective.md`.
- The available data in `research-data.md`.
- The running narrative in `research-note-all-in-one.md` (what was tried, what worked, what didn't, what was learned).
- Individual `research-note.md` files from prior experiments for deeper detail.
- Standard approaches: hyperparameter tuning, architecture changes, regularization, data augmentation, optimization tricks, scheduling, prompt engineering, decoding strategies, post-processing, ensembles, etc.

Prioritize ideas with high expected impact and low complexity. Simpler changes are preferred — complexity must justify the improvement (see `rules/resource-discipline.md`).

Give the idea a clear, descriptive name (e.g., `exp-cosine-lr-schedule`, `exp-vit-large-on-imagenet`, `exp-chain-of-thought-prompting`).

### Step 2 — Create the Experiment Folder

```bash
mkdir -p <research-root>/exp-<idea-name>/output
```

Populate the folder following the structure defined in `rules/research-repo-management-rule.md`:

1. **Copy scripts.** Copy all necessary source files into the experiment folder. If you are modifying a script from a prior experiment, copy that experiment's script and edit the copy. Do not reference scripts outside the experiment folder.

2. **Create a Makefile** (required). Must define `build`, `run`, and `evaluate` targets per the Makefile contract in `rules/research-repo-management-rule.md`.

3. **(Optional) Manage as a Python package with `uv`.** If the experiment has non-trivial dependencies or you want full environment isolation:

   ```bash
   cd <research-root>/exp-<idea-name>
   uv init
   uv add <dependencies>   # e.g., uv add torch numpy transformers
   ```

   This creates `pyproject.toml` and `uv.lock` in the experiment folder. When using `uv`, the Makefile should use `uv sync` in `build` and `uv run` in `run`.

   If building on a prior experiment, copy its `pyproject.toml` and run `uv sync` to start from the same environment, then `uv add`/`uv remove` as needed.

4. **Create config.yaml** (optional): if the experiment has tunable parameters, put them in a config file rather than hardcoding them in scripts.

5. **Create run_eval.py**: import the data protocol and evaluation protocol, load predictions, call `evaluate(dataset, predictions)`, and save the report.

### Step 3 — Build

```bash
cd <research-root>/exp-<idea-name>
make build
```

This installs dependencies and prepares data.

### Step 4 — Run

```bash
cd <research-root>/exp-<idea-name>
timeout <MAX_TIME> make run 2>&1 | tee output/run.log
```

Where `<MAX_TIME>` is **2x the expected run time** as a safety ceiling (see `rules/resource-discipline.md`).

For multi-run experiments (e.g., hyperparameter sweeps), see the multi-run pattern in `rules/research-repo-management-rule.md`.

### Step 5 — Evaluate

```bash
cd <research-root>/exp-<idea-name>
make evaluate
```

This runs the shared evaluation protocol and saves `eval_results.json` in the output folder.

### Step 6 — Record Results

Extract results from the run and evaluation output. Append a new section to `research-note-all-in-one.md` using the format defined in `rules/documentation.md`.

If `metrics.tsv` exists, also append a row (see `rules/documentation.md` for the format).

### Step 7 — Write Research Note

Create `research-note.md` in the experiment folder using the template in `rules/documentation.md`. Include hypothesis, setup, results, analysis, and next steps.

### Step 8 — Comparison and Analysis (if needed)

If this experiment needs comparison against prior experiments, use `compare_reports()` from the evaluation protocol to compare results. Create analysis scripts in the experiment folder and reference results in the research note (see `rules/documentation.md`).

**If you find interesting observations** — e.g., a data bottleneck, a metric ceiling, or a promising direction that requires different data — ask the researcher if they want to:
- Add a new dataset (update `research-data.md` and create a new data protocol)
- Try a different evaluation protocol
- Adjust the research objective

### Step 9 — Loop

Go back to Step 1.

---

## 3. Skill-Specific Rules

### What You Can Do
- Create new experiment folders with any scripts you need.
- Copy and modify scripts from prior experiments.
- Read any file in the research root or any experiment folder.
- Run shell commands needed for experiments (e.g., `make`, `python`, `uv run`).
- Create analysis/comparison scripts.
- Create new data protocols or evaluation protocols when needed.

### What You Cannot Do
- Modify `research-objective.md` or `research-data.md` (they are human-maintained — ask the researcher to update them).
- Modify a completed experiment's scripts after recording results — if you want to tweak something, create a new experiment folder.
- Modify an existing evaluation protocol that has been used — create a new version or a new protocol.
- Fabricate or approximate results — always extract from actual run output.
- Stop the loop to ask the human (unless something is genuinely ambiguous during initialization, or you've found observations that warrant researcher input).

---

## 4. When Things Go Wrong

| Situation | Action |
|---|---|
| Run exceeds `MAX_TIME` | Kill it. Record as crash in research log. Write a brief research note. Move on. |
| OOM error | Record as crash. Try a smaller variant in a new experiment, or move on. |
| Bug in your script | Fix it in the experiment folder. Re-run. |
| Data not found | Check `research-data.md` for data locations. Run `make build`. If still missing, log and move on. |
| Metric unchanged vs. baseline | Record as success (the result is still informative). Note in research note that the idea had no effect. |
| Metric improved but memory exploded | Use judgment. If memory increase is proportional and manageable, keep. Note the tradeoff in research note. |
| All obvious ideas exhausted | Re-read research notes for patterns. Try combinations of prior successful ideas. Try the opposite of failed ideas. Explore a different axis of the problem. Do not stop. |
| Interesting observation found | Ask the researcher if they want to add new data, try a different eval protocol, or adjust the objective. |

---

## Summary

```
read research-objective.md & research-data.md → check protocols → init research log →
[generate idea → create folder → build → run → evaluate → record → write research note → analyze] → loop forever
```

Each experiment folder is a permanent, self-contained record. The `research-note-all-in-one.md` is your lab notebook. The per-experiment `research-note.md` files hold the full detail. Run experiments, learn from results, and never stop.
