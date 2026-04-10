# ReportFlow — Agency Reporting Dashboard

A production-ready client reporting dashboard for marketing agencies. Connects to Airtable as the data warehouse and uses n8n to automate data collection from Google Analytics, Meta Ads, Google Ads, Stripe, and Mailchimp. AI-generated weekly summaries are powered by OpenAI GPT-4o and delivered by email.

---

## How it works

```
GA4 / Meta / Google Ads        n8n Scheduled          Airtable
   Stripe / Mailchimp    ──►   Workflows (WF1–3)  ──►  Tables
                                                           │
OpenAI GPT-4o           ──►   AI Reports (WF4)    ──►    │
                                                           │
Gmail                   ◄──   Report Delivery (WF5) ◄──   │
                                                           │
Browser Dashboard       ◄──   WF6 Webhook API      ◄──────┘
```

**WF1–5 are the writers.** They run on a schedule and keep Airtable up to date.  
**WF6 is the reader.** It responds to the dashboard's requests with live data.  
**Without WF1–5 running, WF6 will return empty data.**

---

## Prerequisites

| Tool | Purpose | Notes |
|---|---|---|
| n8n (self-hosted) | Automation brain | All API keys live here |
| Airtable account | Data warehouse | Free plan works |
| OpenAI API key | AI summaries | GPT-4o, ~$0.02/report |
| Gmail account | Report delivery | Via Google OAuth2 |
| A modern browser | Dashboard | No server needed for portfolio use |

---

## Quick Start (Portfolio / Demo Mode)

No setup required. Just open the dashboard:

```
frontend/index.html
```

Open it in any browser — it runs entirely offline using built-in demo data for 3 mock clients (BrightEdge Digital, NovaTech Solutions, Elevate Coaching).

---

## Full Setup (Live Data)

### Step 1 — Set up Airtable

Create a new Airtable base with these **6 tables** (exact names matter):

| Table | Key fields |
|---|---|
| `Clients` | `client_id`, `company_name`, `niche`, `brand_color`, `contact_email`, `status`, `ga4_property_id`, `meta_ad_account_id`, `google_ads_customer_id` |
| `Campaigns` | `campaign_id`, `campaign_name`, `client`, `platform`, `impressions`, `clicks`, `ctr`, `spend`, `cpc`, `conversions`, `revenue`, `roas`, `date`, `status`, `source` |
| `Revenue` | `client`, `week_label`, `week_start`, `channel`, `revenue`, `transactions`, `source` |
| `KPI Snapshots` | `client`, `snapshot_date`, `period_type`, `total_revenue`, `ad_spend`, `roas`, `conversion_rate`, `total_orders`, `total_sessions`, `avg_order_value` |
| `Channel Performance` | `client`, `channel`, `period_start`, `period_end`, `week_label`, `total_revenue`, `total_spend`, `roas`, `bar_width_pct`, `trend`, `total_transactions` |
| `AI Summaries` | `client`, `body_html`, `insight_1_type`, `insight_1_title`, `insight_1_text`, `insight_2_type`, `insight_2_title`, `insight_2_text`, `insight_3_type`, `insight_3_title`, `insight_3_text`, `period_start`, `period_end`, `generated_at`, `status` |

Add at least one row to `Clients` with `status = Active` before activating workflows.

Find your **Airtable Base ID** in the URL:  
`https://airtable.com/appXXXXXXXXXXXXXX/...` → copy `appXXXXXXXXXXXXXX`

---

### Step 2 — Configure n8n credentials

In n8n go to **Settings → Credentials** and create:

| Credential name | Type | Used by |
|---|---|---|
| Airtable account | Airtable Personal Access Token | WF1–6 |
| Google account | Google OAuth2 (Analytics + Ads scopes) | WF1 |
| Meta Bearer Token | HTTP Bearer Auth (your Meta access token) | WF1 |
| Stripe API Key | HTTP Bearer Auth (your Stripe secret key) | WF1 |
| Mailchimp Basic Auth | HTTP Basic Auth (user: anything, password: API key) | WF1 |
| OpenAI API Key | HTTP Bearer Auth (your OpenAI key) | WF4 |
| Gmail account | Google OAuth2 (Gmail scope) | WF5 |

---

### Step 3 — Import and configure workflows

Import all 6 workflow JSON files from the `workflows/` folder into n8n:  
**n8n → Workflows → Import from file**

Then in every workflow, replace `YOUR_AIRTABLE_BASE_ID` with your actual base ID.

Additionally:
- **WF1** node `Google Ads Query`: replace `YOUR_GOOGLE_ADS_DEVELOPER_TOKEN` with your token
- **WF5** node `Send Email`: replace `YOUR_FROM_EMAIL` with your Gmail address
- **WF1** node `Mailchimp Get Reports`: if your Mailchimp server is not `us1`, update the URL

Workflow files to import:

