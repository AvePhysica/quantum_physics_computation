from __future__ import annotations

from run_homework3 import _degeneracy_weight_summary


def test_degeneracy_summary_keeps_raw_weights_and_maximum_deviation() -> None:
    summary = _degeneracy_weight_summary(
        full_addition=8.0,
        full_removal=8.0,
        shortcut_addition=6.0,
        shortcut_removal=10.0,
    )

    assert summary == {
        "full_addition_weight": 8.0,
        "shortcut_addition_weight": 6.0,
        "full_removal_weight": 8.0,
        "shortcut_removal_weight": 10.0,
        "shortcut_max_deviation_from_exact_pair": 2.0,
    }
