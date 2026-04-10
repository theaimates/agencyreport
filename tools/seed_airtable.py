"""
seed_airtable.py — Seed Airtable with ReportFlow mock data

Usage:
    python tools/seed_airtable.py

What it does:
    1. Creates/upserts 3 clients in the Clients table
    2. Creates KPI Snapshot rows for each client (last 14 days)
    3. Creates Revenue rows for each client (last 4 weeks)
    4. Creates Channel Performance rows for each client
    5. Creates one AI Summary (Draft) per client

Requires in .env:
    AIRTABLE_BASE_ID=appXXXXXXXXXXXXXX
    AIRTABLE_API_KEY=patXXXXXXXXXXXXXX

All writes use Airtable's upsert endpoint (merge on a key field) so
this script is safe to run multiple times — it won't create duplicates.
"""

import os
import sys
import json
import time
from datetime import date, timedelta

try:
    import requests
except ImportError:
    print("ERROR: 'requests' is not installed. Run: pip install requests")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not installed — fall back to reading .env manually
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    os.environ.setdefault(k.strip(), v.strip())

# ── Config ──────────────────────────────────────────────────────────────────

BASE_ID = os.environ.get('AIRTABLE_BASE_ID', '').strip()
API_KEY = os.environ.get('AIRTABLE_API_KEY', '').strip()

if not BASE_ID or BASE_ID == 'appXXXXXXXXXXXXXX':
    print("ERROR: AIRTABLE_BASE_ID not set in .env")
    sys.exit(1)
if not API_KEY:
    print("ERROR: AIRTABLE_API_KEY not set in .env")
    sys.exit(1)

BASE_URL = f"https://api.airtable.com/v0/{BASE_ID}"
HEADERS  = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

TODAY = date.today()


# ── Airtable helpers ─────────────────────────────────────────────────────────

def airtable_create(table: str, records: list) -> list:
    """Create up to 10 records at once. Returns list of created record IDs."""
    created = []
    for i in range(0, len(records), 10):
        batch = records[i:i+10]
        resp = requests.post(
            f"{BASE_URL}/{table}",
            headers=HEADERS,
            json={"records": [{"fields": r} for r in batch]}
        )
        if not resp.ok:
            print(f"  ERROR creating in {table}: {resp.status_code} {resp.text[:200]}")
            return created
        created += [r["id"] for r in resp.json().get("records", [])]
        time.sleep(0.25)  # Airtable rate limit: 5 requests/sec
    return created


def airtable_upsert(table: str, records: list, key_field: str) -> int:
    """Upsert records by key_field. Returns number of records touched."""
    touched = 0
    for i in range(0, len(records), 10):
        batch = records[i:i+10]
        resp = requests.patch(
            f"{BASE_URL}/{table}",
            headers=HEADERS,
            json={
                "performUpsert": {"fieldsToMergeOn": [key_field]},
                "records": [{"fields": r} for r in batch]
            }
        )
        if not resp.ok:
            print(f"  ERROR upserting in {table}: {resp.status_code} {resp.text[:200]}")
            return touched
        touched += len(resp.json().get("records", []))
        time.sleep(0.25)
    return touched


def clear_table(table: str):
    """Delete all records in a table (use with care — only for seeding)."""
    resp = requests.get(f"{BASE_URL}/{table}?pageSize=100", headers=HEADERS)
    if not resp.ok:
        return
    records = resp.json().get("records", [])
    ids = [r["id"] for r in records]
    for i in range(0, len(ids), 10):
        batch = ids[i:i+10]
        params = "&".join(f"records[]={rid}" for rid in batch)
        requests.delete(f"{BASE_URL}/{table}?{params}", headers=HEADERS)
        time.sleep(0.25)


# ── Mock data ────────────────────────────────────────────────────────────────