```
workflows/workflow_6_dashboard_api.json   ← Import this FIRST
workflows/                                ← Then import WF1–5 (provided separately)
```

---

### Step 4 — Activate workflows

Activate in this order:

1. **WF6** (Dashboard API) — activate first so the frontend can connect immediately
2. **WF1** (Daily Data Collection) — run manually once to populate Airtable
3. **WF2** (Weekly Aggregation) — activate for scheduled runs
4. **WF3** (Monthly Channel Performance) — activate for scheduled runs
5. **WF4** (AI Report Generation) — activate after WF1 has data
6. **WF5** (Report Delivery) — activate last, after WF4 has generated summaries

> **Test WF1 manually first.** Go to WF1 → Execute Workflow. Check Airtable — you should see new rows in Campaigns, Revenue, and KPI Snapshots before activating WF4/WF5.

---

### Step 5 — Connect the dashboard

Edit `.env`:

```env
N8N_BASE_URL=https://your-n8n-instance.com
N8N_WEBHOOK_SECRET=   # optional
```

Then open `frontend/index.html` in a browser.  
The dashboard will load mock data instantly, then switch to live Airtable data in the background.

To inject the n8n URL without editing the HTML, add this before the `<script src="js/config.js">` tag:

```html
<script>window.__N8N_BASE_URL__ = 'https://your-n8n-instance.com';</script>
```

This is how you'd configure it per-environment on a web server.

---

## Workflow schedule

| Workflow | When it runs | What it does |
|---|---|---|
| WF1 | Daily at 6:00 AM | Pulls yesterday's data from all 5 integrations → Airtable |
| WF2 | Monday at 7:00 AM | Aggregates last 7 days into Channel Performance |
| WF3 | 1st of month at 8:00 AM | Aggregates last month into Channel Performance |
| WF4 | Monday at 8:00 AM | Generates AI summary using GPT-4o → Airtable |
| WF5 | Monday at 9:00 AM | Sends AI summary email to client → marks Sent |
| WF6 | On demand (webhook) | Reads Airtable and responds to the dashboard |

---

## File structure

```
Agency Report/
│
├── frontend/                    # The dashboard web app
│   ├── index.html               # Open this in a browser
│   ├── css/styles.css           # All styles
│   └── js/
│       ├── config.js            # n8n URL + endpoint config (edit this)
│       └── api.js               # Data fetching service layer
│
├── workflows/                   # n8n automation files
│   ├── workflow_6_dashboard_api.json  # WF6: read API for the dashboard
│   ├── fetch_dashboard_data.md        # WF6 documentation + API contract
│   └── sync_integrations.md          # WF1–5 documentation + Airtable schema
│
├── tools/                       # Python scripts (add as needed)
├── .tmp/                        # Temporary files (gitignored)
├── .env                         # Your local config (gitignored)
├── .env.example                 # Template — safe to commit
└── .gitignore
```

---

## Security model

| What | Where it lives | Notes |
|---|---|---|
| Airtable API key | n8n credentials | Never leaves your server |
| Meta / GA / Stripe tokens | n8n credentials | Never leaves your server |
| OpenAI API key | n8n credentials | Never leaves your server |
| n8n webhook URL | `config.js` | Not a secret — it's a URL |
| Nothing sensitive | Frontend JS | Safe to deploy publicly |

**No API keys ever appear in the frontend.** The browser only knows the n8n webhook URL.

---

## Adding authentication (future)

The dashboard is built to accept auth with one change. In `frontend/js/config.js`:

```js
getAuthHeaders() {
  // Change this to add auth to every API request:
  return { 'Authorization': 'Bearer ' + yourToken };
}
```

On the n8n side, add a **Header Auth** check at the start of WF6 to validate the token.  
No other code changes are needed anywhere else.

---

## Selling to clients (SaaS path)

Each client gets their own `client_id` row in the Airtable `Clients` table. The dashboard reads all active clients from WF6 and populates the dropdown automatically.

To onboard a new client:
1. Add a row to `Clients` in Airtable with their `client_id`, integrations, and `brand_color`
2. WF1 will start collecting their data on the next daily run
3. They'll appear in the dashboard dropdown immediately

For a proper SaaS setup with separate logins per client, the auth layer described above is the starting point.

---

## Troubleshooting

**Dashboard shows demo data even after setup**  
→ Check browser console for errors. The n8n URL in `config.js` may be wrong, or WF6 may not be active.

**WF6 returns empty arrays**  
→ WF1 hasn't run yet. Execute WF1 manually and check Airtable for data first.

**Meta data not coming through**  
→ Meta access tokens expire every 60 days. Refresh the token in n8n credentials.

**Mailchimp returns 401**  
→ Basic Auth password must be your Mailchimp API key (not account password). Server prefix in the URL (`us1`) must match your account's data center.

**AI summary shows placeholder text**  
→ WF4 runs Mondays. Either wait, or execute WF4 manually after WF1 has data.
