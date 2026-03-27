#!/usr/bin/env python3
"""Generate fingerprint.json for experiment reproducibility.

This script auto-detects datasets, system environment (Python, CUDA, GPU),
and writes a fingerprint.json file for drift detection.

Usage:
    python generate_fingerprint.py [--data-dirs DIR [DIR ...]] [--model-files FILE [FILE ...]]

If no arguments are given, the script records only the system environment.
"""

import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def sha256_file(path: str, max_bytes: int | None = None) -> str:
    """Compute SHA-256 of a file. If max_bytes is set, hash only the first N bytes."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        if max_bytes is not None:
            h.update(f.read(max_bytes))
        else:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
    return h.hexdigest()


def dir_stats(path: str) -> dict:
    """Compute stats for a directory: file count, total size, and a listing hash."""
    total_size = 0
    file_count = 0
    listing = []
    for root, _dirs, files in os.walk(path):
        for fname in sorted(files):
            fpath = os.path.join(root, fname)
            try:
                st = os.stat(fpath)
                total_size += st.st_size
                file_count += 1
                listing.append(f"{os.path.relpath(fpath, path)}:{st.st_size}")
            except OSError:
                continue
    listing_hash = hashlib.sha256("\n".join(listing).encode()).hexdigest()
    return {
        "num_files": file_count,
        "size_bytes": total_size,
        "listing_hash": listing_hash,
    }


def fingerprint_dataset(path: str) -> dict:
    """Generate fingerprint entry for a dataset directory."""
    p = Path(path).resolve()
    entry = {
        "name": p.name,
        "path": str(p),
    }
    if p.is_file():
        entry["sha256"] = sha256_file(str(p))
        entry["size_bytes"] = p.stat().st_size
    elif p.is_dir():
        stats = dir_stats(str(p))
        entry.update(stats)
        entry["note"] = "directory listing hash (full file checksums not computed)"
    return entry


def fingerprint_model(path: str) -> dict:
    """Generate fingerprint entry for a model file."""
    p = Path(path).resolve()
    entry = {
        "name": p.name,
        "path": str(p),
    }
    if p.is_file():
        size = p.stat().st_size
        entry["size_bytes"] = size
        # For very large files (>1GB), hash only the first 100MB
        if size > 1_000_000_000:
            entry["sha256_partial"] = sha256_file(str(p), max_bytes=100_000_000)
            entry["note"] = "partial hash (first 100MB)"
        else:
            entry["sha256"] = sha256_file(str(p))
    return entry


def get_system_info() -> dict:
    """Collect system environment information."""
    info = {
        "python": platform.python_version(),
        "platform": platform.platform(),
    }

    # CUDA version
    try:
        result = subprocess.run(
            ["nvcc", "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            for line in result.stdout.split("\n"):
                if "release" in line.lower():
                    # e.g., "Cuda compilation tools, release 12.1, V12.1.105"
                    parts = line.split("release")[-1].strip().split(",")
                    info["cuda"] = parts[0].strip()
                    break
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    # GPU info
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,driver_version,memory.total", "--format=csv,noheader"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            line = result.stdout.strip().split("\n")[0]
            parts = [p.strip() for p in line.split(",")]
            if len(parts) >= 3:
                info["gpu"] = parts[0]
                info["cuda_driver"] = parts[1]
                info["gpu_memory"] = parts[2]
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    return info


def main():
    parser = argparse.ArgumentParser(description="Generate fingerprint.json")
    parser.add_argument(
        "--data-dirs",
        nargs="*",
        default=[],
        help="Paths to dataset directories or files to fingerprint",
    )
    parser.add_argument(
        "--model-files",
        nargs="*",
        default=[],
        help="Paths to model weight files to fingerprint",
    )
    parser.add_argument(
        "--output",
        default="fingerprint.json",
        help="Output file path (default: fingerprint.json)",
    )
    args = parser.parse_args()

    fingerprint = {
        "created": datetime.now(timezone.utc).isoformat(),
        "datasets": [fingerprint_dataset(d) for d in args.data_dirs],
        "models": [fingerprint_model(m) for m in args.model_files],
        "system": get_system_info(),
    }

    with open(args.output, "w") as f:
        json.dump(fingerprint, f, indent=2)

    print(f"Fingerprint written to {args.output}")


if __name__ == "__main__":
    main()
