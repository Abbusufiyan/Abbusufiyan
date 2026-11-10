"""
Contribution Activity Card Generator for Abu Sufiyan.
Displays actual GitHub contribution metrics:
Total contributions, Active days, Current streak, Longest streak, Busiest day, and Monthly breakdown.
"""

from .theme import (
    BG_DARK, BG_CARD_START, BG_CARD_END, BORDER_BASE, BORDER_HIGHLIGHT,
    ACCENT_CYAN, ACCENT_SKY, ACCENT_BLUE, ACCENT_EMERALD, ACCENT_AMBER,
    TEXT_HEADLINE, TEXT_BODY, TEXT_MUTED, TEXT_ACCENT,
    FONT_SERIF, FONT_SANS, FONT_MONO,
    get_common_defs, get_base_css
)


def render_stats_card(metrics: dict, is_static: bool = False) -> str:
    """Generate the animated Contribution Stats SVG card."""
    width = 880
    height = 290

    defs = get_common_defs("stats")
    base_css = get_base_css(is_static)

    # Safely extract metrics
    total = metrics.get("total_contributions", 0)
    active_days = metrics.get("active_days", 0)
    cur_streak = metrics.get("current_streak", 0)
    max_streak = metrics.get("longest_streak", 0)
    busiest = metrics.get("busiest_day", {"date": "N/A", "count": 0})
    busiest_date = busiest.get("date", "N/A")
    busiest_count = busiest.get("count", 0)
    monthly = metrics.get("monthly_summary", [])

    # Format busiest date e.g. 2026-11-08 -> Nov 8, 2026
    if busiest_date and busiest_date != "N/A" and "-" in busiest_date:
        parts = busiest_date.split("-")
        month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        try:
            m_idx = int(parts[1]) - 1
            busiest_display = f"{month_names[m_idx]} {int(parts[2])}"
        except Exception:
            busiest_display = busiest_date
    else:
        busiest_display = "N/A"

    custom_css = "" if is_static else f"""
    @keyframes barRise {{
      from {{ transform: scaleY(0.05); }}
      to {{ transform: scaleY(1); }}
    }}

    @keyframes statGlow {{
      0%, 100% {{ filter: drop-shadow(0 0 3px rgba(0, 240, 255, 0.3)); }}
      50% {{ filter: drop-shadow(0 0 8px rgba(0, 240, 255, 0.7)); }}
    }}

    .metric-value {{
      animation: statGlow 4s ease-in-out infinite;
    }}

    .chart-bar {{
      transform-origin: bottom;
      animation: barRise 1.2s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }}
"""

    # 5 KPI telemetry cards
    kpis = [
        {"label": "TOTAL COMMITS", "value": f"{total}", "sub": "Last 12 Months", "color": ACCENT_CYAN},
        {"label": "ACTIVE DAYS", "value": f"{active_days}", "sub": "Commit Days", "color": ACCENT_SKY},
        {"label": "CURRENT STREAK", "value": f"{cur_streak}d", "sub": "Consistent Activity", "color": ACCENT_EMERALD if cur_streak > 0 else TEXT_MUTED},
        {"label": "LONGEST STREAK", "value": f"{max_streak}d", "sub": "Peak Continuity", "color": ACCENT_AMBER},
        {"label": "BUSIEST DAY", "value": f"{busiest_count}", "sub": busiest_display, "color": ACCENT_CYAN},
    ]

    kpi_svgs = []
    card_w = 156
    gap = 8
    start_x = 30
    for i, k in enumerate(kpis):
        kx = start_x + i * (card_w + gap)
        kpi_svgs.append(f"""
    <!-- KPI: {k['label']} -->
    <g transform="translate({kx}, 66)">
      <rect x="0" y="0" width="{card_w}" height="80" rx="8" fill="#070c18" stroke="{BORDER_BASE}" stroke-width="1"/>
      <rect x="0" y="0" width="{card_w}" height="2" rx="1" fill="{k['color']}" opacity="0.8"/>
      <text x="12" y="22" class="text-mono" font-size="9" fill="{TEXT_MUTED}" letter-spacing="0.08em">{k['label']}</text>
      <text x="12" y="52" class="text-mono metric-value" font-size="22" font-weight="700" fill="{k['color']}">{k['value']}</text>
      <text x="12" y="68" class="text-sans" font-size="9.5" fill="{TEXT_MUTED}">{k['sub']}</text>
    </g>""")

    # Monthly breakdown bar chart
    # Height of bar chart area = 70px, Y base = 250
    chart_y_base = 250
    chart_max_h = 58
    max_month_val = max([m["count"] for m in monthly] + [1])

    bars_svg = []
    bar_slot_w = (width - 60) / max(len(monthly), 1)
    bar_width = min(28, bar_slot_w - 14)

    for i, m in enumerate(monthly):
        bx = start_x + i * bar_slot_w + (bar_slot_w - bar_width) / 2
        cnt = m["count"]
        bar_h = max(3, int((cnt / max_month_val) * chart_max_h)) if cnt > 0 else 3
        by = chart_y_base - bar_h

        bar_color = ACCENT_CYAN if cnt > 30 else ACCENT_SKY if cnt > 10 else ACCENT_BLUE if cnt > 0 else "#10192e"
        bar_opacity = "1" if cnt > 0 else "0.4"

        # Show count if > 0
        count_label = f"""<text x="{bx + bar_width / 2}" y="{by - 4}" class="text-mono" font-size="8.5" fill="{ACCENT_CYAN}" text-anchor="middle">{cnt}</text>""" if cnt > 0 else ""

        bars_svg.append(f"""
      <!-- Month: {m['label']} -->
      {count_label}
      <rect x="{bx}" y="{by}" width="{bar_width}" height="{bar_h}" rx="3" fill="{bar_color}" opacity="{bar_opacity}" class="chart-bar"/>
      <text x="{bx + bar_width / 2}" y="{chart_y_base + 16}" class="text-mono" font-size="9" fill="{TEXT_MUTED}" text-anchor="middle">{m['label']}</text>""")

    chart_markup = "\n".join(bars_svg)

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
  <rect x="2" y="2" width="{width - 4}" height="{height - 4}" rx="16" fill="url(#stats_bgGradient)" stroke="url(#stats_borderGradient)" stroke-width="1.5" filter="url(#stats_cardShadow)"/>
  <rect x="2" y="2" width="{width - 4}" height="{height - 4}" rx="16" fill="url(#stats_ambientGlow)" pointer-events="none"/>

  <!-- Card Header -->
  <g transform="translate(30, 34)">
    <circle cx="6" cy="6" r="4" fill="{ACCENT_CYAN}"/>
    <text x="20" y="10" class="text-title" font-size="19" fill="{TEXT_HEADLINE}">
      CONTRIBUTION ACTIVITY &amp; METRICS
    </text>
    <text x="820" y="10" class="text-mono" font-size="10.5" fill="{TEXT_MUTED}" text-anchor="end">
      LIVE TELEMETRY // REAL GITHUB DATA
    </text>
    <line x1="0" y1="20" x2="820" y2="20" stroke="{BORDER_BASE}" stroke-width="1"/>
  </g>

  <!-- KPI Cards Row -->
  {chr(10).join(kpi_svgs)}

  <!-- Monthly Breakdown Chart -->
  <g>
    <!-- Chart baseline -->
    <line x1="{start_x}" y1="{chart_y_base}" x2="{width - start_x}" y2="{chart_y_base}" stroke="{BORDER_BASE}" stroke-width="1"/>
    {chart_markup}
  </g>
</svg>"""
