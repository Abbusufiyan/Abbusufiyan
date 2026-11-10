"""
Connect Section Card Generator for Abu Sufiyan.
Sleek developer contact & profiles card with GitHub, LinkedIn, Portfolio, and LeetCode.
"""

from .theme import (
    BG_DARK, BG_CARD_START, BG_CARD_END, BORDER_BASE, BORDER_HIGHLIGHT,
    ACCENT_CYAN, ACCENT_SKY, ACCENT_BLUE, ACCENT_EMERALD, ACCENT_AMBER,
    TEXT_HEADLINE, TEXT_BODY, TEXT_MUTED, TEXT_ACCENT,
    FONT_SERIF, FONT_SANS, FONT_MONO,
    get_common_defs, get_base_css
)


def render_connect_card(is_static: bool = False) -> str:
    """Generate the animated Connect & Social SVG card."""
    width = 880
    height = 190

    defs = get_common_defs("connect")
    base_css = get_base_css(is_static)

    custom_css = "" if is_static else f"""
    @keyframes linkGlow {{
      0%, 100% {{ border-color: {BORDER_BASE}; }}
      50% {{ border-color: {ACCENT_CYAN}; }}
    }}

    @keyframes dotPulse {{
      0%, 100% {{ opacity: 0.9; transform: scale(1); }}
      50% {{ opacity: 0.4; transform: scale(0.8); }}
    }}

    .online-dot {{
      animation: dotPulse 2s ease-in-out infinite;
    }}
"""

    channels = [
        {
            "name": "GITHUB",
            "handle": "@Abbusufiyan",
            "sub": "25 Repositories",
            "color": ACCENT_CYAN,
            "icon": "M 9 19 c -5 1.5 -5 -2.5 -7 -3 m 14 6 v -3.87 a 3.37 3.37 0 0 0 -0.94 -2.61 c 3.14 -0.35 6.44 -1.54 6.44 -7 A 5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1 S 18.73 0.65 16 2.48 a 13.38 13.38 0 0 0 -7 0 C 6.27 0.65 5.09 1 5.09 1 A 5.07 5.07 0 0 0 5 4.77 a 5.44 5.44 0 0 0 -1.5 3.78 c 0 5.42 3.3 6.61 6.44 7 A 3.37 3.37 0 0 0 9 18.13 V 22"
        },
        {
            "name": "LINKEDIN",
            "handle": "in/abu-sufiyan",
            "sub": "Professional Network",
            "color": ACCENT_SKY,
            "icon": "M 16 8 a 6 6 0 0 1 6 6 v 7 h -4 v -7 a 2 2 0 0 0 -2 -2 2 2 0 0 0 -2 2 v 7 h -4 v -7 a 6 6 0 0 1 6 -6 z M 2 9 h 4 v 12 H 2 z M 4 2 a 2 2 0 1 1 -2 2 a 2 2 0 0 1 2 -2 z"
        },
        {
            "name": "PORTFOLIO",
            "handle": "Interactive 3D",
            "sub": "Live WebGL Showcase",
            "color": ACCENT_EMERALD,
            "icon": "M 12 2 a 10 10 0 1 0 10 10 A 10 10 0 0 0 12 2 z M 2 12 h 20 M 12 2 a 15.3 15.3 0 0 1 4 10 a 15.3 15.3 0 0 1 -4 10 a 15.3 15.3 0 0 1 -4 -10 a 15.3 15.3 0 0 1 4 -10 z"
        },
        {
            "name": "LEETCODE",
            "handle": "BUHw5Vatuj",
            "sub": "DSA &amp; Problem Solving",
            "color": ACCENT_AMBER,
            "icon": "M 16 3 L 6 13 L 16 23 M 12 13 H 22"
        }
    ]

    tile_w = 196
    tile_h = 86
    start_x = 30
    gap = 12

    tile_elements = []
    for i, ch in enumerate(channels):
        tx = start_x + i * (tile_w + gap)
        tile_elements.append(f"""
    <!-- Channel: {ch['name']} -->
    <g transform="translate({tx}, 72)">
      <rect x="0" y="0" width="{tile_w}" height="{tile_h}" rx="10" fill="#070c18" stroke="{BORDER_BASE}" stroke-width="1"/>
      <rect x="0" y="0" width="{tile_w}" height="2" rx="1" fill="{ch['color']}" opacity="0.8"/>

      <!-- Icon Box -->
      <rect x="12" y="14" width="28" height="28" rx="6" fill="#0a1529" stroke="{BORDER_BASE}" stroke-width="0.8"/>
      <path d="{ch['icon']}" fill="none" stroke="{ch['color']}" stroke-width="1.3" transform="translate(14, 16) scale(1)"/>

      <!-- Texts -->
      <text x="50" y="24" class="text-mono" font-size="10" font-weight="700" fill="{TEXT_HEADLINE}" letter-spacing="0.06em">{ch['name']}</text>
      <text x="50" y="38" class="text-mono" font-size="9" fill="{ch['color']}">{ch['handle']}</text>

      <!-- Subtitle -->
      <text x="12" y="66" class="text-sans" font-size="9" fill="{TEXT_MUTED}">{ch['sub']}</text>

      <!-- Status dot -->
      <circle cx="{tile_w - 14}" cy="16" r="3" fill="{ch['color']}" class="online-dot"/>
    </g>""")

    tiles_markup = "\n".join(tile_elements)

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
  <rect x="2" y="2" width="{width - 4}" height="{height - 4}" rx="16" fill="url(#connect_bgGradient)" stroke="url(#connect_borderGradient)" stroke-width="1.5" filter="url(#connect_cardShadow)"/>
  <rect x="2" y="2" width="{width - 4}" height="{height - 4}" rx="16" fill="url(#connect_ambientGlow)" pointer-events="none"/>

  <!-- Card Header -->
  <g transform="translate(30, 34)">
    <circle cx="6" cy="6" r="4" fill="{ACCENT_CYAN}"/>
    <text x="20" y="10" class="text-title" font-size="19" fill="{TEXT_HEADLINE}">
      CONNECT &amp; COLLABORATE
    </text>
    <text x="820" y="10" class="text-mono" font-size="10.5" fill="{TEXT_MUTED}" text-anchor="end">
      OPEN FOR NEW OPPORTUNITIES
    </text>
    <line x1="0" y1="20" x2="820" y2="20" stroke="{BORDER_BASE}" stroke-width="1"/>
  </g>

  <!-- Channels Grid -->
  {tiles_markup}
</svg>"""
