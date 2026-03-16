#!/usr/bin/env python3
"""Reproduce notebook-style EV distribution figures and comparison artifacts (dependency-free)."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def build_demo_counts() -> list[tuple[str, int]]:
    return [
        ("Battery Electric Vehicle (BEV)", 8),
        ("Plug-in Hybrid Electric Vehicle (PHEV)", 4),
    ]


def polar_to_cartesian(cx: float, cy: float, r: float, angle_deg: float) -> tuple[float, float]:
    rad = math.radians(angle_deg)
    return cx + r * math.cos(rad), cy + r * math.sin(rad)


def pie_slice_path(cx: float, cy: float, r: float, start: float, end: float) -> str:
    x1, y1 = polar_to_cartesian(cx, cy, r, start)
    x2, y2 = polar_to_cartesian(cx, cy, r, end)
    large_arc = 1 if (end - start) % 360 > 180 else 0
    return f"M {cx:.2f} {cy:.2f} L {x1:.2f} {y1:.2f} A {r:.2f} {r:.2f} 0 {large_arc} 1 {x2:.2f} {y2:.2f} Z"


def create_base_svg(counts: list[tuple[str, int]]) -> str:
    """Original baseline style."""
    total = sum(v for _, v in counts)
    colors = ["#a1d99b", "#9ecae1", "#fdd0a2", "#cbc9e2"]

    width, height = 1200, 520
    pie_cx, pie_cy, pie_r = 270, 280, 150
    bar_x0, bar_y0 = 620, 420
    bar_w, bar_gap, bar_max_h = 180, 90, 260
    max_count = max(v for _, v in counts)

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="600" y="40" text-anchor="middle" font-size="30" font-family="Arial" font-weight="bold">Electric Vehicle Type Distribution</text>',
        '<text x="270" y="80" text-anchor="middle" font-size="22" font-family="Arial">Percentage of Electric Vehicle Type</text>',
        '<text x="820" y="80" text-anchor="middle" font-size="22" font-family="Arial">Count of Electric Vehicle Type</text>',
    ]

    current_angle = -90.0
    for i, (label, value) in enumerate(counts):
        sweep = 360.0 * value / total
        path = pie_slice_path(pie_cx, pie_cy, pie_r, current_angle, current_angle + sweep)
        color = colors[i % len(colors)]
        svg.append(f'<path d="{path}" fill="{color}" stroke="white" stroke-width="2"/>')

        mid = current_angle + sweep / 2
        lx, ly = polar_to_cartesian(pie_cx, pie_cy, pie_r * 0.65, mid)
        pct = 100.0 * value / total
        svg.append(f'<text x="{lx:.2f}" y="{ly:.2f}" text-anchor="middle" font-size="18" font-family="Arial">{pct:.1f}%</text>')
        current_angle += sweep

    svg.append(f'<line x1="{bar_x0-20}" y1="{bar_y0}" x2="{bar_x0 + (bar_w+bar_gap)*len(counts)}" y2="{bar_y0}" stroke="black"/>')

    for i, (label, value) in enumerate(counts):
        x = bar_x0 + i * (bar_w + bar_gap)
        h = (value / max_count) * bar_max_h
        y = bar_y0 - h
        color = colors[i % len(colors)]
        svg.append(f'<rect x="{x}" y="{y:.2f}" width="{bar_w}" height="{h:.2f}" fill="{color}" stroke="#666"/>')
        svg.append(f'<text x="{x + bar_w/2:.2f}" y="{y - 12:.2f}" text-anchor="middle" font-size="20" font-family="Arial">{value}</text>')
        short = "BEV" if "BEV" in label else "PHEV"
        svg.append(f'<text x="{x + bar_w/2:.2f}" y="{bar_y0 + 28}" text-anchor="middle" font-size="18" font-family="Arial">{short}</text>')

    legend_y = 470
    for i, (label, _) in enumerate(counts):
        color = colors[i % len(colors)]
        lx = 80 + i * 420
        svg.append(f'<rect x="{lx}" y="{legend_y}" width="20" height="20" fill="{color}"/>')
        svg.append(f'<text x="{lx + 30}" y="{legend_y + 16}" font-size="17" font-family="Arial">{label}</text>')

    svg.append('</svg>')
    return "\n".join(svg)


def create_improved_svg(counts: list[tuple[str, int]]) -> str:
    """Improved bar-chart labeling module: full labels + percentages + y-grid."""
    total = sum(v for _, v in counts)
    colors = ["#66c2a5", "#8da0cb", "#fc8d62", "#e78ac3"]

    width, height = 1240, 620
    pie_cx, pie_cy, pie_r = 280, 300, 150
    bar_x0, bar_y0 = 650, 470
    bar_w, bar_gap, bar_max_h = 220, 90, 300
    max_count = max(v for _, v in counts)

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<text x="620" y="42" text-anchor="middle" font-size="30" font-family="Arial" font-weight="bold">Electric Vehicle Type Distribution (Improved)</text>',
        '<text x="280" y="84" text-anchor="middle" font-size="22" font-family="Arial">Pie Share</text>',
        '<text x="890" y="84" text-anchor="middle" font-size="22" font-family="Arial">Bar Count with % and Full Labels</text>',
    ]

    # pie + donut hole for readability
    current_angle = -90.0
    for i, (label, value) in enumerate(counts):
        sweep = 360.0 * value / total
        path = pie_slice_path(pie_cx, pie_cy, pie_r, current_angle, current_angle + sweep)
        color = colors[i % len(colors)]
        svg.append(f'<path d="{path}" fill="{color}" stroke="white" stroke-width="2"/>')

        mid = current_angle + sweep / 2
        lx, ly = polar_to_cartesian(pie_cx, pie_cy, pie_r * 0.72, mid)
        pct = 100.0 * value / total
        svg.append(f'<text x="{lx:.2f}" y="{ly:.2f}" text-anchor="middle" font-size="19" font-family="Arial" fill="#1f1f1f">{pct:.1f}%</text>')
        current_angle += sweep
    svg.append(f'<circle cx="{pie_cx}" cy="{pie_cy}" r="58" fill="white"/>')
    svg.append(f'<text x="{pie_cx}" y="{pie_cy+5}" text-anchor="middle" font-size="18" font-family="Arial" fill="#4d4d4d">Total: {total}</text>')

    # y-grid lines
    for tick in range(0, max_count + 1, 2):
        y = bar_y0 - (tick / max_count) * bar_max_h
        svg.append(f'<line x1="{bar_x0-40}" y1="{y:.2f}" x2="{bar_x0 + (bar_w+bar_gap)*len(counts)-20}" y2="{y:.2f}" stroke="#e9e9e9"/>')
        svg.append(f'<text x="{bar_x0-48}" y="{y+4:.2f}" text-anchor="end" font-size="14" font-family="Arial" fill="#666">{tick}</text>')
    svg.append(f'<line x1="{bar_x0-20}" y1="{bar_y0}" x2="{bar_x0 + (bar_w+bar_gap)*len(counts)-20}" y2="{bar_y0}" stroke="#333"/>')

    for i, (label, value) in enumerate(counts):
        x = bar_x0 + i * (bar_w + bar_gap)
        h = (value / max_count) * bar_max_h
        y = bar_y0 - h
        color = colors[i % len(colors)]
        pct = 100 * value / total
        svg.append(f'<rect x="{x}" y="{y:.2f}" width="{bar_w}" height="{h:.2f}" fill="{color}" stroke="#555" rx="6"/>')
        svg.append(f'<text x="{x + bar_w/2:.2f}" y="{y - 14:.2f}" text-anchor="middle" font-size="19" font-family="Arial">{value} ({pct:.1f}%)</text>')
        svg.append(f'<text x="{x + bar_w/2:.2f}" y="{bar_y0 + 28}" text-anchor="middle" font-size="14" font-family="Arial">{label}</text>')

    svg.append('</svg>')
    return "\n".join(svg)


def run_comparison(counts: list[tuple[str, int]], output_repo: Path) -> None:
    baseline_labels = ["BEV" if "BEV" in label else "PHEV" for label, _ in counts]
    improved_labels = [label for label, _ in counts]

    results = {
        "module": "bar_labeling",
        "baseline": {
            "label_characters": sum(len(x) for x in baseline_labels),
            "contains_percentage_on_bars": False,
            "contains_y_grid": False,
        },
        "improved": {
            "label_characters": sum(len(x) for x in improved_labels),
            "contains_percentage_on_bars": True,
            "contains_y_grid": True,
        },
    }

    comparison_dir = output_repo / "comparison"
    comparison_dir.mkdir(parents=True, exist_ok=True)

    (comparison_dir / "comparison_metrics.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    report = (
        "# Comparison Experiment\n\n"
        "Improved module: **bar labeling and readability**.\n\n"
        "- Baseline labels use abbreviations (`BEV`, `PHEV`) only.\n"
        "- Improved labels use full class names, add percentage on bars, and add y-grid.\n\n"
        "## Quantitative Summary\n\n"
        f"- Baseline label characters: {results['baseline']['label_characters']}\n"
        f"- Improved label characters: {results['improved']['label_characters']}\n"
        f"- Percentage shown on bars: baseline={results['baseline']['contains_percentage_on_bars']}, improved={results['improved']['contains_percentage_on_bars']}\n"
        f"- Y-grid present: baseline={results['baseline']['contains_y_grid']}, improved={results['improved']['contains_y_grid']}\n"
    )
    (comparison_dir / "report.md").write_text(report, encoding="utf-8")


def init_separate_repo(repo_dir: Path) -> None:
    repo_dir.mkdir(parents=True, exist_ok=True)
    if not (repo_dir / ".git").exists():
        import subprocess

        subprocess.run(["git", "init"], cwd=repo_dir, check=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-repo", default="../paper-figures-repo")
    parser.add_argument("--base-image-name", default="electric_vehicle_type_distribution_baseline.svg")
    parser.add_argument("--improved-image-name", default="electric_vehicle_type_distribution_improved.svg")
    args = parser.parse_args()

    output_repo = Path(args.output_repo).resolve()
    init_separate_repo(output_repo)

    counts = build_demo_counts()

    image_dir = output_repo / "images"
    image_dir.mkdir(parents=True, exist_ok=True)
    base_path = image_dir / args.base_image_name
    improved_path = image_dir / args.improved_image_name

    base_path.write_text(create_base_svg(counts), encoding="utf-8")
    improved_path.write_text(create_improved_svg(counts), encoding="utf-8")
    run_comparison(counts, output_repo)

    (output_repo / "README.md").write_text(
        "# Paper Figures\n\n"
        "This standalone repository stores reproduced figures for academic writing.\n\n"
        "Generated artifacts:\n"
        f"- `images/{args.base_image_name}` (baseline)\n"
        f"- `images/{args.improved_image_name}` (improved)\n"
        "- `comparison/report.md`\n"
        "- `comparison/comparison_metrics.json`\n",
        encoding="utf-8",
    )

    print(f"Saved baseline figure to: {base_path}")
    print(f"Saved improved figure to: {improved_path}")
    print(f"Saved comparison report to: {output_repo / 'comparison' / 'report.md'}")


if __name__ == "__main__":
    main()
