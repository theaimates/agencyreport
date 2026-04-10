# WF1–WF5: Data Sync Pipelines

## Overview
These 5 scheduled workflows collectively form the ETL backbone.  
They run automatically — no manual triggering needed in production.

| Workflow | Schedule | What it does |
|---|---|---|
| WF1: Daily Data Collection | Daily 6:00 AM | GA4, Meta, Google Ads, Stripe, Mailchimp → Airtable |
| WF2: Weekly Aggregation | Monday 7:00 AM | Revenue + Campaigns → Channel Performance (weekly) |
| WF3: Monthly Channel Performance | 1st of month 8:00 AM | Revenue + Campaigns → Channel Performance (monthly) |
| WF4: AI Report Generation | Monday 8:00 AM | KPI Snapshots + Channels + Campaigns → OpenAI → AI Summaries |
| WF5: Report Delivery | Monday 9:00 AM | AI Summaries → Gmail → mark Sent |

## Airtable base ID
Replace `YOUR_AIRTABLE_BASE_ID` in all 5 workflow JSONs with your actual base ID.  
Find it in your Airtable URL: `airtable.com/appXXXXXXXXXXXXXX/...`

## Required n8n credentials

| Credential | Used by | Where to configure |
|---|---|---|
| Airtable account (token) | WF1–WF5 | n8n → Credentials → Airtable API |
| Google OAuth2 (GA4 + Google Ads) | WF1 | n8n → Credentials → Google OAuth2 |
| Meta Bearer Token | WF1 | n8n → Credentials → HTTP Bearer Auth |
| Stripe API Key | WF1 | n8n → Credentials → HTTP Bearer Auth |
| Mailchimp Basic Auth | WF1 | n8n → Credentials → HTTP Basic Auth (user: anystring, pass: API key) |
| OpenAI API Key | WF4 | n8n → Credentials → HTTP Bearer Auth |
| Gmail OAuth2 | WF5 | n8n → Credentials → Google OAuth2 |

## Airtable table schema

### Clients
| Field | Type | Notes |
|---|---|---|
| client_id | Text | Unique string key (e.g. "brightedge") |
| company_name | Text | |
| niche | Text | E-commerce, SaaS, etc. |
| brand_color | Text | Hex color for UI |
| contact_email | Email | For WF5 report delivery |
| status | Single select | Active / Inactive |
| ga4_property_id | Text | From Google Analytics |
| meta_ad_account_id | Text | Meta Ads account ID |
| google_ads_customer_id | Text | |

### Campaigns
| Field | Type | Notes |
|---|---|---|
| campaign_id | Text | Platform-specific ID |
| campaign_name | Text | |
| client | Text | → client_id |
| platform | Single select | ga4 / meta / google / email / stripe |
| impressions | Number | |
| clicks | Number | |
| ctr | Number | Decimal (e.g. 5.2 = 5.2%) |
| spend | Currency | |
| cpc | Currency | |
| conversions | Number | |
| revenue | Currency | |
| roas | Number | Computed: revenue / spend |
| date | Date | Data date |
| status | Single select | Active / Paused |
| source | Text | "Meta Ads", "Google Ads", etc. |
| last_synced | Date | Auto-set by n8n |

### Revenue
| Field | Type | Notes |
|---|---|---|
| client | Text | → client_id |
| week_label | Text | "Week of 2026-03-31" |
| week_start | Date | |
| channel | Text | Channel/platform name |
| revenue | Currency | |
| transactions | Number | |
| source | Text | |

### KPI Snapshots
| Field | Type | Notes |
|---|---|---|
| client | Text | → client_id |
| snapshot_date | Date | |
| period_type | Single select | Daily |
| total_revenue | Currency | |
| ad_spend | Currency | |
| roas | Number | |
| conversion_rate | Number | Decimal % |
| total_orders | Number | |
| total_sessions | Number | |
| avg_order_value | Currency | |

### Channel Performance
| Field | Type | Notes |
|---|---|---|
| client | Text | → client_id |
| channel | Text | Channel name |
| period_start | Date | |
| period_end | Date | |
| week_label | Text | |
| total_revenue | Currency | |
| total_spend | Currency | |
| roas | Number | |
| bar_width_pct | Number | 0–100, for UI progress bar |
| trend | Text | "↑ Growing" / "→ Stable" / "↓ Declining" |
| total_transactions | Number | |

### AI Summaries
| Field | Type | Notes |
|---|---|---|
| client | Text | → client_id |
| body_html | Long text | HTML-formatted narrative |
| insight_1_type | Single select | win / watch / next |
| insight_1_title | Text | |
| insight_1_text | Long text | |
| insight_2_type | Single select | |
| insight_2_title | Text | |
| insight_2_text | Long text | |
| insight_3_type | Single select | |
| insight_3_title | Text | |
| insight_3_text | Long text | |
| period_start | Date | |
| period_end | Date | |
| generated_at | Date/time | |
| status | Single select | Draft / Sent |

## WF1 — Daily Data Collection
**Key behavior:**
- Loops through all Active clients (one at a time via SplitInBatches)
- For each client, fires 5 parallel data fetches: GA4, Meta, Google Ads, Stripe, Mailchimp
- Merges all into a single stream → upserts Campaigns → creates Revenue + KPI Snapshot rows
- Uses `campaign_id` as upsert key in Campaigns table

**Known constraints:**
- Mailchimp server prefix is hardcoded as `us1` in WF1 — update if your account is on a different server
- Google Ads Developer Token must be set in the `developer-token` header (node wf1-010)
- Meta API rate limit: ~200 calls/hour per token. For many clients, add a Wait node between batches

## WF4 — AI Report Generation
- Uses GPT-4o via OpenAI API (credential id 6 in template)
- Prompt assembles last 2 weeks of KPI Snapshots + Channel Performance + top 5 campaigns
- Parses the response to extract Win / Watch / Next insights
- Status is set to `Draft` — WF5 picks it up 1 hour later and sends the email

## WF5 — Report Delivery
- Reads `AI Summaries` where `status = 'Draft'`
- Builds branded HTML email using `brand_color` from the Clients table
- Sends via Gmail, then marks the record as `Sent`
- `YOUR_FROM_EMAIL` in node wf5-006 must be replaced with your Gmail address

## Activating workflows
1. Import all 5 JSON files into n8n (Settings → Import Workflow)
2. Fill in `YOUR_AIRTABLE_BASE_ID` in every Airtable node
3. Configure all credentials listed above
4. Set `YOUR_GOOGLE_ADS_DEVELOPER_TOKEN` in WF1 node wf1-010
5. Set `YOUR_FROM_EMAIL` in WF5 node wf5-006
6. Activate each workflow (toggle the Active switch)
7. Test WF1 manually first — check Airtable for new records before activating WF4/WF5
