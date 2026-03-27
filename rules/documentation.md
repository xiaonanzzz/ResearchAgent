# Documentation

This rule defines the conventions for research notes, metrics tracking, and experiment documentation.

---

## research-note-all-in-one.md (Research Root)

The primary research log. A running markdown document with one section per experiment, appended chronologically. It lives at the research root directory.

### Structure

```markdown
# Research Log: <project name>

## Overview
- **Goal**: <from README.md>
- **Primary metric**: <metric name> (<lower/higher> is better)
- **Started**: <date>

---

## Experiments

(Experiments will be appended below as they are completed.)
```

### Per-Experiment Entry

After each experiment, append a section:

```markdown
### exp-<idea-name>
- **Status**: success | crash | timeout
- **Hypothesis**: <one sentence>
- **Key result**: <primary metric and value, or error summary if crashed>
- **Takeaway**: <one sentence — what did we learn?>
- **Details**: see `exp-<idea-name>/research-note.md`
```

This keeps the file scannable — a human (or the agent in a future iteration) can read it top to bottom and understand the full research trajectory.

### Example

```markdown
# Research Log: Image Classification

## Overview
- **Goal**: Maximize top-1 accuracy on ImageNet-1k
- **Primary metric**: accuracy (higher is better)
- **Started**: 2025-03-24

---

## Experiments

### exp-baseline
- **Status**: success
- **Hypothesis**: Establish baseline performance with ResNet-50
- **Key result**: accuracy = 76.1%
- **Takeaway**: Standard ResNet-50 gives us a reasonable starting point.
- **Details**: see `exp-baseline/research-note.md`

### exp-cosine-lr-schedule
- **Status**: success
- **Hypothesis**: Cosine annealing should improve convergence over step decay
- **Key result**: accuracy = 77.3% (+1.2%)
- **Takeaway**: Confirmed — cosine schedule gives a meaningful improvement with no extra cost.
- **Details**: see `exp-cosine-lr-schedule/research-note.md`

### exp-mixup-augmentation
- **Status**: crash
- **Hypothesis**: Mixup augmentation should regularize and improve generalization
- **Key result**: OOM error — mixup doubled memory footprint unexpectedly
- **Takeaway**: Need to investigate memory-efficient mixup or reduce batch size.
- **Details**: see `exp-mixup-augmentation/research-note.md`
```

---

## metrics.tsv (Research Root, Optional)

A structured table for quick numeric comparison. Only create this if the research involves many experiments targeting the same metric and sorting/filtering would be useful.

### Format

```
experiment	metric_name	metric_value	time_seconds	peak_memory_mb	status
exp-baseline	accuracy	76.1	3600	8192	success
exp-cosine-lr-schedule	accuracy	77.3	3580	8200	success
exp-mixup-augmentation	accuracy	-	-	-	crash
```

Tab-separated values. Use `-` for missing values (e.g., crashed experiments).

---

## research-note.md (Per Experiment)

Generated after each experiment inside the experiment folder. Contains the full detail of what was tried and learned.

### Template

```markdown
# Experiment: <idea-name>

## Hypothesis
<What you expected and why>

## Setup
<Brief description of what was changed/tried>

## Results
<Primary metric, resource usage, any notable observations>
<For multi-run experiments: summary table of all runs>

## Analysis
<Why did this work or not work? What does this tell us?>

## Next Steps
<Ideas this experiment suggests for future experiments>
```

Be concise but thorough. This is the permanent record of what was learned.

---

## Comparison and Analysis

When an experiment needs to be compared against prior experiments:

1. **Create analysis scripts** in the experiment folder (not in `output/`). For example:
   - `compare.py` — generates comparison tables or plots across experiments.
   - `plot_results.py` — visualizes trends (e.g., metric vs. hyperparameter).

2. Save generated figures/tables to the experiment's `output/` folder.

3. Reference the comparison results in the `research-note.md`.