CLIENTS = [
    {
        "client_id":             "brightedge",
        "company_name":          "BrightEdge Digital",
        "niche":                 "E-commerce",
        "brand_color":           "#6366f1",
        "contact_email":         "hello@brightedge.example.com",
        "status":                "Active",
        "ga4_property_id":       "GA4-DEMO-001",
        "meta_ad_account_id":    "ACT_DEMO_001",
        "google_ads_customer_id":"DEMO-001-001",
    },
    {
        "client_id":             "nova",
        "company_name":          "NovaTech Solutions",
        "niche":                 "SaaS",
        "brand_color":           "#3ecf8e",
        "contact_email":         "hello@novatech.example.com",
        "status":                "Active",
        "ga4_property_id":       "GA4-DEMO-002",
        "meta_ad_account_id":    "ACT_DEMO_002",
        "google_ads_customer_id":"DEMO-002-001",
    },
    {
        "client_id":             "elevate",
        "company_name":          "Elevate Coaching",
        "niche":                 "Coaching & Courses",
        "brand_color":           "#f59e0b",
        "contact_email":         "hello@elevate.example.com",
        "status":                "Active",
        "ga4_property_id":       "GA4-DEMO-003",
        "meta_ad_account_id":    "ACT_DEMO_003",
        "google_ads_customer_id":"DEMO-003-001",
    },
]

# KPI data per client: (total_revenue, ad_spend, roas, conversion_rate, total_orders, total_sessions, avg_order_value)
CLIENT_KPIS = {
    "brightedge": (187420, 42180, 4.44, 4.8, 1840, 38330, 101.8),
    "nova":       (94200,  28400, 3.32, 3.2,  890, 27810, 105.8),
    "elevate":    (52800,  12600, 4.19, 6.1,  642,  10524,  82.2),
}

# Revenue per client per channel (channel, weekly_revenue, transactions)
CLIENT_REVENUE = {
    "brightedge": [
        ("Meta Ads",   15740, 154),
        ("Google Ads", 10494,  98),
        ("Email",       6747,  68),
        ("Organic",     4498,  44),
    ],
    "nova": [
        ("Google Ads",  9043,  86),
        ("LinkedIn",    4898,  46),
        ("Content/SEO", 3014,  28),
        ("Email",       1884,  18),
    ],
    "elevate": [
        ("Instagram Ads", 4013, 48),
        ("YouTube",       2957, 36),
        ("Email Funnels", 2323, 28),
        ("Referral",      1267, 16),
    ],
}

# Channel performance per client
CLIENT_CHANNELS = {
    "brightedge": [
        {"channel":"Meta Ads",  "total_revenue":78716,"total_spend":15140,"roas":5.2,"bar_width_pct":87,"trend":"↑ Growing",   "total_transactions":772},
        {"channel":"Google Ads","total_revenue":52478,"total_spend":13810,"roas":3.8,"bar_width_pct":63,"trend":"→ Stable",    "total_transactions":514},
        {"channel":"Email",     "total_revenue":33736,"total_spend": 1200,"roas":28.1,"bar_width_pct":56,"trend":"↑ Growing",  "total_transactions":330},
        {"channel":"Organic",   "total_revenue":22490,"total_spend":    0,"roas":0,  "bar_width_pct":37,"trend":"→ Stable",   "total_transactions":224},
    ],
    "nova": [
        {"channel":"Google Ads",  "total_revenue":45216,"total_spend":11900,"roas":3.8,"bar_width_pct":82,"trend":"↑ Growing","total_transactions":428},
        {"channel":"LinkedIn",    "total_revenue":24492,"total_spend": 9420,"roas":2.6,"bar_width_pct":53,"trend":"→ Stable", "total_transactions":232},
        {"channel":"Content/SEO", "total_revenue":15072,"total_spend": 2100,"roas":7.2,"bar_width_pct":33,"trend":"↑ Growing","total_transactions":142},
        {"channel":"Email",       "total_revenue": 9420,"total_spend":  600,"roas":15.7,"bar_width_pct":20,"trend":"→ Stable","total_transactions": 88},
    ],
    "elevate": [
        {"channel":"Instagram Ads","total_revenue":20064,"total_spend":4180,"roas":4.8,"bar_width_pct":78,"trend":"↑ Growing","total_transactions":244},
        {"channel":"YouTube",      "total_revenue":14784,"total_spend":4350,"roas":3.4,"bar_width_pct":58,"trend":"→ Stable", "total_transactions":180},
        {"channel":"Email Funnels","total_revenue":11616,"total_spend": 600,"roas":19.4,"bar_width_pct":45,"trend":"↑ Growing","total_transactions":142},
        {"channel":"Referral",     "total_revenue": 6336,"total_spend":   0,"roas":0,  "bar_width_pct":25,"trend":"↑ Growing","total_transactions": 76},
    ],
}

