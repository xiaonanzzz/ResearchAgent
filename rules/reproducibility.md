# Reproducibility

This rule defines the requirements for making experiments reproducible: seeding, dependency management, and script-based documentation of all arguments.

---

## Core Requirement

Running `make build && make run` in an experiment folder must produce the same output. Reproducibility is achieved by:

1. **Seeding all randomness** with fixed values.
2. **Pinning dependencies** via lock files or explicit versions.
3. **Documenting all arguments in Makefile targets and scripts** — every parameter is visible in the command that runs it. No separate fingerprinting needed.

---

## Seeding

All sources of randomness must be seeded with a fixed value. This includes:

- Python's `random` module
- NumPy's random number generator
- PyTorch (both CPU and CUDA)
- Any other library-specific RNG

Record the seed value in `config.yaml` or as a script argument so it can be verified and changed if needed.

---

## Dependency Management

Two supported workflows:

1. **`uv`-managed** (recommended for non-trivial dependencies): Set up the experiment as a `uv` project with `pyproject.toml` and `uv.lock`. The lock file pins exact versions. Use `uv sync` in `build` and `uv run` in `run`.

2. **pip-based**: Install dependencies directly in the `build` target with pinned versions (e.g., `pip install torch==2.1.0 numpy==1.26.2`).

If building on a prior experiment, copy its `pyproject.toml` and run `uv sync` to start from the same environment, then `uv add`/`uv remove` as needed.
