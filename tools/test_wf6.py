"""
test_wf6.py — Validate WF6 Dashboard API responses

Usage:
    python tools/test_wf6.py

What it does:
    1. Tests POST /webhook/reportflow/clients  → checks clients list shape
    2. Tests POST /webhook/reportflow/dashboard for each client + date range
       → validates every required field in the response
    3. Prints a clear PASS / FAIL report with details on any missing fields

Requires in .env:
    N8N_BASE_URL=https://your-n8n-instance.com
    N8N_WEBHOOK_SECRET=   (optional)
"""

import os
import sys
import json
import time

try:
    import requests
except ImportError:
    print("ERROR: 'requests' is not installed. Run: pip install requests")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    os.environ.setdefault(k.strip(), v.strip())

# ── Config ───────────────────────────────────────────────────────────────────

N8N_BASE_URL = os.environ.get('N8N_BASE_URL', 'http://localhost:5678').rstrip('/')
WEBHOOK_SECRET = os.environ.get('N8N_WEBHOOK_SECRET', '').strip()

CLIENTS_ENDPOINT   = f"{N8N_BASE_URL}/webhook/reportflow/clients"
DASHBOARD_ENDPOINT = f"{N8N_BASE_URL}/webhook/reportflow/dashboard"

HEADERS = {"Content-Type": "application/json"}
if WEBHOOK_SECRET:
    HEADERS["X-Webhook-Secret"] = WEBHOOK_SECRET

DATE_RANGES = ["this_month", "last_month", "last_90", "ytd"]
TIMEOUT_SECS = 10


# ── Schema definitions ────────────────────────────────────────────────────────

# Required keys at each path. Dot-notation for nested: "kpis.revenue"
CLIENTS_LIST_ITEM_KEYS = ["id", "name", "niche", "color", "initials"]

DASHBOARD_REQUIRED = {
    "client":              ["id", "name", "niche", "color", "initials"],
    "kpis":                ["revenue", "revenueChange", "adSpend", "adSpendChange",
                            "roas", "roasChange", "conversionRate", "conversionChange"],
    "revenueData":         [],   # must be a non-empty list
    "channels":            [],   # must be a list
    "campaigns":           [],   # must be a list
    "aiSummary":           ["bodyHtml", "win", "watch", "next"],
}

INSIGHT_KEYS = ["title", "text"]


# ── Helpers ───────────────────────────────────────────────────────────────────

class Results:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []

    def ok(self, label):
        self.passed += 1
        print(f"  ✓  {label}")

    def fail(self, label, detail=""):
        self.failed += 1
        msg = f"  ✗  {label}"
        if detail:
            msg += f"\n       → {detail}"
        self.errors.append(msg)
        print(msg)

    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'═'*52}")
        print(f"  Results: {self.passed}/{total} checks passed")
        if self.failed:
            print(f"\n  Failed checks:")
            for e in self.errors:
                print(e)
        else:
            print("  All checks passed — WF6 is healthy.")
        print(f"{'═'*52}\n")
        return self.failed == 0


def post(url, body, results, label):
    """POST to url, return parsed JSON or None on error."""
    try:
        resp = requests.post(url, headers=HEADERS, json=body, timeout=TIMEOUT_SECS)
    except requests.exceptions.ConnectionError:
        results.fail(label, f"Cannot connect to {url} — is n8n running and WF6 active?")
        return None
    except requests.exceptions.Timeout:
        results.fail(label, f"Request timed out after {TIMEOUT_SECS}s")
        return None

    if resp.status_code == 404:
        results.fail(label, "404 — webhook path not found. Check WF6 trigger path.")
        return None
    if resp.status_code == 401:
        results.fail(label, "401 — authentication failed. Check N8N_WEBHOOK_SECRET.")
        return None
    if not resp.ok:
        results.fail(label, f"HTTP {resp.status_code}: {resp.text[:150]}")
        return None

    try:
        return resp.json()
    except Exception:
        results.fail(label, f"Response is not valid JSON: {resp.text[:150]}")
        return None


def check_keys(obj, required_keys, path, results):
    """Verify required_keys exist in obj (dict). Report each missing key."""
    if not isinstance(obj, dict):
        results.fail(f"{path} is not an object", f"Got: {type(obj).__name__}")
        return
    for key in required_keys:
        if key in obj:
            results.ok(f"{path}.{key} present")
        else:
            results.fail(f"{path}.{key} MISSING", f"Keys present: {list(obj.keys())}")


def check_list(val, path, results, allow_empty=False):
    """Verify val is a list (and optionally non-empty)."""
    if not isinstance(val, list):
        results.fail(f"{path} should be a list", f"Got: {type(val).__name__}")
        return False
    if not allow_empty and len(val) == 0:
        results.fail(f"{path} is empty — does Airtable have data for this client/period?")
        return False
    results.ok(f"{path} is a list ({len(val)} item{'s' if len(val) != 1 else ''})")
    return True


# ── Test: clients endpoint ────────────────────────────────────────────────────

