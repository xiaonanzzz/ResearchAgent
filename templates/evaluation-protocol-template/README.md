# imagenet_cls_v1

## Purpose

Evaluation protocol for ImageNet image classification. Computes top-1 accuracy, top-5 accuracy, and per-class accuracy.

## Compatible Data Protocols

- `imagenet_original_split.py` (or any data protocol returning the same format)

## Dataset Format

A list of dicts, each with:
```python
{"image_path": str, "label": int}  # label is class index in [0, 999]
```

## Predictions Format

A list of dicts aligned with the dataset (same length, same order), each with:
```python
{"label": int, "top5": [int, int, int, int, int], "confidence": float}
```

## Report Format

```python
{
    "top1_accuracy": float,       # e.g., 0.761
    "top5_accuracy": float,       # e.g., 0.929
    "num_samples": int,
    "per_class_accuracy": {int: float},  # class_index → accuracy
}
```

## Version History

- **v1**: Initial version. Top-1, top-5, per-class accuracy.