AI_SUMMARIES = {
    "brightedge": {
        "body_html": "<p>March was a <strong>breakout month</strong> for BrightEdge Digital. Revenue hit $187,420 — a 32.1% increase over February — while ad spend decreased 8.4%, pushing ROAS from 3.52x to 4.44x.</p>",
        "insight_1_type":"win",  "insight_1_title":"Biggest Win",  "insight_1_text":"Spring Collection Launch drove 28% of total revenue on 20% of ad spend.",
        "insight_2_type":"watch","insight_2_title":"Watch Closely","insight_2_text":"Google Generic Keywords paused — $4,510 budget needs reallocation.",
        "insight_3_type":"next", "insight_3_title":"Next Move",    "insight_3_text":"Scale Shopping Ads budget by 40% and test new email segments.",
    },
    "nova": {
        "body_html": "<p>NovaTech had a <strong>solid March</strong> with $94,200 in revenue — up 18.5% month-over-month. Google Ads remains the primary driver at 48% of revenue.</p>",
        "insight_1_type":"win",  "insight_1_title":"Biggest Win",  "insight_1_text":"Blog SEO generated $15k on $2.1k spend — 7.18x ROAS with compounding value.",
        "insight_2_type":"watch","insight_2_title":"Watch Closely","insight_2_text":"LinkedIn CPC at $1.50+ is above industry average. Needs creative refresh.",
        "insight_3_type":"next", "insight_3_title":"Next Move",    "insight_3_text":"Scale content budget 2x and test LinkedIn video ads to lower CPC.",
    },
    "elevate": {
        "body_html": "<p>Elevate Coaching had its <strong>best month ever</strong> — $52,800 in revenue, a 44.2% jump from February. Instagram Reels testimonial campaign was the star.</p>",
        "insight_1_type":"win",  "insight_1_title":"Biggest Win",  "insight_1_text":"Webinar funnel hit 34x ROAS — email automation is this business's superpower.",
        "insight_2_type":"watch","insight_2_title":"Watch Closely","insight_2_text":"YouTube pre-roll CTR is declining. Creative fatigue setting in.",
        "insight_3_type":"next", "insight_3_title":"Next Move",    "insight_3_text":"Launch a formal referral program and double the webinar funnel frequency.",
    },
}


# ── Seed functions ────────────────────────────────────────────────────────────

def seed_clients():
    print("\n[1/5] Seeding Clients...")
    n = airtable_upsert("Clients", CLIENTS, "client_id")
    print(f"      ✓ {n} client(s) upserted")


def seed_kpi_snapshots():
    print("\n[2/5] Seeding KPI Snapshots (last 14 days)...")
    records = []
    for client_id, (rev, spend, roas, conv, orders, sessions, aov) in CLIENT_KPIS.items():
        for days_ago in range(14):
            snap_date = TODAY - timedelta(days=days_ago)
            # Add mild day-to-day variance so the chart looks natural
            variance = 1 + (hash(f"{client_id}{snap_date}") % 20 - 10) / 100
            records.append({
                "client":          client_id,
                "snapshot_date":   snap_date.isoformat(),
                "period_type":     "Daily",
                "total_revenue":   round(rev / 30 * variance, 2),
                "ad_spend":        round(spend / 30 * variance, 2),
                "roas":            round(roas * variance, 2),
                "conversion_rate": round(conv * variance, 2),
                "total_orders":    max(1, round(orders / 30 * variance)),
                "total_sessions":  max(1, round(sessions / 30 * variance)),
                "avg_order_value": round(aov * variance, 2),
            })
    n = airtable_create("KPI Snapshots", records)
    print(f"      ✓ {len(n)} snapshot(s) created")


