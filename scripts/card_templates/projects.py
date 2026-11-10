"""
Featured Project Cards Generator for Abu Sufiyan.
Generates separate animated SVG cards for:
1. Aura — Music Streaming Application
2. NexusEMS — Intern Management Platform
3. Portfolio Website — 3D Interactive Portfolio
4. Acer ALG Control Center — Linux Hardware Utility & GUI
"""

from .theme import (
    BG_DARK, BG_CARD_START, BG_CARD_END, BORDER_BASE, BORDER_HIGHLIGHT,
    ACCENT_CYAN, ACCENT_SKY, ACCENT_BLUE, ACCENT_EMERALD, ACCENT_ROYAL, ACCENT_AMBER,
    TEXT_HEADLINE, TEXT_BODY, TEXT_MUTED, TEXT_ACCENT,
    FONT_SERIF, FONT_SANS, FONT_MONO,
    get_common_defs, get_base_css, xml_escape
)

PROJECTS_DATA = {
    "aura": {
        "id": "aura",
        "name": "AURA",
        "subtitle": "MUSIC STREAMING APPLICATION",
        "badge": "LIVE DEMO AVAILABLE",
        "badge_color": ACCENT_EMERALD,
        "description_lines": [
            "Modern music platform featuring interactive player,",
            "3D WebGL audio-reactive visuals, JWT auth &amp; dynamic playlists."
        ],
        "tech_stack": ["React", "TypeScript", "Node.js", "Express", "MySQL", "JWT", "WebGL"],
        "repo_url": "https://github.com/Abbusufiyan/Music",
        "demo_url": "https://music-six-lemon.vercel.app/",
        "action_label": "LAUNCH DEMO ↗",
        "icon_path": "M 9 18 V 5 l 12 -2 v 13 M 9 18 a 3 3 0 1 1 -6 0 a 3 3 0 0 1 6 0 M 21 16 a 3 3 0 1 1 -6 0 a 3 3 0 0 1 6 0"
    },
    "nexus-ems": {
        "id": "nexus-ems",
        "name": "NEXUSEMS",
        "subtitle": "INTERN MANAGEMENT PLATFORM",
        "badge": "ROLE-BASED AUTH",
        "badge_color": ACCENT_SKY,
        "description_lines": [
            "Operational platform for intern tracking, task delegation,",
            "structured performance reviews, and administrative analytics."
        ],
        "tech_stack": ["React.js", "Node.js", "Express.js", "MySQL", "REST APIs", "JWT"],
        "repo_url": "https://github.com/Abbusufiyan/Employee_Management_System",
        "demo_url": None,
        "action_label": "EXPLORE REPOSITORY →",
        "icon_path": "M 17 21 v -2 a 4 4 0 0 0 -4 -4 H 5 a 4 4 0 0 0 -4 4 v 2 M 9 7 a 4 4 0 1 0 0 -8 a 4 4 0 0 0 0 8 M 23 21 v -2 a 4 4 0 0 0 -3 -3.87 M 16 3.13 a 4 4 0 0 1 0 7.75"
    },
    "portfolio": {
        "id": "portfolio",
        "name": "PORTFOLIO 3D",
        "subtitle": "INTERACTIVE WEB EXPERIENCE",
        "badge": "THREE.JS / WEBGL",
        "badge_color": ACCENT_CYAN,
        "description_lines": [
            "Immersive portfolio showcasing interactive 3D CV rendering,",
            "particle background shaders, camera paths, &amp; Lenis physics."
        ],
        "tech_stack": ["React", "TypeScript", "Three.js", "R3F", "Tailwind CSS", "Vite"],
        "repo_url": "https://github.com/Abbusufiyan/Portfolio-Website",
        "demo_url": "https://portfolio-website-ten-theta-96.vercel.app/",
        "action_label": "VIEW LIVE SITE ↗",
        "icon_path": "M 21 16 V 8 a 2 2 0 0 0 -1 -1.73 l -7 -4 a 2 2 0 0 0 -2 0 l -7 4 A 2 2 0 0 0 3 8 v 8 a 2 2 0 0 0 1 1.73 l 7 4 a 2 2 0 0 0 2 0 l 7 -4 A 2 2 0 0 0 21 16 z M 3.27 6.96 L 12 12.01 l 8.73 -5.05 M 12 22.08 V 12"
    },
    "acer-control": {
        "id": "acer-control",
        "name": "ACER ALG CENTER",
        "subtitle": "LINUX HARDWARE UTILITY &amp; GUI",
        "badge": "KERNEL DRIVER / DKMS",
        "badge_color": ACCENT_AMBER,
        "description_lines": [
            "Native Linux utility for Acer ALG laptops: 16-color RGB keyboard,",
            "independent dual-fan governor &amp; real-time RTX telemetry."
        ],
        "tech_stack": ["Python 3", "PyQt6", "ACPI Driver", "DKMS", "Linux Sysfs"],
        "repo_url": "https://github.com/Abbusufiyan/ACER-ALG-KEYBOARD-LIGHT-CONTRO",
        "demo_url": None,
        "action_label": "INSPECT HARDWARE REPO →",
        "icon_path": "M 12 2 v 2 M 12 20 v 2 M 4.93 4.93 l 1.41 1.41 M 17.66 17.66 l 1.41 1.41 M 2 12 h 2 M 20 12 h 2 M 4.93 19.07 l 1.41 -1.41 M 17.66 6.34 l 1.41 -1.41"
    }
}


