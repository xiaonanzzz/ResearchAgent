# ResearchAgent

A reusable skills and rules toolkit for autonomous research agents. Initialize a new research project, describe your objective and data, and let the agent run experiments autonomously.

## Quick Start

1. **Initialize** a new research project:

   ```bash
   make init research-image-classification
   cd research-image-classification/
   ```

   This creates the project structure with skills, rules, data/evaluation protocol directories, and template files.

2. **Describe your research** — edit the two human-maintained files:

   - `research-objective.md` — What problem you're solving, primary metric, resources, constraints
   - `research-data.md` — What datasets you have, where they are, their format

3. **Start researching** — invoke the `auto-experiment` skill. The agent reads your objective and data descriptions, creates experiment folders, runs experiments, and iterates autonomously. When it finds interesting observations, it may ask if you want to add new data or try a different evaluation protocol.

## Project Structure (after `make init`)

```
research-xxx/
├── research-objective.md        # human-written: problem, goal, metric, resources
├── research-data.md             # human-written: datasets, locations, formats
├── data-protocols/              # shared data definitions (one .py per protocol)
├── evaluation-protocols/        # shared evaluation procedures (one folder per protocol)
│
├── .claude/
│   ├── commands/                # skills (copied from ResearchAgent)
│   │   ├── auto-experiment.md
│   │   └── paper-reviewer.md
│   └── rules/                   # rules (copied from ResearchAgent)
│       ├── research-repo-management-rule.md
│       ├── reproducibility.md
│       ├── documentation.md
│       └── resource-discipline.md
│
├── exp-<idea-name>/             # created by agent during experimentation
│   └── ...
└── research-note-all-in-one.md  # created by agent: running lab notebook
```

## Toolkit Structure

```
ResearchAgent/
├── README.md                    # This file
├── VERSION                      # Current version
├── Makefile                     # init target for new projects
│
├── rules/                       # Cross-cutting principles
│   ├── research-repo-management-rule.md  # Directory layout, protocols, Makefile contract
│   ├── reproducibility.md       # Seeding, dependency management
│   ├── documentation.md         # Research notes, metrics.tsv conventions
│   └── resource-discipline.md   # Time, memory, disk budgets & guidelines
│
├── skills/                      # Modular agent workflows
│   ├── auto-experiment.md       # Autonomous experiment loop
│   └── paper-reviewer.md        # ML paper review
│
└── templates/                   # Starter files copied during init
    ├── research-objective.template.md
    ├── research-data.template.md
    ├── data_protocol.template.py
    ├── evaluation-protocol-template/
    ├── Makefile.template
    ├── config.template.yaml
    ├── research-note.template.md
    └── research-note-all-in-one.template.md
```

## Adding a New Skill

1. Create a new markdown file in `skills/` (e.g., `skills/literature-review.md`).
2. Write the skill as a self-contained instruction document the agent can follow.
3. Reference `rules/` files for cross-cutting concerns instead of duplicating content.

## Adding a New Rule

1. Create a new markdown file in `rules/` (e.g., `rules/safety.md`).
2. Define the rule clearly with examples where helpful.
3. Update existing skills to reference the new rule where applicable.
