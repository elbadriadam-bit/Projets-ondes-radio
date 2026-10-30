#!/usr/bin/env python3
"""Simulation de propagation radio urbaine sous pluie et humidité.

Ce script reproduit les principales hypothèses et formules visibles dans le
simulateur HTML du dépôt :
- pertes en espace libre (Friis),
- pertes urbaines simplifiées UIT-R P.1411,
- atténuation due à la pluie (UIT-R P.838-3, approximation pédagogique),
- atténuation due aux gaz atmosphériques (UIT-R P.676-13, approximation),
- calcul du SNR à partir de la puissance reçue et du bruit thermique.

Le programme est volontairement documenté pour servir de base à un mini-projet
ou à une validation numérique simple.
"""

from __future__ import annotations

import os
from typing import Dict, Iterable, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def calc_fspl(distance_km: float, freq_ghz: float) -> float:
    """Perte de propagation en espace libre, formule de Friis (dB)."""
    if distance_km <= 0:
        return 0.0
    freq_mhz = freq_ghz * 1000.0
    return 20 * np.log10(distance_km) + 20 * np.log10(freq_mhz) + 32.44


def calc_path_loss(distance_km: float, freq_ghz: float, model: str = "uit_1411_los") -> float:
    """Approximation simplifiée de propagation urbaine inspirée de l'UIT-R P.1411."""
    fspl = calc_fspl(distance_km, freq_ghz)

    if model == "free_space":
        return fspl

    if model == "uit_1411_los":
        add_loss = 6 + 10 * np.log10(distance_km) + 0.5 * freq_ghz
        return fspl + max(2.0, add_loss)

    if model == "uit_1411_nlos":
        return fspl + 25 + 15 * np.log10(distance_km) + 5 * np.log10(freq_ghz)

    raise ValueError(f"Modèle inconnu : {model}")


def calc_polarization_term(freq_ghz: float, a: Iterable[float], b: Iterable[float], c: Iterable[float], m: float, offset: float) -> float:
    """Termes de type gaussien utilisés pour approximer les coefficients P.838-3."""
    logf = np.log10(freq_ghz)
    resonance = sum(av * np.exp(-((logf - bv) / cv) ** 2) for av, bv, cv in zip(a, b, c))
    return resonance + m * logf + offset


def calc_rain_coefficients(freq_ghz: float, polarization: str) -> Dict[str, float]:
    """Approximation des coefficients k et alpha de l'UIT-R P.838-3."""
    horizontal_k = np.power(10, calc_polarization_term(
        freq_ghz,
        a=[-5.33980, -0.35351, -0.23789, -0.94158],
        b=[-0.10008, 1.26970, 0.86036, 0.64552],
        c=[1.13098, 0.45400, 0.15354, 0.16817],
        m=-0.18961,
        offset=0.71147,
    ))

    vertical_k = np.power(10, calc_polarization_term(
        freq_ghz,
        a=[-3.80595, -3.44965, -0.39902, 0.50167],
        b=[0.56934, -0.22911, 0.73042, 1.07319],
        c=[0.81061, 0.51059, 0.11899, 0.27195],
        m=-0.16398,
        offset=0.63297,
    ))

    horizontal_alpha = calc_polarization_term(
        freq_ghz,
        a=[-0.14318, 0.29591, 0.32177, -5.37610, 16.1721],
        b=[1.82442, 0.77564, 0.63773, -0.96230, -3.29980],
        c=[-0.55187, 0.19822, 0.13164, 1.47828, 3.43990],
        m=0.67849,
        offset=-1.95537,
    )

    vertical_alpha = calc_polarization_term(
        freq_ghz,
        a=[-0.07771, 0.56727, -0.20238, -48.2991, 48.5833],
        b=[2.33840, 0.95545, 1.14520, 0.791669, 0.791459],
        c=[-0.76284, 0.54039, 0.26809, -5.7416, -5.7416],
        m=-0.053739,
        offset=0.83433,
    )

    if polarization == "H":
        return {"k": float(horizontal_k), "alpha": float(horizontal_alpha)}
    if polarization == "V":
        return {"k": float(vertical_k), "alpha": float(vertical_alpha)}

    # Cas circulaire : moyenne des coefficients horizontaux et verticaux.
    k_circ = (horizontal_k + vertical_k) / 2.0
    alpha_circ = (horizontal_k * horizontal_alpha + vertical_k * vertical_alpha) / (2.0 * k_circ)
    return {"k": float(k_circ), "alpha": float(alpha_circ)}


def calc_rain_gamma(freq_ghz: float, rain_rate_mm_h: float, polarization: str = "C") -> float:
    """Atténuation spécifique de pluie gamma_R (dB/km) selon l'approximation P.838-3."""
    if rain_rate_mm_h <= 0:
        return 0.0
    coeff = calc_rain_coefficients(freq_ghz, polarization)
    return coeff["k"] * np.power(rain_rate_mm_h, coeff["alpha"])