def seed_revenue():
    print("\n[3/5] Seeding Revenue (last 4 weeks)...")
    records = []
    for client_id, channels in CLIENT_REVENUE.items():
        for weeks_ago in range(4):
            week_start = TODAY - timedelta(days=TODAY.weekday() + 7 * weeks_ago)
            week_label = f"Week of {week_start.strftime('%Y-%m-%d')}"
            for channel, weekly_rev, transactions in channels:
                variance = 1 + (hash(f"{client_id}{channel}{weeks_ago}") % 16 - 8) / 100
                records.append({
                    "client":       client_id,
                    "week_label":   week_label,
                    "week_start":   week_start.isoformat(),
                    "channel":      channel,
                    "revenue":      round(weekly_rev * variance, 2),
                    "transactions": max(1, round(transactions * variance)),
                    "source":       "seed_airtable.py",
                })
    n = airtable_create("Revenue", records)
    print(f"      ✓ {len(n)} revenue row(s) created")


def seed_channel_performance():
    print("\n[4/5] Seeding Channel Performance...")
    period_start = (TODAY - timedelta(days=TODAY.day - 1)).isoformat()  # 1st of month
    period_end   = TODAY.isoformat()
    week_label   = f"Week of {(TODAY - timedelta(days=TODAY.weekday())).strftime('%Y-%m-%d')}"
    records = []
    for client_id, channels in CLIENT_CHANNELS.items():
        for ch in channels:
            records.append({
                "client":             client_id,
                "channel":            ch["channel"],
                "period_start":       period_start,
                "period_end":         period_end,
                "week_label":         week_label,
                "total_revenue":      ch["total_revenue"],
                "total_spend":        ch["total_spend"],
                "roas":               ch["roas"],
                "bar_width_pct":      ch["bar_width_pct"],
                "trend":              ch["trend"],
                "total_transactions": ch["total_transactions"],
            })
    n = airtable_create("Channel Performance", records)
    print(f"      ✓ {len(n)} channel performance row(s) created")


def seed_ai_summaries():
    print("\n[5/5] Seeding AI Summaries...")
    month_start = (TODAY - timedelta(days=TODAY.day - 1)).isoformat()
    records = []
    for client_id, s in AI_SUMMARIES.items():
        records.append({
            "client":          client_id,
            "body_html":       s["body_html"],
            "insight_1_type":  s["insight_1_type"],
            "insight_1_title": s["insight_1_title"],
            "insight_1_text":  s["insight_1_text"],
            "insight_2_type":  s["insight_2_type"],
            "insight_2_title": s["insight_2_title"],
            "insight_2_text":  s["insight_2_text"],
            "insight_3_type":  s["insight_3_type"],
            "insight_3_title": s["insight_3_title"],
            "insight_3_text":  s["insight_3_text"],
            "period_start":    month_start,
            "period_end":      TODAY.isoformat(),
            "generated_at":    TODAY.isoformat(),
            "status":          "Draft",
        })
    n = airtable_create("AI Summaries", records)
    print(f"      ✓ {len(n)} AI summary(ies) created")


# ── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 52)
    print("  ReportFlow — Airtable Seeder")
    print(f"  Base ID : {BASE_ID}")
    print(f"  Date    : {TODAY}")
    print("=" * 52)
    print("\nThis will CREATE new rows in your Airtable base.")
    print("It will UPSERT Clients (safe to re-run).")
    print("KPI Snapshots, Revenue, and Channel Performance")
    print("rows will be ADDED each time (not deduplicated).")
    confirm = input("\nContinue? [y/N] ").strip().lower()
    if confirm != 'y':
        print("Aborted.")
        sys.exit(0)

    seed_clients()
    seed_kpi_snapshots()
    seed_revenue()
    seed_channel_performance()
    seed_ai_summaries()

    print("\n" + "=" * 52)
    print("  Done. Check your Airtable base.")
    print("  Next: activate WF6 in n8n and open the dashboard.")
    print("=" * 52 + "\n")
