"""
Data Protocol: <protocol-name>

<Describe what this protocol provides: dataset source, split strategy, preprocessing, etc.>

Usage from an experiment:
    import sys
    sys.path.insert(0, "../../data-protocols")
    from <this_file> import get_train_data, get_val_data, get_test_data
"""

# Version: v1
# Do not modify after use by any experiment. Bugfix → bump version. New approach → new file.


def get_train_data():
    """Return the training split."""
    raise NotImplementedError


def get_val_data():
    """Return the validation split."""
    raise NotImplementedError


def get_test_data():
    """Return the test split."""
    raise NotImplementedError
