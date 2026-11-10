#!/usr/bin/env python3
"""
Master SVG Renderer for Abu Sufiyan's GitHub Profile README.
Generates all animated SVG cards based on real contributions and project data.

Supports static preview mode via:
    STATIC=1 python scripts/render_readme_cards.py
    python scripts/render_readme_cards.py --static
"""

import os
import sys
import json
import argparse
import xml.etree.ElementTree as ET

# Ensure parent directory is in python path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

from scripts.card_templates import (
    render_hero_card,
    render_skills_card,
    render_stats_card,
    render_heatmap_card,
    render_project_card,
    PROJECTS_DATA,
    render_connect_card,
)


def load_contributions_data(filepath: str) -> dict:
    """Load contributions JSON or fallback to graceful defaults."""
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[!] Warning: Failed to parse {filepath}: {e}")

    # Fallback structure
    print("[!] Using fallback contribution data.")
    return {
        "username": "Abbusufiyan",
        "total_contributions": 226,
        "active_days": 44,
        "current_streak": 7,
        "longest_streak": 12,
        "busiest_day": {"date": "2026-11-08", "count": 28},
        "monthly_summary": [
            {"label": "Dec 25", "count": 0}, {"label": "Jan 26", "count": 0},
            {"label": "Feb 26", "count": 0}, {"label": "Mar 26", "count": 56},
            {"label": "Apr 26", "count": 0}, {"label": "May 26", "count": 9},
            {"label": "Jun 26", "count": 0}, {"label": "Jul 26", "count": 0},
            {"label": "Aug 26", "count": 10}, {"label": "Sep 26", "count": 22},
            {"label": "Oct 26", "count": 32}, {"label": "Nov 26", "count": 97}
        ],
        "weeks": [],
    }


def validate_and_save_svg(svg_content: str, output_path: str) -> bool:
    """Validate XML well-formedness and save to disk."""
    try:
        # Validate XML structure
        ET.fromstring(svg_content)
    except ET.ParseError as err:
        print(f"[✗] XML Validation Error in {os.path.basename(output_path)}: {err}")
        return False

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content.strip() + "\n")
    return True


def main():
    parser = argparse.ArgumentParser(description="Render animated SVG cards for GitHub README.")
    parser.add_argument("--static", action="store_true", help="Render static preview without animations")
    parser.add_argument("--output-dir", default=os.path.join(ROOT_DIR, "assets", "cards"), help="Output directory")
    parser.add_argument("--data-file", default=os.path.join(ROOT_DIR, "data", "contributions.json"), help="Contributions JSON path")
    args = parser.parse_args()

    is_static = args.static or (os.environ.get("STATIC", "").lower() in ("1", "true", "yes"))

    mode_str = "STATIC PREVIEW (Animations disabled)" if is_static else "ANIMATED PRODUCTION (CSS keyframes enabled)"
    print(f"==================================================")
    print(f"  Abu Sufiyan README SVG Card Generator")
    print(f"  Mode: {mode_str}")
    print(f"==================================================")

    # Load data
    metrics = load_contributions_data(args.data_file)

    # Define all cards to render
    cards_to_render = [
        ("hero.svg", lambda: render_hero_card(is_static=is_static)),
        ("skills.svg", lambda: render_skills_card(is_static=is_static)),
        ("contribution-stats.svg", lambda: render_stats_card(metrics, is_static=is_static)),
        ("contribution-heatmap.svg", lambda: render_heatmap_card(metrics, is_static=is_static)),
        ("project-aura.svg", lambda: render_project_card("aura", is_static=is_static)),
        ("project-nexus-ems.svg", lambda: render_project_card("nexus-ems", is_static=is_static)),
        ("project-portfolio.svg", lambda: render_project_card("portfolio", is_static=is_static)),
        ("project-acer-control.svg", lambda: render_project_card("acer-control", is_static=is_static)),
        ("connect.svg", lambda: render_connect_card(is_static=is_static)),
    ]

    success_count = 0
    total_count = len(cards_to_render)

    print("\nRendering cards:")
    for filename, render_func in cards_to_render:
        dest_path = os.path.join(args.output_dir, filename)
        content = render_func()
        if validate_and_save_svg(content, dest_path):
            size_kb = os.path.getsize(dest_path) / 1024
            print(f"  [✓] {filename:<26} ({size_kb:6.2f} KB) -> {os.path.relpath(dest_path, ROOT_DIR)}")
            success_count += 1
        else:
            print(f"  [✗] Failed to render {filename}")

    print(f"\nCompleted: {success_count}/{total_count} cards successfully generated.")
    if success_count < total_count:
        sys.exit(1)


if __name__ == "__main__":
    main()