def calc_vapor_density(relative_humidity_pct: float, temperature_c: float) -> float:
    """Densité de vapeur en g/m³, approximation pédagogique inspirée de la formule P.676."""
    temp_k = temperature_c + 273.15
    saturation_pressure = 6.1121 * np.exp((18.678 - temperature_c / 234.5) * (temperature_c / (257.14 + temperature_c)))
    return 216.7 * (relative_humidity_pct / 100.0) * saturation_pressure / temp_k


def calc_gas_components(freq_ghz: float, humidity_pct: float, temperature_c: float) -> Dict[str, float]:
    """Approximation des contributions des gaz et de la vapeur d'eau."""
    vapor_density = calc_vapor_density(humidity_pct, temperature_c)

    dry_continuum = 0.00005 * freq_ghz * freq_ghz / (1 + (freq_ghz / 60.0) ** 2)
    oxygen_band = 14.8 / (1 + ((freq_ghz - 60.0) / 7.0) ** 2)
    vapor_continuum = 0.00012 * vapor_density * (freq_ghz / 10.0) ** 2
    vapor_line = 0.2 * (vapor_density / 7.5) / (1 + ((freq_ghz - 22.235) / 2.5) ** 2)

    return {
        "oxygen": dry_continuum + oxygen_band,
        "vapor": vapor_continuum + vapor_line,
    }


def calc_gas_gamma(freq_ghz: float, humidity_pct: float, temperature_c: float) -> float:
    """Atténuation atmosphérique totale due à l'oxygène et à la vapeur d'eau."""
    components = calc_gas_components(freq_ghz, humidity_pct, temperature_c)
    return components["oxygen"] + components["vapor"]


def calc_noise_floor(bw_mhz: float, nf_db: float) -> float:
    """Bruit thermique à l'entrée du récepteur (dBm)."""
    bw_hz = bw_mhz * 1e6
    return -174 + 10 * np.log10(bw_hz) + nf_db


def calc_link_budget(
    freq_ghz: float,
    dist_km: float,
    rain_rate_mm_h: float,
    humidity_pct: float,
    temperature_c: float,
    polarization: str,
    model: str,
    pt_dbm: float,
    gt_dbi: float,
    gr_dbi: float,
    bw_mhz: float,
    nf_db: float,
) -> Dict[str, float]:
    """Calcule la perte totale, la puissance reçue et le SNR."""
    path_loss = calc_path_loss(dist_km, freq_ghz, model)
    rain_loss = calc_rain_gamma(freq_ghz, rain_rate_mm_h, polarization) * dist_km
    gas_loss = calc_gas_gamma(freq_ghz, humidity_pct, temperature_c) * dist_km
    total_loss = path_loss + rain_loss + gas_loss

    pr_dbm = pt_dbm + gt_dbi + gr_dbi - total_loss
    noise_floor = calc_noise_floor(bw_mhz, nf_db)
    snr_db = pr_dbm - noise_floor

    return {
        "path_loss": float(path_loss),
        "rain_loss": float(rain_loss),
        "gas_loss": float(gas_loss),
        "total_loss": float(total_loss),
        "pr_dbm": float(pr_dbm),
        "noise_floor": float(noise_floor),
        "snr_db": float(snr_db),
    }


def save_figure(path: str, fig: plt.Figure) -> None:
    """Sauvegarde une figure avec un répertoire de sortie automatique."""
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_snr_vs_distance(scenario: Dict[str, float], results: Dict[str, float]) -> None:
    """Trace le SNR vs distance, avec comparaison temps sec / temps humide."""
    distances = np.linspace(0.1, 5.0, 50)
    snr_dry = []
    snr_wet = []
    threshold = np.full_like(distances, 10.0)

    for dist in distances:
        dry = calc_link_budget(
            freq_ghz=scenario["freq_ghz"],
            dist_km=float(dist),
            rain_rate_mm_h=0.0,
            humidity_pct=0.0,
            temperature_c=20.0,
            polarization=scenario["polarization"],
            model=scenario["model"],
            pt_dbm=scenario["pt_dbm"],
            gt_dbi=scenario["gt_dbi"],
            gr_dbi=scenario["gr_dbi"],
            bw_mhz=scenario["bw_mhz"],
            nf_db=scenario["nf_db"],
        )
        wet = calc_link_budget(
            freq_ghz=scenario["freq_ghz"],
            dist_km=float(dist),
            rain_rate_mm_h=scenario["rain_rate_mm_h"],
            humidity_pct=scenario["humidity_pct"],
            temperature_c=scenario["temperature_c"],
            polarization=scenario["polarization"],
            model=scenario["model"],
            pt_dbm=scenario["pt_dbm"],
            gt_dbi=scenario["gt_dbi"],
            gr_dbi=scenario["gr_dbi"],
            bw_mhz=scenario["bw_mhz"],
            nf_db=scenario["nf_db"],
        )
        snr_dry.append(dry["snr_db"])
        snr_wet.append(wet["snr_db"])

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(distances, snr_dry, label="SNR temps sec", linestyle="--", color="royalblue")
    ax.plot(distances, snr_wet, label="SNR avec pluie + humidité", color="forestgreen", linewidth=2)
    ax.plot(distances, threshold, label="Seuil de coupure (10 dB)", linestyle=":", color="crimson")
    ax.set_xlabel("Distance (km)")
    ax.set_ylabel("SNR (dB)")
    ax.set_title(f"SNR vs distance — f = {scenario['freq_ghz']} GHz")
    ax.grid(True, alpha=0.3)
    ax.legend()
    save_figure("figures/snr_vs_distance.png", fig)


