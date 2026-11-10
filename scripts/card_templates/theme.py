"""
Shared Theme and Design System for Abu Sufiyan's Animated README Cards.
Electric Blue & Deep Cosmic Navy aesthetic with premium serif typography.
"""

# Color Palette
BG_DARK = "#060913"
BG_CARD_START = "#0b1224"
BG_CARD_END = "#060a16"
BORDER_BASE = "#152238"
BORDER_HIGHLIGHT = "#00f0ff"

# Accent Colors
ACCENT_CYAN = "#00f0ff"       # Electric Cyan
ACCENT_SKY = "#38bdf8"        # Sky Blue
ACCENT_BLUE = "#3b82f6"       # Core Blue
ACCENT_ROYAL = "#1d4ed8"      # Deep Blue
ACCENT_EMERALD = "#10b981"    # Operational Green
ACCENT_AMBER = "#f59e0b"      # Alert Amber

# Text Colors
TEXT_HEADLINE = "#f8fafc"     # Crisp White
TEXT_BODY = "#94a3b8"         # Cool Slate
TEXT_MUTED = "#64748b"        # Muted Slate
TEXT_ACCENT = "#38bdf8"       # Accent Cyan Slate

# Typography Stacks
FONT_SERIF = "'Cinzel', 'Playfair Display', 'Cormorant Garamond', 'Georgia', serif"
FONT_SANS = "'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
FONT_MONO = "'JetBrains Mono', 'Fira Code', 'SF Mono', Consolas, 'Courier New', monospace"


def xml_escape(text: str) -> str:
    """Safely escape text for XML/SVG rendering."""
    if not isinstance(text, str):
        return str(text)
    # Avoid double escaping already escaped entities
    text = text.replace("&amp;", "&")
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )



def get_common_defs(prefix: str = "") -> str:
    """Return reusable SVG gradients, filters, and patterns."""
    p = f"{prefix}_" if prefix else ""
    return f"""
  <defs>
    <!-- Background Card Gradient -->
    <linearGradient id="{p}bgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{BG_CARD_START}"/>
      <stop offset="100%" stop-color="{BG_CARD_END}"/>
    </linearGradient>

    <!-- Electric Accent Gradient -->
    <linearGradient id="{p}accentGradient" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{ACCENT_CYAN}"/>
      <stop offset="50%" stop-color="{ACCENT_SKY}"/>
      <stop offset="100%" stop-color="{ACCENT_BLUE}"/>
    </linearGradient>

    <!-- Glowing Accent Gradient for Border -->
    <linearGradient id="{p}borderGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{ACCENT_CYAN}" stop-opacity="0.6"/>
      <stop offset="30%" stop-color="{BORDER_BASE}" stop-opacity="0.8"/>
      <stop offset="70%" stop-color="{BORDER_BASE}" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="{ACCENT_SKY}" stop-opacity="0.4"/>
    </linearGradient>

    <!-- Subtle Cyan Ambient Radial Glow -->
    <radialGradient id="{p}ambientGlow" cx="20%" cy="15%" r="65%">
      <stop offset="0%" stop-color="{ACCENT_CYAN}" stop-opacity="0.12"/>
      <stop offset="50%" stop-color="{ACCENT_BLUE}" stop-opacity="0.04"/>
      <stop offset="100%" stop-color="{BG_DARK}" stop-opacity="0"/>
    </radialGradient>

    <!-- Cyan Glow Filter -->
    <filter id="{p}cyanGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <!-- Subtle Drop Shadow -->
    <filter id="{p}cardShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#000000" flood-opacity="0.5"/>
    </filter>

    <!-- Tech Grid Pattern -->
    <pattern id="{p}techGrid" width="24" height="24" patternUnits="userSpaceOnUse">
      <path d="M 24 0 L 0 0 0 24" fill="none" stroke="{ACCENT_CYAN}" stroke-opacity="0.03" stroke-width="0.8"/>
      <circle cx="24" cy="24" r="0.75" fill="{ACCENT_CYAN}" fill-opacity="0.08"/>
    </pattern>
  </defs>
"""


def get_base_css(is_static: bool = False) -> str:
    """Return common CSS styles and animation rules."""
    if is_static:
        return f"""
    * {{
      animation: none !important;
      transition: none !important;
      opacity: 1 !important;
    }}
    .animated-pulse, .cursor-blink, .shimmer, .reveal-text, .meter-fill, .float-dot {{
      animation: none !important;
      opacity: 1 !important;
    }}
    @media (prefers-reduced-motion: reduce) {{
      * {{ animation: none !important; }}
    }}
"""
    return f"""
    @keyframes pulseGlow {{
      0%, 100% {{ opacity: 0.7; transform: scale(1); }}
      50% {{ opacity: 1; transform: scale(1.02); }}
    }}

    @keyframes gradientShift {{
      0% {{ stop-color: {ACCENT_CYAN}; }}
      50% {{ stop-color: {ACCENT_SKY}; }}
      100% {{ stop-color: {ACCENT_CYAN}; }}
    }}

    @keyframes cursorBlink {{
      0%, 49% {{ opacity: 1; }}
      50%, 100% {{ opacity: 0; }}
    }}

    @keyframes scanline {{
      0% {{ transform: translateY(-100%); }}
      100% {{ transform: translateY(1000%); }}
    }}

    @keyframes shimmerMove {{
      0% {{ transform: translateX(-100%); }}
      100% {{ transform: translateX(200%); }}
    }}

    @keyframes fadeIn {{
      0% {{ opacity: 0; transform: translateY(6px); }}
      100% {{ opacity: 1; transform: translateY(0); }}
    }}

    @keyframes floatGentle {{
      0%, 100% {{ transform: translateY(0px); }}
      50% {{ transform: translateY(-3px); }}
    }}

    .cursor-blink {{
      animation: cursorBlink 1.1s infinite steps(1);
    }}

    .animated-pulse {{
      animation: pulseGlow 4s ease-in-out infinite;
    }}

    .float-item {{
      animation: floatGentle 5s ease-in-out infinite;
    }}

    @media (prefers-reduced-motion: reduce) {{
      *, .cursor-blink, .animated-pulse, .float-item {{
        animation: none !important;
        transition: none !important;
      }}
    }}
"""
