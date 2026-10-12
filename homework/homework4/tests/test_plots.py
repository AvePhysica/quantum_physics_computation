from pathlib import Path

import numpy as np

from plots import plot_dispersion, plot_j2_scan, plot_magnetization, plot_structure_factor


def test_all_plot_writers_create_nonempty_pngs(tmp_path: Path):
    dispersion = {
        "J2=0": [{"k_over_pi": 0.0, "energy": -1.0}, {"k_over_pi": 1.0, "energy": -2.0}]
    }
    magnetization = {"J2=0": (np.array([0.0, 1.0]), np.array([0.0, 0.5]))}
    scan = [{"j2": 0.0, "energy_per_site": -0.4, "ground_momenta": "0"}]
    structure = {"J2=0": np.array([0.0, 1.0, 0.2, 1.0])}
    writers = [
        (plot_dispersion, (dispersion, tmp_path / "dispersion.png")),
        (plot_magnetization, (magnetization, tmp_path / "magnetization.png")),
        (plot_j2_scan, (scan, tmp_path / "scan.png")),
        (plot_structure_factor, (structure, tmp_path / "structure.png")),
    ]
    for writer, arguments in writers:
        writer(*arguments)
        assert arguments[-1].is_file()
        assert arguments[-1].stat().st_size > 1000
