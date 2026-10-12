"""Publication-style plotting helpers."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def _prepare(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.style.use("seaborn-v0_8-whitegrid")


def plot_dispersion(tables: dict[str, list[dict]], path: Path) -> None:
    _prepare(path)
    fig, ax = plt.subplots(figsize=(7.0, 4.4))
    for label, rows in tables.items():
        x = [row["k_over_pi"] for row in rows]
        y = [row["energy"] for row in rows]
        ax.plot(x, y, marker="o", linewidth=1.7, label=label)
    ax.set_xlabel(r"$k/\pi$")
    ax.set_ylabel(r"lowest energy $E_0(k)$")
    ax.set_title("N=16 momentum-resolved lowest spectrum")
    ax.legend(frameon=True)
    fig.tight_layout()
    fig.savefig(path, dpi=220)
    plt.close(fig)


def plot_magnetization(data: dict[str, tuple[np.ndarray, np.ndarray]], path: Path) -> None:
    _prepare(path)
    fig, ax = plt.subplots(figsize=(7.0, 4.4))
    for label, (fields, magnetization) in data.items():
        ax.step(fields, magnetization, where="post", linewidth=1.8, label=label)
    ax.set_xlabel(r"field $h/J_1$")
    ax.set_ylabel(r"magnetization density $m=S^z_{\rm tot}/N$")
    ax.set_title("N=16 zero-temperature magnetization")
    ax.legend(frameon=True)
    fig.tight_layout()
    fig.savefig(path, dpi=220)
    plt.close(fig)


def plot_j2_scan(rows: list[dict], path: Path) -> None:
    _prepare(path)
    fig, ax = plt.subplots(figsize=(7.0, 4.4))
    x = [row["j2"] for row in rows]
    y = [row["energy_per_site"] for row in rows]
    ax.plot(x, y, marker="o", linewidth=1.8)
    for row in rows:
        ax.annotate(row["ground_momenta"], (row["j2"], row["energy_per_site"]), xytext=(0, 7), textcoords="offset points", ha="center", fontsize=7)
    ax.set_xlabel(r"$J_2/J_1$")
    ax.set_ylabel(r"$E_0/N$")
    ax.set_title(r"N=16 frustration scan (labels: ground $m_k$)")
    fig.tight_layout()
    fig.savefig(path, dpi=220)
    plt.close(fig)


def plot_structure_factor(data: dict[str, np.ndarray], path: Path) -> None:
    _prepare(path)
    fig, ax = plt.subplots(figsize=(7.0, 4.4))
    for label, values in data.items():
        n_sites = len(values)
        momenta = 2.0 * np.arange(n_sites) / n_sites
        ax.plot(momenta, values, marker="o", linewidth=1.7, label=label)
    ax.set_xlabel(r"$q/\pi$")
    ax.set_ylabel(r"$S(q)=N^{-1}\sum_r e^{-iqr}C(r)$")
    ax.set_title("N=16 spin structure factor")
    ax.legend(frameon=True)
    fig.tight_layout()
    fig.savefig(path, dpi=220)
    plt.close(fig)

