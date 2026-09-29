from __future__ import annotations

import numpy as np

from plots import (
    plot_hubbard_band_schematic,
    plot_rho_zero_ratio,
    plot_stacked_dos,
)


def test_stacked_dos_plot_is_written(tmp_path) -> None:
    omega = np.linspace(-3.0, 3.0, 51)
    curves = {
        0.0: np.exp(-omega**2),
        2.0: np.exp(-(omega - 1.0) ** 2) + np.exp(-(omega + 1.0) ** 2),
    }
    destination = tmp_path / "stacked.png"
    plot_stacked_dos(omega, curves, destination)
    assert destination.stat().st_size > 1_000


def test_ratio_plot_and_conceptual_schematic_are_written(tmp_path) -> None:
    ratio_path = tmp_path / "ratio.png"
    schematic_path = tmp_path / "schematic.png"
    plot_rho_zero_ratio([0, 2, 4], [1.0, 0.4, 0.05], ratio_path)
    plot_hubbard_band_schematic(schematic_path)
    assert ratio_path.stat().st_size > 1_000
    assert schematic_path.stat().st_size > 1_000

