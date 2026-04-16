"""
ImageNet Classification Evaluation Protocol (v1)

Evaluates image classification predictions against ground-truth labels.
Computes top-1 accuracy, top-5 accuracy, and per-class accuracy.

Dataset format: list of {"image_path": str, "label": int}
Predictions format: list of {"label": int, "top5": [int, ...], "confidence": float}
"""

from collections import defaultdict


def evaluate(dataset, predictions):
    """Score predictions against the dataset.

    Args:
        dataset: list of dicts with keys "image_path", "label".
        predictions: list of dicts with keys "label", "top5", "confidence".
            Must be same length and order as dataset.

    Returns:
        Report dict with top1_accuracy, top5_accuracy, num_samples,
        and per_class_accuracy.
    """
    assert len(dataset) == len(predictions), (
        f"dataset ({len(dataset)}) and predictions ({len(predictions)}) length mismatch"
    )

    correct_top1 = 0
    correct_top5 = 0
    per_class_correct = defaultdict(int)
    per_class_total = defaultdict(int)

    for sample, pred in zip(dataset, predictions):
        gt_label = sample["label"]
        per_class_total[gt_label] += 1

        if pred["label"] == gt_label:
            correct_top1 += 1

        if gt_label in pred["top5"]:
            correct_top5 += 1
            per_class_correct[gt_label] += 1

    n = len(dataset)
    per_class_accuracy = {
        cls: per_class_correct[cls] / per_class_total[cls]
        for cls in sorted(per_class_total)
    }

    return {
        "top1_accuracy": correct_top1 / n if n > 0 else 0.0,
        "top5_accuracy": correct_top5 / n if n > 0 else 0.0,
        "num_samples": n,
        "per_class_accuracy": per_class_accuracy,
    }


def compare_reports(*reports):
    """Compare evaluation reports from multiple experiments or runs.

    Args:
        *reports: Two or more report dicts (as returned by evaluate()).
            Each report may optionally include an "experiment" key for labeling.

    Returns:
        Comparison dict with ranked results and deltas.
    """
    entries = []
    for i, report in enumerate(reports):
        entries.append({
            "experiment": report.get("experiment", f"exp_{i}"),
            "top1_accuracy": report["top1_accuracy"],
            "top5_accuracy": report["top5_accuracy"],
            "num_samples": report["num_samples"],
        })

    # Rank by top-1 accuracy descending
    ranked = sorted(entries, key=lambda x: x["top1_accuracy"], reverse=True)

    best = ranked[0]["top1_accuracy"]
    for entry in ranked:
        entry["delta_from_best"] = entry["top1_accuracy"] - best

    return {
        "ranked": ranked,
        "best_experiment": ranked[0]["experiment"],
        "best_top1_accuracy": best,
    }
