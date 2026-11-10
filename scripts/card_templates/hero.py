"""
Hero Card Generator for Abu Sufiyan.
Features premium serif typography for name, electric blue gradient animations,
terminal typing effect, and sleek cyber-geometric accents.
"""

from .theme import (
    BG_DARK, BG_CARD_START, BG_CARD_END, BORDER_BASE, BORDER_HIGHLIGHT,
    ACCENT_CYAN, ACCENT_SKY, ACCENT_BLUE, ACCENT_EMERALD,
    TEXT_HEADLINE, TEXT_BODY, TEXT_MUTED, TEXT_ACCENT,
    FONT_SERIF, FONT_SANS, FONT_MONO,
    get_common_defs, get_base_css
)


def render_hero_card(is_static: bool = False) -> str:
    """Generate the animated Hero SVG card."""
    width = 880
    height = 340

    defs = get_common_defs("hero")
    base_css = get_base_css(is_static)

    # Hero-specific animation CSS
    custom_css = "" if is_static else f"""
    @keyframes nameGlow {{
      0%, 100% {{ filter: drop-shadow(0 0 4px rgba(0, 240, 255, 0.4)); }}
      50% {{ filter: drop-shadow(0 0 14px rgba(0, 240, 255, 0.85)); }}
    }}

    @keyframes statusPulse {{
      0%, 100% {{ opacity: 0.8; transform: scale(1); }}
      50% {{ opacity: 0.3; transform: scale(0.85); }}
    }}

    @keyframes textShimmer {{
      0% {{ fill-opacity: 0.9; }}
      50% {{ fill-opacity: 1; }}
      100% {{ fill-opacity: 0.9; }}
    }}

    @keyframes borderTrace {{
      0% {{ stroke-dashoffset: 400; }}
      100% {{ stroke-dashoffset: 0; }}
    }}

    .hero-name {{
      animation: nameGlow 5s ease-in-out infinite;
    }}

    .status-dot {{
      animation: statusPulse 2s ease-in-out infinite;
      transform-origin: 45px 38px;
    }}

    .shimmer-text {{
      animation: textShimmer 3s ease-in-out infinite;
    }}
"""

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
  <rect x="2" y="2" width="{width - 4}" height="{height - 4}" rx="16" fill="url(#hero_bgGradient)" stroke="url(#hero_borderGradient)" stroke-width="1.5" filter="url(#hero_cardShadow)"/>
  <rect x="2" y="2" width="{width - 4}" height="{height - 4}" rx="16" fill="url(#hero_ambientGlow)" pointer-events="none"/>
  <rect x="2" y="2" width="{width - 4}" height="{height - 4}" rx="16" fill="url(#hero_techGrid)" pointer-events="none"/>

  <!-- Top System Header Bar -->
  <g class="text-mono" font-size="11" fill="{TEXT_MUTED}">
    <!-- Status Indicator -->
    <circle cx="45" cy="38" r="5" fill="{ACCENT_CYAN}" opacity="0.3"/>
    <circle cx="45" cy="38" r="3.2" fill="{ACCENT_CYAN}" class="status-dot"/>
    <text x="58" y="42" font-weight="600" fill="{ACCENT_CYAN}" letter-spacing="0.08em">SYSTEM ACTIVE</text>
    <text x="180" y="42" fill="{TEXT_MUTED}" opacity="0.5">|</text>
    <text x="195" y="42" fill="{TEXT_BODY}">ROLE: FULL-STACK &amp; SYSTEMS</text>

    <!-- Right Header Telemetry -->
    <text x="835" y="42" text-anchor="end" fill="{TEXT_MUTED}">CORE :: LINUX x86_64</text>
    <line x1="30" y1="58" x2="850" y2="58" stroke="{BORDER_BASE}" stroke-width="1"/>
  </g>

  <!-- Corner Tech Crosshairs -->
  <g stroke="{ACCENT_CYAN}" stroke-width="1" opacity="0.4">
    <path d="M 20 25 L 20 18 L 27 18"/>
    <path d="M 860 25 L 860 18 L 853 18"/>
    <path d="M 20 315 L 20 322 L 27 322"/>
    <path d="M 860 315 L 860 322 L 853 322"/>
  </g>

  <!-- Primary Headline Section -->
  <!-- Name with Serif Elegance -->
  <g transform="translate(45, 118)">
    <text class="text-title hero-name" font-size="46" fill="{TEXT_HEADLINE}">
      ABU SUFIYAN
    </text>
    <!-- Cyan Shimmer Accent bar below name -->
    <rect x="2" y="14" width="220" height="3" rx="1.5" fill="url(#hero_accentGradient)"/>
    <circle cx="232" cy="15.5" r="2.5" fill="{ACCENT_CYAN}"/>
  </g>

  <!-- Title / Designation -->
  <g transform="translate(46, 168)" class="text-sans">
    <text font-size="15" font-weight="600" fill="{ACCENT_SKY}" letter-spacing="0.12em">
      SOFTWARE DEVELOPER <tspan fill="{TEXT_MUTED}">|</tspan> SOFTWARE ENGINEERING STUDENT
    </text>
  </g>

  <!-- Terminal Console Box -->
  <g transform="translate(45, 192)">
    <!-- Terminal Background -->
    <rect x="0" y="0" width="790" height="114" rx="10" fill="#050811" stroke="{BORDER_BASE}" stroke-width="1"/>

    <!-- Terminal Window Controls -->
    <circle cx="18" cy="18" r="4.5" fill="#ef4444" opacity="0.75"/>
    <circle cx="34" cy="18" r="4.5" fill="#f59e0b" opacity="0.75"/>
    <circle cx="50" cy="18" r="4.5" fill="#10b981" opacity="0.75"/>
    <text x="75" y="22" class="text-mono" font-size="11" fill="{TEXT_MUTED}">bash — dev-profile — 80x24</text>
    <line x1="0" y1="34" x2="790" y2="34" stroke="{BORDER_BASE}" stroke-width="0.8"/>

    <!-- Terminal Content -->
    <g class="text-mono" font-size="12">
      <!-- Command prompt -->
      <text x="20" y="56" fill="{ACCENT_CYAN}" font-weight="600">$</text>
      <text x="36" y="56" fill="{TEXT_HEADLINE}">sufiyan --info</text>
      <text x="170" y="56" fill="{TEXT_MUTED}">--target production</text>

      <!-- Output Line 1 -->
      <text x="20" y="78" fill="{TEXT_BODY}">
        &gt; Architecting scalable web applications, interactive 3D WebGL experiences &amp; native Linux utilities.
      </text>

      <!-- Output Line 2 with typing cursor -->
      <text x="20" y="99" fill="{TEXT_MUTED}">
        &gt; Core Stack: <tspan fill="{ACCENT_SKY}">React</tspan> • <tspan fill="{ACCENT_SKY}">TypeScript</tspan> • <tspan fill="{ACCENT_SKY}">Node.js</tspan> • <tspan fill="{ACCENT_SKY}">C++</tspan> • <tspan fill="{ACCENT_SKY}">Three.js</tspan> • <tspan fill="{ACCENT_SKY}">Tailwind</tspan>
      </text>
      <rect x="475" y="87" width="8" height="14" fill="{ACCENT_CYAN}" class="cursor-blink"/>
    </g>
  </g>

  <!-- Right Geometric Tech Emblem -->
  <g transform="translate(735, 78)">
    <!-- Tech Insignia Hexagon Wireframe -->
    <polygon points="45,0 90,26 90,78 45,104 0,78 0,26" fill="#091224" stroke="{ACCENT_CYAN}" stroke-width="1.2" opacity="0.7"/>
    <polygon points="45,10 78,29 78,69 45,88 12,69 12,29" fill="none" stroke="{ACCENT_SKY}" stroke-width="0.8" opacity="0.4" stroke-dasharray="3,3"/>
    
    <!-- Monogram AS in Serif -->
    <text x="45" y="58" class="text-title" font-size="22" font-weight="700" fill="{TEXT_HEADLINE}" text-anchor="middle" letter-spacing="0.1em">
      AS
    </text>
    <text x="45" y="74" class="text-mono" font-size="8.5" fill="{ACCENT_CYAN}" text-anchor="middle" letter-spacing="0.18em">
      DEV // 2026
    </text>
  </g>
</svg>"""
