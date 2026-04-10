# WF6: Dashboard API (Webhook)

## Objective
Serve real-time dashboard data to the ReportFlow Next.js dashboard on demand.  
This is the read-only counterpart to WF1–WF5, which write data to Airtable.

## Architecture note (updated)
The frontend no longer calls n8n directly. Requests go:
```
Browser → Next.js API route (/api/dashboard) → n8n WF6 webhook → Airtable
```
This means `N8N_BASE_URL` and `N8N_WEBHOOK_SECRET` are **server-side env vars** in Vercel — never exposed to the browser. The `X-Webhook-Secret` header is added by the Next.js API route, not the client.

**To configure:** Set `N8N_BASE_URL` and `N8N_WEBHOOK_SECRET` in Vercel project settings (or `dashboard/.env.local` for local dev).

## Trigger
- **Type:** Webhook (HTTP POST)
- **Path:** `/webhook/reportflow/dashboard`
- **Auth:** `X-Webhook-Secret` header — sent by the Next.js API route using the `N8N_WEBHOOK_SECRET` env var

## Inputs (request body)
```json
{
  "clientId":  "brightedge",
  "dateRange": "this_month"
}
```

**dateRange values:** `this_month` | `last_month` | `q1` | `last_90` | `ytd`

## Airtable tables read
- `Clients` — client metadata (name, niche, brand_color, contact_email)
- `KPI Snapshots` — revenue, spend, ROAS, conversion rate (daily snapshots)
- `Revenue` — per-channel revenue rows for chart data
- `Channel Performance` — aggregated channel breakdown (from WF2/WF3)
- `Campaigns` — campaign-level metrics
- `AI Summaries` — latest AI-generated insights for this client

## Processing steps

### 1. Parse inputs
- Receive `clientId` and `dateRange` from POST body
- Compute date window:
  - `this_month` → first day of current month to today
  - `last_month` → full previous month
  - `q1` → Jan 1 to Mar 31 of current year
  - `last_90` → today minus 90 days to today
  - `ytd` → Jan 1 to today

### 2. Fetch client record
```
filterByFormula: {client_id} = '{{ clientId }}'
table: Clients
```

### 3. Fetch KPI Snapshots (parallel)
- **Current period:** snapshots within date window, ordered desc
- **Previous period:** same window offset back one period (for % change calc)
- Aggregate: sum revenue, sum spend, latest ROAS + conv_rate

### 4. Compute KPI changes
```js
revenueChange = ((currentRevenue - prevRevenue) / prevRevenue) * 100
adSpendChange = ((currentSpend  - prevSpend)  / prevSpend)  * 100
roasChange    = currentRoas - prevRoas
convChange    = currentConvRate - prevConvRate
```

### 5. Fetch Revenue rows (for trend chart)
- Filter by `client = clientId` and date within window
- Group by `week_label`, sum `revenue` per group
- Return as array: `[{ label: "Wk 1", value: 42000, prev: 38000 }]`

### 6. Fetch Channel Performance
- Filter by `client = clientId` and `period_start` within window
- Returns: channel name, revenue, spend, ROAS, bar_width_pct

### 7. Compute channel percentages
```js
totalRevenue = sum(channel.total_revenue)
channel.percentage = Math.round((channel.total_revenue / totalRevenue) * 100)
```

### 8. Fetch Campaigns
- Filter by `client = clientId` and `date` within window
- Sort by `revenue` desc, limit 20

### 9. Fetch latest AI Summary
- Filter by `client = clientId` and `status` IN ('Draft', 'Sent')
- Sort by `generated_at` desc, limit 1

### 10. Respond to Webhook
Use the **Respond to Webhook** n8n node with the JSON below.

## Response shape
```json
{
  "client": {
    "id": "brightedge",
    "name": "BrightEdge Digital",
    "niche": "E-commerce",
    "color": "#6366f1",
    "colorEnd": "#a855f7",
    "initials": "BE"
  },
  "kpis": {
    "revenue": 187420,        "revenueChange": 32.1,
    "conversionRate": 4.8,   "conversionChange": 1.2,
    "adSpend": 42180,         "adSpendChange": -8.4,
    "roas": 4.44,             "roasChange": 0.92
  },
  "revenueData": [
    { "label": "Wk 1", "value": 28400, "prev": 24200 }
  ],
  "channels": [
    { "name": "Meta Ads", "percentage": 42, "spend": 15140,
      "revenue": 78716, "roas": 5.2, "barWidthPct": 87 }
  ],
  "campaigns": [
    { "id": "...", "name": "Spring Collection Launch", "platform": "Meta",
      "spend": 8420, "revenue": 52180, "roas": 6.20, "status": "Active",
      "impressions": 245000, "clicks": 12800, "ctr": 5.2, "cpc": 0.66 }
  ],
  "aiSummary": {
    "bodyHtml": "<p>...</p>",
    "win":   { "title": "Biggest Win",  "text": "..." },
    "watch": { "title": "Watch Closely","text": "..." },
    "next":  { "title": "Next Move",    "text": "..." }
  },
  "lastSynced": "2026-04-03T06:00:00.000Z"
}
```

## Error handling
- If client not found: respond `{ "error": "Client not found" }` with HTTP 404
- If Airtable query fails: respond `{ "error": "Data unavailable" }` with HTTP 500
- The frontend falls back to mock data on any non-200 response

## Notes
- This workflow is triggered on every client switch and date range change in the frontend
- Keep response time under 3 seconds — use parallel Airtable fetches where possible
- The `Respond to Webhook` node must be set to "Respond with Last Node's Data" OFF,
  explicitly returning the assembled JSON object