def render_project_card(project_key: str, is_static: bool = False) -> str:
    """Generate an animated SVG card for a specific featured project."""
    if project_key not in PROJECTS_DATA:
        raise ValueError(f"Unknown project key: {project_key}")

    p = PROJECTS_DATA[project_key]
    width = 430
    height = 240

    defs = get_common_defs(f"proj_{p['id']}")
    base_css = get_base_css(is_static)

    custom_css = "" if is_static else f"""
    @keyframes projectGlow {{
      0%, 100% {{ filter: drop-shadow(0 0 2px rgba(0, 240, 255, 0.25)); }}
      50% {{ filter: drop-shadow(0 0 6px rgba(0, 240, 255, 0.65)); }}
    }}

    .proj-title {{
      animation: projectGlow 5s ease-in-out infinite;
    }}
"""

    # Render tech pills
    pill_elements = []
    px = 22
    py = 186
    max_w = width - 24

    for tech in p["tech_stack"][:5]:  # show top 5 for clean fit
        tech_escaped = xml_escape(tech)
        tw = max(42, len(tech) * 6.5 + 16)
        if px + tw > max_w:
            break
        pill_elements.append(f"""
      <g transform="translate({px}, {py})">
        <rect x="0" y="0" width="{tw}" height="20" rx="10" fill="#091326" stroke="{BORDER_BASE}" stroke-width="0.8"/>
        <text x="{tw / 2}" y="13.5" class="text-mono" font-size="9" fill="{TEXT_BODY}" text-anchor="middle">{tech_escaped}</text>
      </g>""")
        px += tw + 6

    pills_markup = "\n".join(pill_elements)

    desc_line1 = xml_escape(p["description_lines"][0])
    desc_line2 = xml_escape(p["description_lines"][1]) if len(p["description_lines"]) > 1 else ""
    subtitle = xml_escape(p["subtitle"])
    action_label = xml_escape(p["action_label"])

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="{height}" style="background: transparent;">
  <style>
    {base_css}
    {custom_css}
    .text-title {{
      font-family: {FONT_SERIF};
      font-weight: 700;
      letter-spacing: 0.06em;
    }}
    .text-sans {{
      font-family: {FONT_SANS};
    }}
    .text-mono {{
      font-family: {FONT_MONO};
    }}
  </style>

  {defs}

  <!-- Main Card Container -->
  <rect x="2" y="2" width="{width - 4}" height="{height - 4}" rx="14" fill="url(#proj_{p['id']}_bgGradient)" stroke="url(#proj_{p['id']}_borderGradient)" stroke-width="1.5" filter="url(#proj_{p['id']}_cardShadow)"/>
  <rect x="2" y="2" width="{width - 4}" height="{height - 4}" rx="14" fill="url(#proj_{p['id']}_ambientGlow)" pointer-events="none"/>

  <!-- Top Status Badge &amp; Icon -->
  <g transform="translate(22, 22)">
    <!-- Category Icon -->
    <rect x="0" y="0" width="30" height="30" rx="8" fill="#08142a" stroke="{BORDER_BASE}" stroke-width="1"/>
    <path d="{p['icon_path']}" fill="none" stroke="{ACCENT_CYAN}" stroke-width="1.3" transform="translate(4, 4) scale(0.9)"/>

    <!-- Badge -->
    <g transform="translate({width - 44 - 150}, 4)">
      <rect x="0" y="0" width="150" height="22" rx="11" fill="#08172c" stroke="{p['badge_color']}" stroke-width="0.8" opacity="0.9"/>
      <circle cx="12" cy="11" r="3" fill="{p['badge_color']}"/>
      <text x="22" y="14.5" class="text-mono" font-size="8.5" font-weight="600" fill="{p['badge_color']}" letter-spacing="0.05em">{p['badge']}</text>
    </g>
  </g>

  <!-- Project Name &amp; Subtitle -->
  <g transform="translate(22, 82)">
    <text class="text-title proj-title" font-size="22" fill="{TEXT_HEADLINE}">
      {p['name']}
    </text>
    <text x="0" y="20" class="text-mono" font-size="9.5" fill="{ACCENT_SKY}" letter-spacing="0.08em">
      {subtitle}
    </text>
    <line x1="0" y1="28" x2="{width - 44}" y2="28" stroke="{BORDER_BASE}" stroke-width="0.8"/>
  </g>

  <!-- Short Description -->
  <g transform="translate(22, 132)" class="text-sans" font-size="11.5" fill="{TEXT_BODY}">
    <text x="0" y="0">{desc_line1}</text>
    <text x="0" y="18" fill="{TEXT_MUTED}">{desc_line2}</text>
  </g>

  <!-- Tech Stack Pills -->
  {pills_markup}

  <!-- Bottom Action Cue -->
  <g transform="translate({width - 24}, 222)">
    <text x="0" y="0" class="text-mono" font-size="9.5" font-weight="600" fill="{ACCENT_CYAN}" text-anchor="end" letter-spacing="0.06em">
      {action_label}
    </text>
  </g>
</svg>"""