def test_clients_endpoint(results):
    print(f"\n{'─'*52}")
    print(f"  Test: GET clients list")
    print(f"  POST {CLIENTS_ENDPOINT}")
    print(f"{'─'*52}")

    data = post(CLIENTS_ENDPOINT, {}, results, "clients endpoint reachable")
    if data is None:
        return []

    results.ok("clients endpoint reachable")

    if not isinstance(data, list):
        # Some n8n setups wrap the response
        if isinstance(data, dict) and "clients" in data:
            data = data["clients"]
        else:
            results.fail("response should be a JSON array", f"Got: {type(data).__name__}")
            return []

    if len(data) == 0:
        results.fail("clients list is empty — add at least one Active client in Airtable")
        return []

    results.ok(f"clients list has {len(data)} client(s)")

    # Check first item shape
    first = data[0]
    check_keys(first, CLIENTS_LIST_ITEM_KEYS, "clients[0]", results)

    return [c.get("id") for c in data if isinstance(c, dict) and "id" in c]


# ── Test: dashboard endpoint ──────────────────────────────────────────────────

def test_dashboard_endpoint(client_id, date_range, results):
    label = f"dashboard ({client_id} / {date_range})"
    print(f"\n{'─'*52}")
    print(f"  Test: {label}")
    print(f"  POST {DASHBOARD_ENDPOINT}")
    print(f"  Body: {{'clientId': '{client_id}', 'dateRange': '{date_range}'}}")
    print(f"{'─'*52}")

    data = post(
        DASHBOARD_ENDPOINT,
        {"clientId": client_id, "dateRange": date_range},
        results,
        f"{label} reachable"
    )
    if data is None:
        return

    results.ok(f"{label} returned a response")

    # Check top-level sections
    for section, required_keys in DASHBOARD_REQUIRED.items():
        if section not in data:
            results.fail(f"response.{section} MISSING")
            continue

        val = data[section]

        if section in ("revenueData", "channels", "campaigns"):
            check_list(val, f"response.{section}", results, allow_empty=(section == "channels"))
        else:
            check_keys(val, required_keys, f"response.{section}", results)

    # Deep-check aiSummary insights
    ai = data.get("aiSummary", {})
    if isinstance(ai, dict):
        for insight_key in ("win", "watch", "next"):
            ins = ai.get(insight_key)
            if ins is None:
                results.fail(f"response.aiSummary.{insight_key} MISSING")
            else:
                check_keys(ins, INSIGHT_KEYS, f"response.aiSummary.{insight_key}", results)

    # Check lastSynced
    if "lastSynced" in data:
        results.ok("response.lastSynced present")
    else:
        results.fail("response.lastSynced MISSING")

    # Sanity-check numeric KPIs are positive
    kpis = data.get("kpis", {})
    if isinstance(kpis, dict):
        for num_key in ("revenue", "adSpend", "roas"):
            val = kpis.get(num_key)
            if val is not None and isinstance(val, (int, float)) and val > 0:
                results.ok(f"kpis.{num_key} is positive ({val})")
            elif val == 0:
                results.fail(f"kpis.{num_key} is 0 — Airtable may have no data for this period")
            elif val is None:
                results.fail(f"kpis.{num_key} is null")


# ── Test: error handling ──────────────────────────────────────────────────────

def test_unknown_client(results):
    print(f"\n{'─'*52}")
    print(f"  Test: unknown clientId error handling")
    print(f"{'─'*52}")

    try:
        resp = requests.post(
            DASHBOARD_ENDPOINT,
            headers=HEADERS,
            json={"clientId": "__nonexistent_client__", "dateRange": "this_month"},
            timeout=TIMEOUT_SECS
        )
    except Exception as e:
        results.fail("error handling test failed to connect", str(e))
        return

    if resp.status_code in (404, 400):
        results.ok(f"unknown client returns HTTP {resp.status_code} (correct)")
    elif resp.status_code == 200:
        body = resp.json() if resp.ok else {}
        if "error" in body:
            results.ok("unknown client returns {error:...} in response body")
        else:
            results.fail(
                "unknown client should return an error response",
                f"Got HTTP 200 with no error key: {str(body)[:100]}"
            )
    else:
        results.ok(f"unknown client returns HTTP {resp.status_code}")


# ── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 52)
    print("  ReportFlow — WF6 API Validator")
    print(f"  n8n URL : {N8N_BASE_URL}")
    print(f"  Secret  : {'set' if WEBHOOK_SECRET else 'not set (open webhook)'}")
    print("=" * 52)

    results = Results()

    # 1. Test /clients
    client_ids = test_clients_endpoint(results)

    if not client_ids:
        print("\nNo client IDs returned — skipping dashboard tests.")
        print("Make sure WF6 is active and Airtable has at least one Active client.\n")
        results.summary()
        sys.exit(1 if results.failed else 0)

    # 2. Test /dashboard for first client across all date ranges
    first_client = client_ids[0]
    for date_range in DATE_RANGES:
        test_dashboard_endpoint(first_client, date_range, results)
        time.sleep(0.5)

    # 3. Test additional clients (first date range only) if more than 1
    for client_id in client_ids[1:]:
        test_dashboard_endpoint(client_id, "this_month", results)
        time.sleep(0.5)

    # 4. Test error handling
    test_unknown_client(results)

    # Print summary and exit with code 0 (pass) or 1 (fail)
    passed = results.summary()
    sys.exit(0 if passed else 1)
