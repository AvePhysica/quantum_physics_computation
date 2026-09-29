"""Plotting helpers for the homework outputs."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping, Sequence

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def _prepare_destination(destination: str | Path) -> Path:
    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def plot_stacked_dos(
    omega_shifted: np.ndarray,
    curves: Mapping[float, np.ndarray],
    destination: str | Path,
) -> None:
    """Plot equal-scale DOS curves with vertical offsets, smallest U on top."""

    if not curves:
        raise ValueError("at least one DOS curve is required")
    omega = np.asarray(omega_shifted, dtype=float)
    ordered = sorted(curves.items())
    global_peak = max(float(np.max(np.asarray(curve))) for _, curve in ordered)
    if global_peak <= 0:
        raise ValueError("DOS curves must have positive spectral weight")
    spacing = 1.25 * global_peak

    fig, ax = plt.subplots(figsize=(8.4, 6.0), constrained_layout=True)
    line_styles = ["-", "--", ":", (0, (1, 1)), "-.", (0, (5, 1, 1, 1))]
    for index, (interaction, curve) in enumerate(ordered):
        values = np.asarray(curve, dtype=float)
        if values.shape != omega.shape:
            raise ValueError("every DOS curve must match the omega grid")
        offset = (len(ordered) - index - 1) * spacing
        ax.plot(
            omega,
            values + offset,
            color="black",
            linewidth=1.45,
            linestyle=line_styles[index % len(line_styles)],
            label=fr"$U={interaction:g}$",
        )
        ax.axhline(offset, color="0.82", linewidth=0.55, zorder=0)

    ax.axvline(0.0, color="#9b1c31", linewidth=0.9, alpha=0.7)
    ax.set_xlabel(r"$\omega-\mu$")
    ax.set_ylabel(r"DOS $\rho(\omega-\mu)$ (vertically shifted)")
    ax.set_yticks([])
    ax.legend(frameon=False, ncol=2, loc="upper right")
    ax.set_title("Half-filled 1D Hubbard ring: interaction-driven spectral evolution")
    fig.savefig(_prepare_destination(destination), dpi=240)
    plt.close(fig)


def plot_rho_zero_ratio(
    interactions: Sequence[float],
    ratios: Sequence[float],
    destination: str | Path,
) -> None:
    """Plot the normalized Fermi-level DOS versus interaction strength."""

    u_values = np.asarray(interactions, dtype=float)
    ratio_values = np.asarray(ratios, dtype=float)
    if u_values.shape != ratio_values.shape or u_values.ndim != 1:
        raise ValueError("interactions and ratios must be same-length vectors")
    fig, ax = plt.subplots(figsize=(6.4, 4.2), constrained_layout=True)
    ax.plot(u_values, ratio_values, "o-", color="#325d9b", linewidth=1.7)
    ax.set_xlabel(r"$U/t$")
    ax.set_ylabel(r"$\rho(0)/\rho_{\max}$")
    ax.set_ylim(bottom=0)
    ax.grid(alpha=0.25)
    ax.set_title("Suppression of spectral weight at the chemical potential")
    fig.savefig(_prepare_destination(destination), dpi=240)
    plt.close(fig)


def plot_hubbard_band_schematic(destination: str | Path) -> None:
    """Draw a clearly labeled conceptual metal/Mott-insulator DOS schematic."""

    fig, axes = plt.subplots(1, 2, figsize=(8.2, 4.7), constrained_layout=True)

    energy = np.linspace(-1.0, 1.0, 401)
    metallic_dos = np.sqrt(np.clip(1.0 - energy**2, 0.0, None))
    ax = axes[0]
    ax.plot(metallic_dos, energy, color="black", linewidth=1.6)
    occupied = energy <= 0
    ax.fill_betweenx(
        energy[occupied], 0.0, metallic_dos[occupied], color="#6867d9", alpha=0.86
    )
    ax.axhline(0.0, color="black", linestyle="--", linewidth=1.0)
    ax.text(-0.04, 0.0, r"$E_F$", ha="right", va="center")
    ax.text(0.92, 0.88, r"$U=0$", ha="right")
    ax.set_title("Metal: one band crosses $E_F$")

    lower_energy = np.linspace(-1.65, -0.55, 241)
    upper_energy = np.linspace(0.55, 1.65, 241)
    lower_dos = np.sqrt(np.clip(1.0 - ((lower_energy + 1.1) / 0.55) ** 2, 0.0, None))
    upper_dos = np.sqrt(np.clip(1.0 - ((upper_energy - 1.1) / 0.55) ** 2, 0.0, None))
    ax = axes[1]
    ax.plot(lower_dos, lower_energy, color="black", linewidth=1.6)
    ax.plot(upper_dos, upper_energy, color="black", linewidth=1.6)
    ax.fill_betweenx(lower_energy, 0.0, lower_dos, color="#6867d9", alpha=0.86)
    ax.axhline(0.0, color="black", linestyle="--", linewidth=1.0)
    ax.annotate(
        "Mott gap",
        xy=(0.72, 0.5),
        xytext=(0.72, -0.5),
        arrowprops={"arrowstyle": "<->", "color": "#9b1c31"},
        ha="center",
        va="center",
        color="#9b1c31",
    )
    ax.text(-0.04, 0.0, r"$E_F$", ha="right", va="center")
    ax.text(0.92, 1.48, r"$U\gtrsim W$", ha="right")
    ax.set_title("Mott insulator: lower and upper Hubbard bands")

    for ax in axes:
        ax.set_xlabel("DOS (schematic)")
        ax.set_ylabel("Energy")
        ax.set_xlim(-0.16, 1.08)
        ax.spines[["top", "right"]].set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])
    fig.suptitle("Conceptual Hubbard-band splitting (not numerical data)")
    fig.savefig(_prepare_destination(destination), dpi=240)
    plt.close(fig)


def plot_u0_benchmark(
    omega_shifted: np.ndarray,
    numerical: np.ndarray,
    analytical: np.ndarray,
    destination: str | Path,
) -> None:
    """Overlay the numerical and exact free-fermion spectra."""

    fig, (upper, lower) = plt.subplots(
        2,
        1,
        figsize=(7.5, 6.0),
        sharex=True,
        gridspec_kw={"height_ratios": [3, 1]},
        constrained_layout=True,
    )
    upper.plot(omega_shifted, analytical, color="black", linewidth=2.0, label="analytic")
    upper.plot(
        omega_shifted,
        numerical,
        color="#b13c3c",
        linestyle="--",
        linewidth=1.2,
        label="Lanczos + continued fraction",
    )
    upper.set_ylabel(r"$\rho(\omega)$")
    upper.legend(frameon=False)
    upper.set_title(r"$U=0$ analytical benchmark")
    lower.plot(omega_shifted, numerical - analytical, color="#325d9b")
    lower.axhline(0.0, color="black", linewidth=0.7)
    lower.set_xlabel(r"$\omega-\mu$")
    lower.set_ylabel("difference")
    fig.savefig(_prepare_destination(destination), dpi=240)
    plt.close(fig)


def plot_ritz_convergence(
    steps: np.ndarray,
    ritz_values: np.ndarray,
    exact_ground_energy: float,
    destination: str | Path,
) -> None:
    """Plot the lowest Ritz value and its error against Krylov dimension."""

    fig, (upper, lower) = plt.subplots(
        2,
        1,
        figsize=(7.2, 6.0),
        sharex=True,
        gridspec_kw={"height_ratios": [2, 1]},
        constrained_layout=True,
    )
    upper.plot(steps, ritz_values, color="#325d9b")
    upper.axhline(exact_ground_energy, color="#9b1c31", linestyle="--", label=r"$E_0$")
    upper.set_ylabel("lowest Ritz value")
    upper.legend(frameon=False)
    error = np.maximum(ritz_values - exact_ground_energy, np.finfo(float).tiny)
    lower.semilogy(steps, error, color="#325d9b")
    lower.set_xlabel("Krylov dimension $L$")
    lower.set_ylabel(r"$E_\mathrm{Ritz}-E_0$")
    fig.savefig(_prepare_destination(destination), dpi=240)
    plt.close(fig)

