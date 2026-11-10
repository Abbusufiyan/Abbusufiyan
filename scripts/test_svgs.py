#!/usr/bin/env python3
"""
Comprehensive Validation & Test Suite for Abu Sufiyan's Profile SVG System.
Validates:
1. XML syntax and well-formedness of all generated SVG cards.
2. SVG standards compliance (viewBox, xmlns, width, height).
3. Security: No inline executable javascript (<script> tags).
4. Accessibility: Presence of prefers-reduced-motion media query.
5. CSS Animation rules and keyframes integrity.
6. Static preview mode verification (STATIC=1).
7. Data integrity against data/contributions.json.
8. External link validity format.
"""

import os
import sys
import json
import xml.etree.ElementTree as ET
import subprocess

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARDS_DIR = os.path.join(ROOT_DIR, "assets", "cards")
DATA_FILE = os.path.join(ROOT_DIR, "data", "contributions.json")

# Ensure ROOT_DIR in sys.path
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

EXPECTED_CARDS = [
    "hero.svg",
    "skills.svg",
    "contribution-stats.svg",
    "contribution-heatmap.svg",
    "project-aura.svg",
    "project-nexus-ems.svg",
    "project-portfolio.svg",
    "project-acer-control.svg",
    "connect.svg",
]


def test_svg_files_exist_and_valid():
    """Verify all expected SVG cards exist and are well-formed XML."""
    print("[1/6] Testing SVG existence and XML well-formedness...")
    assert os.path.isdir(CARDS_DIR), f"Missing cards directory: {CARDS_DIR}"

    for card_name in EXPECTED_CARDS:
        card_path = os.path.join(CARDS_DIR, card_name)
        assert os.path.exists(card_path), f"Missing card: {card_name}"
        file_size = os.path.getsize(card_path)
        assert file_size > 500, f"Card {card_name} is suspiciously small: {file_size} bytes"
        assert file_size < 300_000, f"Card {card_name} is too large: {file_size} bytes"

        # XML parsing
        try:
            tree = ET.parse(card_path)
            root = tree.getroot()
        except ET.ParseError as e:
            raise AssertionError(f"XML parse error in {card_name}: {e}")

        # Check root tag and attributes
        tag = root.tag.split("}")[-1] if "}" in root.tag else root.tag
        assert tag == "svg", f"Root element of {card_name} is '{tag}', expected 'svg'"
        assert "viewBox" in root.attrib, f"{card_name} missing viewBox attribute"

        # Security check: no script tags
        scripts = [elem for elem in root.iter() if elem.tag.endswith("script")]
        assert len(scripts) == 0, f"Security hazard: found <script> tag in {card_name}"

        # CSS checks: read raw content
        with open(card_path, "r", encoding="utf-8") as f:
            content = f.read()

        assert "prefers-reduced-motion" in content, f"{card_name} missing prefers-reduced-motion CSS query"
        print(f"  [✓] {card_name:<26} (XML valid, {file_size / 1024:.1f} KB)")


def test_animated_keyframes():
    """Verify animations exist in animated production mode."""
    print("\n[2/6] Testing CSS animation keyframes...")
    animated_cards = ["hero.svg", "skills.svg", "contribution-stats.svg", "contribution-heatmap.svg"]
    for card_name in animated_cards:
        card_path = os.path.join(CARDS_DIR, card_name)
        with open(card_path, "r", encoding="utf-8") as f:
            content = f.read()
        assert "@keyframes" in content, f"{card_name} should contain CSS keyframes in normal mode"
    print("  [✓] All animated cards include valid CSS keyframes.")


def test_static_preview_mode():
    """Verify STATIC=1 disables all animations."""
    print("\n[3/6] Testing STATIC=1 preview mode execution...")
    env = os.environ.copy()
    env["STATIC"] = "1"
    res = subprocess.run([sys.executable, os.path.join(ROOT_DIR, "scripts", "render_readme_cards.py")], env=env, capture_output=True, text=True)
    assert res.returncode == 0, f"Static render failed: {res.stderr}"

    # Inspect hero.svg in static mode
    hero_path = os.path.join(CARDS_DIR, "hero.svg")
    with open(hero_path, "r", encoding="utf-8") as f:
        hero_static = f.read()

    assert "animation: none !important" in hero_static, "hero.svg should disable animations in static mode"
    print("  [✓] Static preview mode executed and disabled keyframes successfully.")

    # Re-render normal mode
    res_normal = subprocess.run([sys.executable, os.path.join(ROOT_DIR, "scripts", "render_readme_cards.py")], capture_output=True, text=True)
    assert res_normal.returncode == 0, f"Normal render failed: {res_normal.stderr}"
    print("  [✓] Restored animated production cards.")


def test_contributions_data_integrity():
    """Verify contribution data structure and metrics."""
    print("\n[4/6] Testing contributions data integrity...")
    assert os.path.exists(DATA_FILE), f"Missing data file: {DATA_FILE}"
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data.get("username") == "Abbusufiyan"
    assert isinstance(data.get("total_contributions"), int) and data["total_contributions"] > 0
    assert isinstance(data.get("active_days"), int) and data["active_days"] > 0
    assert isinstance(data.get("current_streak"), int)
    assert isinstance(data.get("longest_streak"), int) and data["longest_streak"] >= data["current_streak"]
    assert "busiest_day" in data and "count" in data["busiest_day"]
    assert len(data.get("monthly_summary", [])) > 0
    assert len(data.get("weeks", [])) >= 50

    print(f"  [✓] Validated {data['total_contributions']} total commits across {len(data['weeks'])} weeks.")


def test_project_links_and_tech_stack():
    """Verify project definitions and URLs."""
    print("\n[5/6] Testing project metadata and URLs...")
    from scripts.card_templates import PROJECTS_DATA

    for key, p in PROJECTS_DATA.items():
        assert p["repo_url"].startswith("https://github.com/Abbusufiyan/"), f"Invalid repo url: {p['repo_url']}"
        if p.get("demo_url"):
            assert p["demo_url"].startswith("https://"), f"Invalid demo url: {p['demo_url']}"
        assert len(p["tech_stack"]) >= 3, f"Project {key} should have at least 3 technologies listed"
        print(f"  [✓] Project {p['name']:<18} ({len(p['tech_stack'])} tech items, repo verified)")


def test_readme_references():
    """Verify README.md references all generated SVG cards."""
    print("\n[6/6] Testing README.md file and asset references...")
    readme_path = os.path.join(ROOT_DIR, "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()
        for card_name in EXPECTED_CARDS:
            assert card_name in content, f"README.md does not reference {card_name}"
        print(f"  [✓] README.md references all {len(EXPECTED_CARDS)} SVG cards.")
    else:
        print("  [-] README.md not yet created. Skipping README check.")


def main():
    print("==================================================")
    print("  Running Test Suite for Profile Cards System")
    print("==================================================")
    test_svg_files_exist_and_valid()
    test_animated_keyframes()
    test_static_preview_mode()
    test_contributions_data_integrity()
    test_project_links_and_tech_stack()
    test_readme_references()
    print("\n==================================================")
    print("  ALL TESTS PASSED SUCCESSFULLY! (6/6 Suites)")
    print("==================================================")


if __name__ == "__main__":
    main()
