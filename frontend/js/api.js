// ══════════════════════════════════════════════════════════════
// ReportFlow — API Service
//
// All fetch() calls live here. The dashboard JS never calls
// fetch() directly — it calls these functions instead.
//
// Data flow:
//   Frontend → n8n webhook → Airtable → n8n formats → JSON response
//
// To add auth later: update CONFIG.getAuthHeaders() in config.js only.
// No changes needed here.
//
// Airtable tables read by WF6 (the Dashboard API workflow):
//   Clients, KPI Snapshots, Campaigns, Revenue,
//   Channel Performance, AI Summaries
// ══════════════════════════════════════════════════════════════

const ReportAPI = (() => {

  // ── Channel color palette (matches existing CSS platform tags) ──
  const CHANNEL_COLORS = {
    'meta ads':       '#d4a843',
    'google ads':     '#6366f1',
    'email':          '#3ecf8e',
    'email funnels':  '#3ecf8e',
    'organic':        '#a855f7',
    'linkedin':       '#3ecf8e',
    'content/seo':    '#d4a843',
    'instagram ads':  '#f59e0b',
    'youtube':        '#ef4444',
    'referral':       '#6366f1',
    'stripe':         '#a855f7',
    'direct':         '#6366f1',
  };

  const CHANNEL_GRADIENTS = {
    'meta ads':       'linear-gradient(90deg,#d4a843,#e8c547)',
    'google ads':     'linear-gradient(90deg,#6366f1,#818cf8)',
    'email':          'linear-gradient(90deg,#3ecf8e,#6ee7a8)',
    'email funnels':  'linear-gradient(90deg,#3ecf8e,#6ee7a8)',
    'organic':        'linear-gradient(90deg,#a855f7,#c084fc)',
    'linkedin':       'linear-gradient(90deg,#3ecf8e,#6ee7a8)',
    'content/seo':    'linear-gradient(90deg,#d4a843,#e8c547)',
    'instagram ads':  'linear-gradient(90deg,#f59e0b,#fbbf24)',
    'youtube':        'linear-gradient(90deg,#ef4444,#f87171)',
    'referral':       'linear-gradient(90deg,#6366f1,#818cf8)',
  };

  function channelColor(name) {
    return CHANNEL_COLORS[name.toLowerCase()] || '#7a7570';
  }

  function channelGradient(name) {
    return CHANNEL_GRADIENTS[name.toLowerCase()] || 'linear-gradient(90deg,#7a7570,#a0a0a0)';
  }

  // ── HTTP helper ──────────────────────────────────────────────
  async function post(path, body) {
    const url = CONFIG.n8nBaseUrl + path;
    const res = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...CONFIG.getAuthHeaders(),
      },
      body: JSON.stringify(body),
    });
    if (!res.ok) throw new Error(`n8n ${res.status}: ${res.statusText}`);
    return res.json();
  }

  // ── Normalize n8n clients list → dropdown format ─────────────
  // Expected n8n response: array of { id, name, niche, color, colorEnd, initials, campaignCount }
  function normalizeClients(apiClients) {
    return apiClients.map(c => ({
      id:              c.id,
      name:            c.name,
      initials:        c.initials || c.name.split(' ').map(w => w[0]).join('').slice(0,2).toUpperCase(),
      gradient:        `linear-gradient(135deg, ${c.color || '#6366f1'}, ${c.colorEnd || c.color || '#a855f7'})`,
      niche:           c.niche || '',
      activeCampaigns: c.campaignCount || 0,
    }));
  }

  // ── Normalize n8n dashboard response → internal CLIENTS[] shape ──
  // This is the contract between WF6 and the frontend.
  // n8n must return:
  // {
  //   client:    { id, name, niche, color, colorEnd, initials }
  //   kpis:      { revenue, revenueChange, conversionRate, conversionChange,
  //                adSpend, adSpendChange, roas, roasChange }
  //   revenueData: [{ label, value, prev }]
  //   channels:    [{ name, percentage, spend, revenue, roas, convRate, barWidthPct }]
  //   campaigns:   [{ id, name, platform, spend, revenue, roas, status,
  //                   impressions, clicks, ctr, cpc }]
  //   aiSummary:   { bodyHtml,
  //                  win:   { title, text },
  //                  watch: { title, text },
  //                  next:  { title, text } }
  //   lastSynced:  ISO string
  // }
  function normalizeDashboard(data) {
    const client = data.client || {};
    const kpis   = data.kpis   || {};

    const channels = (data.channels || []).map(ch => ({
      name:  ch.name,
      pct:   ch.percentage || 0,
      value: ch.revenue    || 0,
      color: channelColor(ch.name),
    }));

    const performance = (data.channels || []).map(ch => ({
      name:      ch.name,
      roas:      ch.roas     || 0,
      spend:     ch.spend    || 0,
      revenue:   ch.revenue  || 0,
      conv:      ch.convRate || 0,
      barWidth:  (ch.barWidthPct || 50) + '%',
      gradient:  channelGradient(ch.name),
    }));

    const campaigns = (data.campaigns || []).map(c => ({
      name:        c.name,
      platform:    (c.platform || '').toLowerCase(),
      spend:       c.spend       || 0,
      revenue:     c.revenue     || 0,
      roas:        c.roas        || 0,
      status:      (c.status || 'active').toLowerCase(),
      impressions: c.impressions || 0,
      clicks:      c.clicks      || 0,
      ctr:         c.ctr         || 0,
      cpc:         c.cpc         || 0,
    }));

    const ai = data.aiSummary || {};
    const summary = {
      body: ai.bodyHtml || '<p>AI summary not available for this period.</p>',
      insights: [
        { type: 'win',   title: (ai.win   || {}).title || 'Win',        text: (ai.win   || {}).text || '' },
        { type: 'watch', title: (ai.watch || {}).title || 'Watch',      text: (ai.watch || {}).text || '' },
        { type: 'next',  title: (ai.next  || {}).title || 'Next Steps', text: (ai.next  || {}).text || '' },
      ],
    };

    return {
      id:               client.id || 'unknown',
      name:             client.name || 'Unknown Client',
      initials:         client.initials || '??',
      gradient:         `linear-gradient(135deg, ${client.color || '#6366f1'}, ${client.colorEnd || client.color || '#a855f7'})`,
      niche:            client.niche || '',
      activeCampaigns:  campaigns.length,
      kpis: {
        revenue:        kpis.revenue         || 0,
        revenueChange:  kpis.revenueChange   || 0,
        convRate:       kpis.conversionRate  || 0,
        convChange:     kpis.conversionChange|| 0,
        adSpend:        kpis.adSpend         || 0,
        spendChange:    kpis.adSpendChange   || 0,
        roas:           kpis.roas            || 0,
        roasChange:     kpis.roasChange      || 0,
      },
      revenue:     (data.revenueData || []).map(r => ({
        week:  r.label || r.week || '',
        value: r.value || 0,
        prev:  r.prev  || 0,
      })),
      channels,
      performance,
      campaigns,
      summary,
      _lastSynced: data.lastSynced || null,
      _isLive: true,
    };
  }

  // ── Public API ───────────────────────────────────────────────

  // Fetch the list of active clients for the dropdown.
  // Falls back to null on error (caller uses MOCK_CLIENTS).
  async function fetchClients() {
    try {
      const data = await post(CONFIG.webhooks.clients, {});
      const list = Array.isArray(data) ? data : (data.clients || []);
      return normalizeClients(list);
    } catch (err) {
      console.warn('[ReportFlow] fetchClients failed:', err.message);
      return null; // caller falls back to mock
    }
  }

  // Fetch full dashboard data for a client + date range.
  // Returns normalized object (same shape as MOCK_CLIENTS[i]) or null on error.
  async function fetchDashboard(clientId, dateRangeId) {
    try {
      const data = await post(CONFIG.webhooks.dashboard, {
        clientId,
        dateRange: dateRangeId,
      });
      return normalizeDashboard(data);
    } catch (err) {
      console.warn('[ReportFlow] fetchDashboard failed:', err.message);
      return null; // caller falls back to mock
    }
  }

  return { fetchClients, fetchDashboard };

})();
