# Research Repo Management Rule

This rule defines the standard directory layout and organizational principles for any research project using ResearchAgent.

---

## Directory Layout

A research project is initialized via `make init research-xxx` and contains human-written research documents, shared **protocols** (data and evaluation), and a collection of **experiment folders**. Each experiment folder is a standalone, reproducible unit.

```
<research-root>/
├── research-objective.md              # human-written: problem statement, goal, metric, resources, constraints
├── research-data.md                   # human-written: datasets available, locations, formats
├── research-note-all-in-one.md        # agent-maintained: running narrative of all experiments
├── metrics.tsv                        # (optional) agent-maintained: structured metric tracking
│
├── related-works/                     # downloaded papers and literature summary
│   ├── README.md                     # structured summary of related work
│   ├── references.bib                # BibTeX entries for all papers
│   └── <author>_<year>_<title>.pdf   # downloaded papers
│
├── data-protocols/                    # shared data definitions, one .py file per protocol
│   ├── <protocol-name>.py           # e.g., imagenet_original_split.py, cifar10_stratified.py
│   └── ...
│
├── evaluation-protocols/              # shared evaluation procedures reusable across experiments
│   ├── <name>_v<N>/                  # e.g., imagenet_cls_v1/, bleu_eval_v1/ (must be valid Python module)
│   │   ├── README.md                 # dataset format, predictions format, report format
│   │   ├── __init__.py               # exposes evaluate() and compare_reports()
│   │   └── <implementation>.py       # evaluation logic
│   └── ...
│
├── exp-<idea-name>/                   # one folder per experimental idea
│   ├── Makefile                       # REQUIRED: defines `build`, `run`, and `evaluate` targets
│   ├── <scripts>                      # all code needed to run this experiment (self-contained copies)
│   ├── config.yaml                    # (optional) experiment-specific settings
│   ├── pyproject.toml                 # (optional) if managed as a Python package via uv
│   ├── uv.lock                        # (optional) uv-generated pinned dependency versions
│   ├── research-note.md               # agent-generated: findings, analysis, conclusions
│   ├── <analysis-scripts>             # comparison plots, tables, etc. (if needed)
│   └── output/                        # all run outputs go here
│       ├── <run-name>/                # sub-folder per run (for multi-run experiments)
│       │   ├── run.log
│       │   ├── metrics.json
│       │   └── <artifacts>
│       └── ...
│
├── exp-<another-idea>/
│   └── ...
└── ...
```

---

## Key Principles

- **Makefile is the contract.** Every experiment folder **must** contain a `Makefile` with at least three targets: `build` (install dependencies, prepare data), `run` (execute the experiment), and `evaluate` (run evaluation using a shared evaluation protocol). This is the universal interface — anyone (human or agent) can reproduce the experiment by running `make build && make run && make evaluate` without needing to understand the internals. All arguments are naturally documented in Makefile targets and scripts.

- **Self-contained experiments.** Each experiment folder must contain all scripts needed to reproduce the experiment. Copy scripts into the folder — do not rely on git history, symlinks, or references to parent directories for code. Shared `data-protocols/`, shared `evaluation-protocols/`, and data locations referenced in `research-data.md` are the exceptions (use paths specified there).

- **Shared data protocols.** The `data-protocols/` folder holds one Python file per data protocol. Each file defines `get_train_data()`, `get_val_data()`, and `get_test_data()` functions that return data in whatever format suits the dataset. Different protocols for the same source (e.g., same images with different splits) are separate files. Both humans and agents can add new files when needed (use `data_protocol.template.py` as a starting point). Experiments import a protocol via `sys.path`; they do not duplicate data-loading logic.

- **Shared evaluation protocols.** The `evaluation-protocols/` folder holds reusable evaluation procedures that multiple experiments can reference. Each evaluation protocol takes `(dataset, predictions)` as input and generates an evaluation report. The protocol defines the expected format of both `dataset` and `predictions`. Each protocol also provides a `compare_reports(report_1, report_2, ...)` function to compare results across experiments. Both humans and agents can create new protocols when needed. This ensures consistent, comparable evaluation across experiments.

- **Protocol compatibility.** An evaluation protocol is typically associated with a data protocol — the evaluation protocol defines the expected format of `dataset` and `predictions`, and the caller is responsible for ensuring the data matches. When creating a new evaluation protocol, document which data protocols it is compatible with.

- **Protocol immutability.** Once a protocol has been used by any experiment, it must not be modified. If a bug is found, fix it and bump the version (folder suffix for evaluation protocols; user-managed for data protocol files). If it's a new approach, create a new file or folder with a new name. Experiments that used the old version continue to reference it unchanged — this preserves reproducibility.

- **Explicit protocol dependencies.** Each experiment must declare which data and evaluation protocols it depends on. These are naturally documented in the experiment's scripts (via imports) and Makefile targets.

- **Isolation.** Each experiment tests one idea. If you want to test two ideas, create two experiment folders.

- **Output separation.** Scripts and analysis code live in the experiment folder root. Run outputs (logs, checkpoints, metrics) go in `output/`. Never mix code and output.

---

## Naming Conventions

| Item | Pattern | Examples |
|------|---------|----------|
| Experiment folder | `exp-<idea-name>/` | `exp-lstm-baseline/`, `exp-attention-ablation/` |
| Data protocol file | `<descriptive_name>.py` (snake_case) | `imagenet_original_split.py`, `cifar10_stratified.py` |
| Evaluation protocol folder | `<descriptive_name>_v<N>/` (snake_case) | `imagenet_cls_v1/`, `bleu_eval_v1/` |

