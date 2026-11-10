"""
Technology and Skills Card Generator for Abu Sufiyan.
Organized into 4 visual categories: Frontend, Backend, Programming & Databases, Tools.
Electric blue theme with pill badges and tech accents.
"""

from .theme import (
    BG_DARK, BG_CARD_START, BG_CARD_END, BORDER_BASE, BORDER_HIGHLIGHT,
    ACCENT_CYAN, ACCENT_SKY, ACCENT_BLUE, ACCENT_EMERALD, ACCENT_ROYAL,
    TEXT_HEADLINE, TEXT_BODY, TEXT_MUTED, TEXT_ACCENT,
    FONT_SERIF, FONT_SANS, FONT_MONO,
    get_common_defs, get_base_css, xml_escape
)


def render_skills_card(is_static: bool = False) -> str:
    """Generate the animated Technology & Skills SVG card."""
    width = 880
    height = 380

    defs = get_common_defs("skills")
    base_css = get_base_css(is_static)

    custom_css = "" if is_static else f"""
    @keyframes pillPulse {{
      0%, 100% {{ border-color: {BORDER_BASE}; }}
      50% {{ border-color: {ACCENT_CYAN}; }}
    }}

    @keyframes iconGlow {{
      0%, 100% {{ filter: drop-shadow(0 0 2px rgba(0, 240, 255, 0.2)); }}
      50% {{ filter: drop-shadow(0 0 6px rgba(0, 240, 255, 0.7)); }}
    }}

    .cat-icon {{
      animation: iconGlow 4s ease-in-out infinite;
    }}
"""

    # Skills definitions
    categories = [
        {
            "id": "frontend",
            "title": "FRONTEND &amp; GRAPHICS",
            "subtitle": "Interactive UI &amp; 3D Web",
            "icon": "M 4 8 L 12 2 L 20 8 L 20 18 L 12 22 L 4 18 Z",
            "x": 30, "y": 75, "w": 395, "h": 130,
            "skills": [
                "React.js", "TypeScript", "JavaScript",
                "Tailwind CSS", "Three.js", "R3F", "Framer Motion"
            ]
        },
        {
            "id": "backend",
            "title": "BACKEND &amp; ARCHITECTURE",
            "subtitle": "APIs &amp; Authentication",
            "icon": "M 3 6 L 12 3 L 21 6 L 21 15 L 12 21 L 3 15 Z M 12 3 L 12 21",
            "x": 455, "y": 75, "w": 395, "h": 130,
            "skills": [
                "Node.js", "Express.js", "REST APIs", "JWT", "Bcrypt"
            ]
        },
        {
            "id": "systems",
            "title": "PROGRAMMING &amp; DATABASES",
            "subtitle": "Systems, OOP &amp; Structures",
            "icon": "M 2 12 L 12 2 L 22 12 L 12 22 Z M 7 12 L 12 7 L 17 12 L 12 17 Z",
            "x": 30, "y": 220, "w": 395, "h": 130,
            "skills": [
                "C++", "MySQL", "DBMS", "OOP", "Data Structures &amp; Algos"
            ]
        },
        {
            "id": "tools",
            "title": "ENGINEERING TOOLS &amp; DEVOPS",
            "subtitle": "Workflow &amp; Code Quality",
            "icon": "M 4 4 L 20 4 L 20 20 L 4 20 Z M 9 9 L 15 9 M 9 12 L 15 12 M 9 15 L 13 15",
            "x": 455, "y": 220, "w": 395, "h": 130,
            "skills": [
                "Git", "GitHub", "SonarQube", "Linux / Bash", "Vite"
            ]
        }
    ]

    # Generate category blocks
    category_svgs = []
    for cat in categories:
        cx, cy, cw, ch = cat["x"], cat["y"], cat["w"], cat["h"]

        # Render skill pills with calculated offsets
        pill_elements = []
        px = 16
        py = 56
        row_height = 28
        max_row_width = cw - 28

        for skill in cat["skills"]:
            approx_w = max(52, len(skill.replace("&amp;", "&")) * 7.5 + 20)
            if px + approx_w > max_row_width:
                px = 16
                py += row_height

            pill_elements.append(f"""
        <!-- Pill: {skill} -->
        <g transform="translate({px}, {py})">
          <rect x="0" y="0" width="{approx_w}" height="22" rx="11" fill="#091326" stroke="{BORDER_BASE}" stroke-width="1"/>
          <circle cx="9" cy="11" r="2" fill="{ACCENT_CYAN}" opacity="0.8"/>
          <text x="17" y="14.5" class="text-mono" font-size="10.5" fill="{TEXT_HEADLINE}" font-weight="500">{skill}</text>
        </g>""")
            px += approx_w + 8

        pills_markup = "\n".join(pill_elements)

        category_svgs.append(f"""
    <!-- Category: {cat['title']} -->
    <g transform="translate({cx}, {cy})">
      <!-- Container Background -->
      <rect x="0" y="0" width="{cw}" height="{ch}" rx="12" fill="#070c18" stroke="{BORDER_BASE}" stroke-width="1"/>
      <rect x="0" y="0" width="{cw}" height="{ch}" rx="12" fill="url(#skills_techGrid)" opacity="0.4"/>

      <!-- Header -->
      <g transform="translate(14, 14)">
        <!-- Category Icon Box -->
        <rect x="0" y="0" width="28" height="28" rx="6" fill="#0c1830" stroke="{BORDER_BASE}" stroke-width="1"/>
        <path d="{cat['icon']}" fill="none" stroke="{ACCENT_CYAN}" stroke-width="1.3" transform="translate(2, 2) scale(1)" class="cat-icon"/>

        <!-- Title &amp; Subtitle -->
        <text x="38" y="13" class="text-mono" font-size="11.5" font-weight="700" fill="{TEXT_HEADLINE}" letter-spacing="0.06em">
          {cat['title']}
        </text>
        <text x="38" y="25" class="text-sans" font-size="9.5" fill="{TEXT_MUTED}">
          {cat['subtitle']}
        </text>
      </g>

      <!-- Divider line -->
      <line x1="14" y1="48" x2="{cw - 14}" y2="48" stroke="{BORDER_BASE}" stroke-width="0.8" opacity="0.6"/>

      <!-- Skill Pills -->
      <g>
        {pills_markup}
      </g>
    </g>""")

    rendered_categories = "\n".join(category_svgs)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="{height}" style="background: transparent;">
  <style>
    {base_css}
    {custom_css}
    .text-title {{
      font-family: {FONT_SERIF};
      font-weight: 700;
      letter-spacing: 0.05em;
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
  <rect x="2" y="2" width="{width - 4}" height="{height - 4}" rx="16" fill="url(#skills_bgGradient)" stroke="url(#skills_borderGradient)" stroke-width="1.5" filter="url(#skills_cardShadow)"/>
  <rect x="2" y="2" width="{width - 4}" height="{height - 4}" rx="16" fill="url(#skills_ambientGlow)" pointer-events="none"/>

  <!-- Card Header -->
  <g transform="translate(30, 36)">
    <circle cx="6" cy="6" r="4" fill="{ACCENT_CYAN}"/>
    <text x="20" y="10" class="text-title" font-size="20" fill="{TEXT_HEADLINE}">
      TECHNICAL ARSENAL &amp; CAPABILITIES
    </text>
    <text x="820" y="10" class="text-mono" font-size="10.5" fill="{TEXT_MUTED}" text-anchor="end">
      STACK // VERIFIED SKILLS
    </text>
    <line x1="0" y1="22" x2="820" y2="22" stroke="{BORDER_BASE}" stroke-width="1"/>
  </g>

  <!-- Categories Grid -->
  {rendered_categories}
</svg>"""
