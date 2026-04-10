// ══════════════════════════════════════════════════════════════
// ReportFlow — Configuration
// All n8n webhook endpoints are defined here.
// To connect to live data: set window.__N8N_BASE_URL__ before
// this script loads (e.g. injected by a server at serve time),
// or configure via the Settings page in the dashboard (saved to localStorage).
// ══════════════════════════════════════════════════════════════

const CONFIG = {

  // Base URL of your n8n instance.
  // Priority: localStorage (Settings page) → window injection → default localhost
  get n8nBaseUrl() {
    const saved = localStorage.getItem('reportflow_n8n_url');
    return (saved || window.__N8N_BASE_URL__ || 'http://localhost:5678').replace(/\/$/, '');
  },
  setN8nUrl(url) {
    localStorage.setItem('reportflow_n8n_url', url.replace(/\/$/, ''));
  },

  // Optional webhook secret for X-Webhook-Secret header auth in WF6.
  // Priority: localStorage (Settings page) → window injection → empty (no auth)
  get webhookSecret() {
    return localStorage.getItem('reportflow_webhook_secret') || window.__N8N_WEBHOOK_SECRET__ || '';
  },
  setWebhookSecret(secret) {
    if (secret) {
      localStorage.setItem('reportflow_webhook_secret', secret);
    } else {
      localStorage.removeItem('reportflow_webhook_secret');
    }
  },

  // n8n webhook paths (must match your WF6 webhook trigger paths)
  webhooks: {
    clients:   '/webhook/reportflow/clients',
    dashboard: '/webhook/reportflow/dashboard',
  },

  // Auth header factory — adds X-Webhook-Secret when configured.
  // To add JWT auth later: return { 'Authorization': 'Bearer ' + token }
  getAuthHeaders() {
    const secret = this.webhookSecret;
    return secret ? { 'X-Webhook-Secret': secret } : {};
  },

  // Returns true when running against localhost (enables silent mock fallback)
  isOfflineMode() {
    const url = this.n8nBaseUrl;
    return url.includes('localhost') || url.includes('127.0.0.1');
  },

};
