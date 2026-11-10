#!/usr/bin/env python3
"""
Fetch actual GitHub contribution data for Abu Sufiyan (Abbusufiyan).
Supports GitHub GraphQL API (authenticated) and public contributions HTML parsing (unauthenticated fallback).
Saves structured data into data/contributions.json.
"""

import os
import sys
import json
import re
import urllib.request
import urllib.error
from datetime import datetime, timezone

DEFAULT_USERNAME = "Abbusufiyan"
OUTPUT_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "contributions.json")


def fetch_via_graphql(username: str, token: str) -> dict:
    """Fetch contribution calendar using GitHub GraphQL API."""
    url = "https://api.github.com/graphql"
    query = """
    query($userName: String!) {
      user(login: $userName) {
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                contributionCount
                date
                weekday
                contributionLevel
              }
            }
          }
        }
      }
    }
    """
    data = json.dumps({"query": query, "variables": {"userName": username}}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "Abbusufiyan-Profile-Stats",
        },
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        result = json.loads(resp.read().decode("utf-8"))

    if "errors" in result:
        raise RuntimeError(f"GraphQL returned errors: {result['errors']}")

    calendar = result["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    return calendar


def fetch_via_html_scraping(username: str) -> dict:
    """Fetch public contributions HTML and parse calendar days & tooltips."""
    url = f"https://github.com/users/{username}/contributions"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml",
        },
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode("utf-8")

    # Extract tooltips for contribution counts
    tooltips = dict(re.findall(r'<tool-tip[^>]*for="([^"]+)"[^>]*>(.*?)</tool-tip>', html, re.DOTALL))

    # Match each contribution cell
    td_matches = re.finditer(r'<td\s+([^>]*class="[^"]*ContributionCalendar-day[^"]*"[^>]*)>', html)
    days = []

    for m in td_matches:
        attrs = m.group(1)
        date_m = re.search(r'data-date="([^"]+)"', attrs)
        level_m = re.search(r'data-level="([^"]+)"', attrs)
        id_m = re.search(r'id="([^"]+)"', attrs)
        if date_m and level_m:
            date_str = date_m.group(1)
            level = int(level_m.group(1))
            elem_id = id_m.group(1) if id_m else ""
            tt = tooltips.get(elem_id, "").strip()
            count_m = re.search(r'(\d+)\s+contribution', tt)
            count = int(count_m.group(1)) if count_m else 0
            # Weekday from date
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            # GitHub weekdays: 0 is Sunday, 6 is Saturday
            # Python dt.weekday(): 0 is Monday, 6 is Sunday
            gh_weekday = (dt.weekday() + 1) % 7
            days.append({
                "date": date_str,
                "contributionCount": count,
                "contributionLevel": level,
                "weekday": gh_weekday,
                "tooltip": tt,
            })

    days.sort(key=lambda x: x["date"])

    if not days:
        raise ValueError(f"No contribution cells found in HTML for user {username}")

    # Group into weeks (starting each Sunday)
    weeks = []
    current_week = []
    for d in days:
        if d["weekday"] == 0 and current_week:
            weeks.append({"contributionDays": current_week})
            current_week = []
        current_week.append({
            "date": d["date"],
            "contributionCount": d["contributionCount"],
            "contributionLevel": f"FIRST_QUARTILE" if d["contributionLevel"] == 1 else
                                 f"SECOND_QUARTILE" if d["contributionLevel"] == 2 else
                                 f"THIRD_QUARTILE" if d["contributionLevel"] == 3 else
                                 f"FOURTH_QUARTILE" if d["contributionLevel"] == 4 else "NONE",
            "level": d["contributionLevel"],
            "weekday": d["weekday"],
        })
    if current_week:
        weeks.append({"contributionDays": current_week})

    total_contributions = sum(d["contributionCount"] for d in days)

    return {
        "totalContributions": total_contributions,
        "weeks": weeks,
        "days": days,
    }