Use lowercase snake_case names for both data protocol files and evaluation protocol folders (both must be valid Python module names). The `_v<N>` suffix is **required** for evaluation protocols and starts at `v1`. Bump version only for bugfixes — new approaches get a new name.

---

## Protocol Structure

### Data Protocols

Each data protocol is a single `.py` file in `data-protocols/` that defines three functions:

```python
# data-protocols/imagenet_original_split.py

# Version: v1

def get_train_data():
    ...  # return format is flexible (list, DataFrame, Dataset, etc.)

def get_val_data():
    ...

def get_test_data():
    ...
```

Different protocols for the same source (e.g., different splits) are separate files. Use `data_protocol.template.py` as a starting point.

Experiments import a protocol via `sys.path`:
```python
import sys
sys.path.insert(0, "../../data-protocols")
from imagenet_original_split import get_train_data, get_val_data, get_test_data
```

### Evaluation Protocols

Each evaluation protocol is a folder containing a Python module with two required functions:

- **`evaluate(dataset, predictions) → report`** — scores predictions against the dataset and returns a structured report (e.g., dict, JSON-serializable object).
- **`compare_reports(report_1, report_2, ...) → comparison`** — compares reports from multiple experiments and returns a summary (e.g., ranked table, statistical tests, delta analysis).

The protocol defines the expected format of `dataset` and `predictions` in its README. An evaluation protocol is typically associated with a data protocol — the caller is responsible for ensuring the formats match.

```
evaluation-protocols/imagenet_cls_v1/
├── README.md              # purpose, dataset format, predictions format, report format
├── __init__.py            # exposes evaluate() and compare_reports()
├── evaluate.py            # implementation
└── references/            # (optional) reference data for evaluation
```

Folder names must be valid Python identifiers (snake_case) so they are directly importable. Use `evaluation-protocol-template/` (ImageNet classification example) as a starting point for new protocols.

Example usage from an experiment:
```python
import sys
sys.path.insert(0, "../../evaluation-protocols")
from imagenet_cls_v1 import evaluate, compare_reports

report = evaluate(dataset=test_data, predictions=model_outputs)
```

`compare_reports()` is typically called by the agent when comparing results across multiple experiments or runs:
```python
comparison = compare_reports(report_exp1, report_exp2, report_exp3)
```

### Protocol README

Each protocol's `README.md` must document:
- **Purpose**: What this protocol provides.
- **Interface**: Function signatures, expected inputs/outputs.
- **Dataset format**: What structure `dataset` must have (e.g., list of dicts with keys `"text"`, `"label"`).
- **Predictions format**: What structure `predictions` must have (e.g., list of strings, array of logits).
- **Report format**: What the returned report looks like (e.g., `{"bleu": 0.42, "brevity_penalty": 0.98}`).
- **Data details** (data protocols only): Source, size, format, preprocessing.
- **Versioning**: What version this is and what changed from prior versions (if any).

---

## Makefile Contract

The Makefile must define at least three targets:

- **`build`**: Install dependencies and prepare data — everything needed before the experiment can run.
- **`run`**: Execute the experiment (training, inference, etc.). Must be deterministic — running it again produces the same output.
- **`evaluate`**: Run evaluation using a shared evaluation protocol. Separated from `run` so that evaluation is consistent across experiments and can be re-run independently. The agent uses `compare_reports()` from the evaluation protocol when comparing results across multiple experiments or runs during analysis.

**Simple example** (scripts with inline dependencies, using shared protocols):
```makefile
build:
	pip install torch numpy

run:
	python train.py --config config.yaml --output-dir output/

evaluate:
	python run_eval.py --output output/eval_results.json
```

Where `run_eval.py` in the experiment folder calls the evaluation protocol:
```python
import sys
sys.path.insert(0, "../../data-protocols")
sys.path.insert(0, "../../evaluation-protocols")

from imagenet_original_split import get_test_data
from imagenet_cls_v1 import evaluate

dataset = get_test_data()
predictions = load_predictions("output/predictions.json")
report = evaluate(dataset=dataset, predictions=predictions)
save_json(report, "output/eval_results.json")
```

**Python package example** (using `uv` for dependency management):
```makefile
build:
	uv sync

run:
	uv run python train.py --config config.yaml --output-dir output/

evaluate:
	uv run python run_eval.py --output output/eval_results.json
```

---

## Multi-Run Experiments

For experiments with multiple runs (e.g., hyperparameter sweeps), each run must have its own Makefile target so that any researcher can inspect, rerun, or debug a single run independently. The default `run` target should execute all runs, but individual runs must also be invocable on their own.

Each run gets a sub-folder under `output/`. Example:

```makefile
RUNS := lr-0.001 lr-0.01 lr-0.1

run: $(RUNS)

lr-0.001:
	mkdir -p output/lr-0.001
	uv run python train.py --lr 0.001 --output-dir output/lr-0.001 2>&1 | tee output/lr-0.001/run.log

lr-0.01:
	mkdir -p output/lr-0.01
	uv run python train.py --lr 0.01 --output-dir output/lr-0.01 2>&1 | tee output/lr-0.01/run.log

lr-0.1:
	mkdir -p output/lr-0.1
	uv run python train.py --lr 0.1 --output-dir output/lr-0.1 2>&1 | tee output/lr-0.1/run.log

evaluate:
	@for run in $(RUNS); do \
		uv run python run_eval.py --predictions-dir output/$$run --output output/$$run/eval_results.json; \
	done
```

Resulting output structure:

```
output/
├── lr-0.001/
│   ├── run.log
│   ├── metrics.json
│   └── eval_results.json
├── lr-0.01/
│   ├── run.log
│   ├── metrics.json
│   └── eval_results.json
└── lr-0.1/
    ├── run.log
    ├── metrics.json
    └── eval_results.json
```
