"""
Contribution Heatmap Card Generator for Abu Sufiyan.
53-week GitHub-style contribution graph styled with electric blue theme.
Uses actual contribution data with square cells and tooltips.
"""

from datetime import datetime
from .theme import (
    BG_DARK, BG_CARD_START, BG_CARD_END, BORDER_BASE, BORDER_HIGHLIGHT,
    ACCENT_CYAN, ACCENT_SKY, ACCENT_BLUE, ACCENT_ROYAL,
    TEXT_HEADLINE, TEXT_BODY, TEXT_MUTED, TEXT_ACCENT,
    FONT_SERIF, FONT_SANS, FONT_MONO,
    get_common_defs, get_base_css
)

# Heatmap Palette (Level 0 - 4)
COLOR_LEVEL_0 = "#0d1527"
COLOR_LEVEL_1 = "#1d4ed8"
COLOR_LEVEL_2 = "#0284c7"
COLOR_LEVEL_3 = "#38bdf8"
COLOR_LEVEL_4 = "#00f0ff"

LEVEL_COLORS = {
    0: COLOR_LEVEL_0,
    1: COLOR_LEVEL_1,
    2: COLOR_LEVEL_2,
    3: COLOR_LEVEL_3,
    4: COLOR_LEVEL_4,
}


def render_heatmap_card(metrics: dict, is_static: bool = False) -> str:
    """Generate the animated Contribution Heatmap SVG card."""
    width = 880
    height = 240

    defs = get_common_defs("heatmap")
    base_css = get_base_css(is_static)

    total = metrics.get("total_contributions", 0)
    weeks = metrics.get("weeks", [])

    custom_css = "" if is_static else f"""
    @keyframes cellPop {{
      0% {{ opacity: 0; transform: scale(0.5); }}
      100% {{ opacity: 1; transform: scale(1); }}
    }}

    .heatmap-cell {{
      transform-origin: center;
      animation: cellPop 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }}
"""

    # Grid parameters
    cell_size = 11
    cell_gap = 3.5
    grid_start_x = 56
    grid_start_y = 80

    # Calculate month header positions
    month_headers = []
    seen_months = set()
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    for col_idx, week in enumerate(weeks):
        for day in week:
            dt = datetime.strptime(day["date"], "%Y-%m-%d")
            # If 1st day of month or first week
            if dt.day <= 7:
                m_key = f"{dt.year}-{dt.month}"
                if m_key not in seen_months:
                    seen_months.add(m_key)
                    mx = grid_start_x + col_idx * (cell_size + cell_gap)
                    month_headers.append((mx, month_names[dt.month - 1]))
                    break

    month_svg = "\n".join([
        f'<text x="{mx}" y="{grid_start_y - 8}" class="text-mono" font-size="9" fill="{TEXT_MUTED}">{mname}</text>'
        for mx, mname in month_headers
    ])

    # Weekday labels (Mon, Wed, Fri) -> rows 1, 3, 5 (0 is Sun)
    weekday_labels = [
        (1, "Mon"),
        (3, "Wed"),
        (5, "Fri"),
    ]
    weekday_svg = "\n".join([
        f'<text x="{grid_start_x - 10}" y="{grid_start_y + row * (cell_size + cell_gap) + 9}" class="text-mono" font-size="8.5" fill="{TEXT_MUTED}" text-anchor="end">{label}</text>'
        for row, label in weekday_labels
    ])

    # Generate cells
    cell_elements = []
    for col_idx, week in enumerate(weeks):
        for day in week:
            # weekday: 0 is Sun, 6 is Sat
            row_idx = day.get("weekday", 0)
            cx = grid_start_x + col_idx * (cell_size + cell_gap)
            cy = grid_start_y + row_idx * (cell_size + cell_gap)
            lvl = day.get("level", 0)
            cnt = day.get("count", 0)
            date_str = day.get("date", "")
            fill_color = LEVEL_COLORS.get(lvl, COLOR_LEVEL_0)

            # Border for empty cells or glow for level 4
            stroke = f'stroke="{ACCENT_CYAN}" stroke-width="0.7"' if lvl == 4 else f'stroke="{BORDER_BASE}" stroke-width="0.5"' if lvl == 0 else ""
            anim_delay = f'style="animation-delay: {col_idx * 15}ms;"' if not is_static else ""

            cell_elements.append(f"""
      <rect x="{cx}" y="{cy}" width="{cell_size}" height="{cell_size}" rx="2.5" fill="{fill_color}" {stroke} class="heatmap-cell" {anim_delay}>
        <title>{cnt} contribution{'s' if cnt != 1 else ''} on {date_str}</title>
      </rect>""")

    cells_markup = "\n".join(cell_elements)

    # Legend elements at bottom right
    legend_start_x = width - 180
    legend_y = grid_start_y + 7 * (cell_size + cell_gap) + 14
    legend_swatches = []
    for i in range(5):
        lx = legend_start_x + 36 + i * (cell_size + 3)
        legend_swatches.append(f'<rect x="{lx}" y="{legend_y - 9}" width="{cell_size}" height="{cell_size}" rx="2" fill="{LEVEL_COLORS[i]}" stroke="{BORDER_BASE}" stroke-width="0.5"/>')

    legend_markup = f"""
    <g class="text-mono" font-size="9" fill="{TEXT_MUTED}">
      <text x="{legend_start_x + 8}" y="{legend_y}">Less</text>
      {''.join(legend_swatches)}
      <text x="{legend_start_x + 36 + 5 * (cell_size + 3) + 6}" y="{legend_y}">More</text>
    </g>
"""

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
  <rect x="2" y="2" width="{width - 4}" height="{height - 4}" rx="16" fill="url(#heatmap_bgGradient)" stroke="url(#heatmap_borderGradient)" stroke-width="1.5" filter="url(#heatmap_cardShadow)"/>
  <rect x="2" y="2" width="{width - 4}" height="{height - 4}" rx="16" fill="url(#heatmap_ambientGlow)" pointer-events="none"/>

  <!-- Card Header -->
  <g transform="translate(30, 32)">
    <circle cx="6" cy="6" r="4" fill="{ACCENT_CYAN}"/>
    <text x="20" y="10" class="text-title" font-size="19" fill="{TEXT_HEADLINE}">
      ANNUAL CONTRIBUTION MATRIX
    </text>
    <text x="820" y="10" class="text-mono" font-size="10.5" fill="{TEXT_MUTED}" text-anchor="end">
      {total} CONTRIBUTIONS // 53-WEEK TIMELINE
    </text>
    <line x1="0" y1="20" x2="820" y2="20" stroke="{BORDER_BASE}" stroke-width="1"/>
  </g>

  <!-- Heatmap Grid -->
  <g>
    <!-- Month Labels -->
    {month_svg}
    <!-- Weekday Labels -->
    {weekday_svg}
    <!-- Contribution Cells -->
    {cells_markup}
    <!-- Legend -->
    {legend_markup}
  </g>
</svg>"""