def plot_rain_attenuation_curves() -> None:
    """Trace l'atténuation spécifique de pluie pour plusieurs fréquences."""
    rain_rates = np.linspace(0, 100, 200)
    frequencies = [2.4, 5.0, 10.0, 28.0, 60.0]

    fig, ax = plt.subplots(figsize=(8, 5))
    for freq in frequencies:
        gamma = [calc_rain_gamma(freq, r, polarization="C") for r in rain_rates]
        ax.plot(rain_rates, gamma, label=f"{freq} GHz")

    ax.set_xlabel("Intensité de pluie R (mm/h)")
    ax.set_ylabel("Atténuation spécifique γ_R (dB/km)")
    ax.set_title("Atténuation due à la pluie — modèle inspiré de l'UIT-R P.838-3")
    ax.grid(True, alpha=0.3)
    ax.legend()
    save_figure("figures/rain_attenuation_curves.png", fig)


def plot_gas_spectrum() -> None:
    """Trace le spectre d'absorption des gaz et de la vapeur d'eau."""
    freqs = np.linspace(1, 100, 400)
    gas = [calc_gas_gamma(f, 60.0, 20.0) for f in freqs]
    rain = [calc_rain_gamma(f, 25.0, "C") for f in freqs]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(freqs, gas, label="Gaz + vapeur d'eau (dB/km)", color="teal")
    ax.plot(freqs, rain, label="Pluie actuelle (dB/km)", color="dodgerblue")
    ax.set_xscale("linear")
    ax.set_yscale("log")
    ax.set_xlabel("Fréquence (GHz)")
    ax.set_ylabel("Atténuation spécifique (dB/km)")
    ax.set_title("Spectre d'atténuation atmosphérique approximatif")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    save_figure("figures/gas_and_rain_spectrum.png", fig)


def print_summary(name: str, scenario: Dict[str, float], metrics: Dict[str, float]) -> None:
    """Affiche les résultats principaux de simulation."""
    print(f"\n=== {name} ===")
    print(f"Fréquence         : {scenario['freq_ghz']} GHz")
    print(f"Distance          : {scenario['dist_km']} km")
    print(f"Pluie             : {scenario['rain_rate_mm_h']} mm/h")
    print(f"Humidité          : {scenario['humidity_pct']} %")
    print(f"Température       : {scenario['temperature_c']} °C")
    print(f"Polarisation      : {scenario['polarization']}")
    print(f"Modèle de trajet  : {scenario['model']}")
    print(f"Perte de trajet   : {metrics['path_loss']:.2f} dB")
    print(f"Perte pluie       : {metrics['rain_loss']:.2f} dB")
    print(f"Perte gaz         : {metrics['gas_loss']:.2f} dB")
    print(f"Perte totale      : {metrics['total_loss']:.2f} dB")
    print(f"Puissance reçue   : {metrics['pr_dbm']:.2f} dBm")
    print(f"Bruit thermique   : {metrics['noise_floor']:.2f} dBm")
    print(f"SNR               : {metrics['snr_db']:.2f} dB")


def main() -> None:
    """Point d'entrée principal du simulateur."""
    scenario = {
        "freq_ghz": 28.0,
        "dist_km": 1.0,
        "rain_rate_mm_h": 25.0,
        "humidity_pct": 60.0,
        "temperature_c": 20.0,
        "polarization": "C",
        "model": "uit_1411_los",
        "pt_dbm": 30.0,
        "gt_dbi": 10.0,
        "gr_dbi": 5.0,
        "bw_mhz": 20.0,
        "nf_db": 7.0,
    }

    metrics = calc_link_budget(**scenario)
    print_summary("Mini-projet : propagation radio urbaine", scenario, metrics)

    # Création du dossier de sortie.
    os.makedirs("figures", exist_ok=True)

    # Génération des figures de simulation.
    plot_snr_vs_distance(scenario, metrics)
    plot_rain_attenuation_curves()
    plot_gas_spectrum()

    print("\nFigures sauvegardées dans le dossier 'figures/'")
    print("Exemple d'exécution : python radio_propagation_simulation.py")


if __name__ == "__main__":
    main()
