# ResearchAgent

A reusable skills and rules toolkit for autonomous research agents. Copy this repo to start a new research project, point your agent at the skills and rules, and let it run experiments autonomously.

## Quick Start

1. **Copy** this repo to a new project directory:

   ```bash
   cp -r ResearchAgent/ my-new-research/
   cd my-new-research/
   ```

2. **Customize** the project README:

   ```bash
   cp templates/project-readme.md README.md
   # Edit README.md with your research goal, metrics, data locations, etc.
   ```

3. **Run** your agent, pointing it at the relevant skill:

   The agent reads `skills/auto-experiment.md` as its instruction manual and uses `rules/` for cross-cutting principles. It will create experiment folders at the project root, run experiments, and iterate autonomously.

## Repo Structure

```
ResearchAgent/
├── README.md                 # This file
├── CHANGELOG.md              # Version history
├── VERSION                   # Current version
│
├── rules/                    # Cross-cutting principles (all skills follow these)
│   ├── project-structure.md  # Research directory layout & organization
│   ├── reproducibility.md    # Fingerprinting, seeding, environment tracking
│   ├── documentation.md      # Research notes, metrics.tsv conventions
│   └── resource-discipline.md# Time, memory, disk budgets & guidelines
│
├── skills/                   # Modular agent workflows
│   └── auto-experiment.md    # Autonomous experiment loop
│
├── templates/                # Starter files for new projects
│   ├── project-readme.md     # Template README for a research project
│   ├── Makefile.template     # Template Makefile for an experiment folder
│   ├── generate_fingerprint.py  # Reusable fingerprint generation script
│   ├── config.template.yaml  # Template experiment config
│   ├── research-note.template.md        # Per-experiment research note template
│   └── research-note-all-in-one.template.md  # Root research log template
│
└── .claude/
    └── settings.local.json   # Agent settings
```

### rules/

Cross-cutting principles that apply to all skills. These define the standards for project layout, reproducibility, documentation, and resource management. Every skill references these rules rather than duplicating the content.

### skills/

Modular agent workflows. Each skill is a self-contained instruction document that tells the agent how to perform a specific type of research activity. Currently includes:

- **`auto-experiment.md`** — Autonomous experiment loop: generate ideas, run experiments, analyze results, iterate.

### templates/

Starter files that get copied into new research projects. These provide the scaffolding for experiment folders and project-level documentation.

## Adding a New Skill

1. Create a new markdown file in `skills/` (e.g., `skills/literature-review.md`).
2. Write the skill as a self-contained instruction document the agent can follow.
3. Reference `rules/` files for cross-cutting concerns instead of duplicating content.
4. Add a brief description to this README under the `skills/` section.

## Adding a New Rule

1. Create a new markdown file in `rules/` (e.g., `rules/safety.md`).
2. Define the rule clearly with examples where helpful.
3. Update existing skills to reference the new rule where applicable.
4. Add a brief description to this README under the `rules/` section.