def compute_metrics(calendar: dict, username: str) -> dict:
    """Calculate streak, busiest day, monthly breakdown, and stats."""
    # Flatten days
    all_days = []
    if "days" in calendar and calendar["days"]:
        for d in calendar["days"]:
            count = d.get("contributionCount", 0)
            level = d.get("contributionLevel", 0)
            if isinstance(level, str):
                level_map = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}
                level = level_map.get(level, 0)
            all_days.append({
                "date": d["date"],
                "count": count,
                "level": level,
                "weekday": d.get("weekday", 0),
            })
    else:
        level_map = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}
        for w in calendar.get("weeks", []):
            for d in w.get("contributionDays", []):
                lvl = d.get("contributionLevel", 0)
                if isinstance(lvl, str):
                    lvl = level_map.get(lvl, 0)
                all_days.append({
                    "date": d["date"],
                    "count": d.get("contributionCount", 0),
                    "level": lvl,
                    "weekday": d.get("weekday", 0),
                })

    all_days.sort(key=lambda x: x["date"])

    total_contributions = calendar.get("totalContributions", sum(d["count"] for d in all_days))
    active_days = sum(1 for d in all_days if d["count"] > 0)
    busiest_day = max(all_days, key=lambda x: x["count"]) if all_days else {"date": "N/A", "count": 0}

    # Streaks calculation
    longest_streak = 0
    temp_streak = 0
    for d in all_days:
        if d["count"] > 0:
            temp_streak += 1
            if temp_streak > longest_streak:
                longest_streak = temp_streak
        else:
            temp_streak = 0

    # Current streak (standard GitHub streak handling)
    current_streak = 0
    for d in reversed(all_days):
        if d["count"] > 0:
            current_streak += 1
        else:
            # If current streak hasn't started and we're looking at today (count 0), allow checking yesterday
            if current_streak == 0:
                continue
            break

    # Monthly breakdown (last 12 months)
    month_counts = {}
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    for d in all_days:
        mk = d["date"][:7]  # YYYY-MM
        month_counts[mk] = month_counts.get(mk, 0) + d["count"]

    monthly_summary = []
    for mk in sorted(month_counts.keys()):
        parts = mk.split("-")
        y = parts[0]
        m_idx = int(parts[1]) - 1
        label = f"{month_names[m_idx]} {y[2:]}"
        monthly_summary.append({
            "key": mk,
            "label": label,
            "count": month_counts[mk],
        })

    # Keep only the last 12 months for visual balance if more exist
    if len(monthly_summary) > 12:
        monthly_summary = monthly_summary[-12:]

    # Group into normalized 53-week grid for heatmap
    # Week starts on Sunday
    weeks_grid = []
    # Index all days by date
    day_by_date = {d["date"]: d for d in all_days}
    if all_days:
        start_date = datetime.strptime(all_days[0]["date"], "%Y-%m-%d")
        end_date = datetime.strptime(all_days[-1]["date"], "%Y-%m-%d")
        # Pad backwards to preceding Sunday if needed
        # (dt.weekday() + 1) % 7 -> Sunday is 0
        from datetime import timedelta
        cur = start_date
        week = []
        while cur <= end_date:
            ds = cur.strftime("%Y-%m-%d")
            entry = day_by_date.get(ds, {"date": ds, "count": 0, "level": 0, "weekday": (cur.weekday() + 1) % 7})
            if (cur.weekday() + 1) % 7 == 0 and week:
                weeks_grid.append(week)
                week = []
            week.append(entry)
            cur += timedelta(days=1)
        if week:
            weeks_grid.append(week)

    return {
        "username": username,
        "total_contributions": total_contributions,
        "active_days": active_days,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "busiest_day": {
            "date": busiest_day.get("date", "N/A"),
            "count": busiest_day.get("count", 0),
        },
        "monthly_summary": monthly_summary,
        "weeks": weeks_grid,
        "total_days_tracked": len(all_days),
        "date_range": {
            "start": all_days[0]["date"] if all_days else None,
            "end": all_days[-1]["date"] if all_days else None,
        },
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }


def main():
    username = os.environ.get("GITHUB_ACTOR", DEFAULT_USERNAME)
    if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
        username = sys.argv[1]

    token = os.environ.get("GITHUB_TOKEN")

    print(f"[*] Fetching contribution data for user: {username}")
    calendar = None

    if token:
        try:
            print("[*] Attempting GitHub GraphQL API with GITHUB_TOKEN...")
            calendar = fetch_via_graphql(username, token)
            print("[✓] GraphQL fetch successful.")
        except Exception as e:
            print(f"[!] GraphQL fetch failed: {e}. Falling back to public scraping...")

    if not calendar:
        try:
            print("[*] Fetching from public GitHub contributions page...")
            calendar = fetch_via_html_scraping(username)
            print("[✓] Public HTML scraping successful.")
        except Exception as e:
            print(f"[!] Public scraping failed: {e}")
            if os.path.exists(OUTPUT_FILE):
                print(f"[*] Existing {OUTPUT_FILE} preserved as fallback.")
                sys.exit(0)
            else:
                print("[!] No cached data found. Exiting with error.")
                sys.exit(1)

    metrics = compute_metrics(calendar, username)

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    print(f"[✓] Saved contributions data to {OUTPUT_FILE}")
    print(f"    Total Contributions: {metrics['total_contributions']}")
    print(f"    Active Days: {metrics['active_days']}")
    print(f"    Current Streak: {metrics['current_streak']} days")
    print(f"    Longest Streak: {metrics['longest_streak']} days")
    print(f"    Busiest Day: {metrics['busiest_day']['date']} ({metrics['busiest_day']['count']} commits)")


if __name__ == "__main__":
    main()
