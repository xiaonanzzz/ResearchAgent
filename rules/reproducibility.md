# Reproducibility

This rule defines the requirements for making experiments reproducible: fingerprinting, seeding, drift detection, and environment tracking.

---

## Core Requirement

Running `make run` in an experiment folder must produce the same output. All randomness should be seeded. `make build` generates a `fingerprint.json` that snapshots all external dependencies (data, models, system) so drift can be detected later.

---

## fingerprint.json

`fingerprint.json` is generated as the **final step of `make build`**. It is a snapshot of everything external the experiment depends on — data, models, and the system environment. It is not a dependency manager (that's what `uv.lock` or `requirements.txt` is for). Its purpose is **drift detection**: if someone runs `make build` again later or on a different machine, they can compare the new fingerprint against the recorded one to see if anything changed that could affect reproducibility.

### What to Capture

- **Datasets**: file path, SHA-256 checksum, file count, total size.
- **Models / pretrained weights**: file path, SHA-256 checksum, source URL if applicable.
- **System environment**: Python version, CUDA version, GPU model, driver version — anything that could affect numerics or behavior.
- **Packages** (only if not using `uv.lock` or another package lock file): pinned versions of installed packages.

### Example

```json
{
  "created": "2025-03-24T10:30:00Z",
  "datasets": [
    {
      "name": "imagenet-1k-train",
      "path": "/data/imagenet/train",
      "sha256": "a1b2c3...",
      "num_files": 1281167,
      "size_bytes": 147897321472
    }
  ],
  "models": [
    {
      "name": "vit-base-patch16-224",
      "path": "/models/vit-base/pytorch_model.bin",
      "sha256": "d4e5f6...",
      "source": "https://huggingface.co/google/vit-base-patch16-224"
    }
  ],
  "system": {
    "python": "3.11.7",
    "cuda": "12.1",
    "cuda_driver": "535.129.03",
    "gpu": "NVIDIA A100 80GB"
  }
}
```

### Large Datasets

For very large datasets where computing a full checksum is impractical, record a partial signature instead: checksum of the first N files, total file count, total size, and a directory listing hash. Document which approach was used.

---

## Seeding

All sources of randomness must be seeded with a fixed value. This includes:

- Python's `random` module
- NumPy's random number generator
- PyTorch (both CPU and CUDA)
- Any other library-specific RNG

Record the seed value in `config.yaml` or as a script argument so it can be verified and changed if needed.

---

## Fingerprint Generation

Write a `generate_fingerprint.py` (or equivalent script) in the experiment folder to automate fingerprint creation. The `build` target calls it as its last step. See `templates/generate_fingerprint.py` for a reusable starting point.

---

## Dependency Management

Two supported workflows:

1. **`uv`-managed** (recommended for non-trivial dependencies): Set up the experiment as a `uv` project with `pyproject.toml` and `uv.lock`. The lock file pins exact versions. Use `uv sync` in `build` and `uv run` in `run`.

2. **pip-based**: Install dependencies directly in the `build` target. In this case, `fingerprint.json` should include pinned package versions since there is no lock file.

If building on a prior experiment, copy its `pyproject.toml` and run `uv sync` to start from the same environment, then `uv add`/`uv remove` as needed.
