import type { Client, DashboardApiResponse } from './types'
import { channelColor, channelGradient } from './utils'

// Normalize API response → internal Client shape
function normalizeDashboard(data: DashboardApiResponse): Client {
  const client = data.client || {}
  const kpis = data.kpis || {}

  const channels = (data.channels || []).map(ch => ({
    name: ch.name,
    pct: ch.percentage || 0,
    value: ch.revenue || 0,
    color: channelColor(ch.name),
  }))

  const performance = (data.channels || []).map(ch => ({
    name: ch.name,
    roas: ch.roas || 0,
    spend: ch.spend || 0,
    revenue: ch.revenue || 0,
    conv: ch.convRate || 0,
    barWidth: (ch.barWidthPct || 50) + '%',
    gradient: channelGradient(ch.name),
  }))

  const campaigns = (data.campaigns || []).map(c => ({
    name: c.name,
    platform: (c.platform || '').toLowerCase(),
    spend: c.spend || 0,
    revenue: c.revenue || 0,
    roas: c.roas || 0,
    status: (c.status || 'active').toLowerCase(),
    impressions: c.impressions || 0,
    clicks: c.clicks || 0,
    ctr: c.ctr || 0,
    cpc: c.cpc || 0,
  }))

  const ai = data.aiSummary || {} as DashboardApiResponse['aiSummary']
  const summary = {
    body: ai.bodyHtml || '<p>AI summary not available for this period.</p>',
    insights: [
      { type: 'win' as const, title: (ai.win || {}).title || 'Win', text: (ai.win || {}).text || '' },
      { type: 'watch' as const, title: (ai.watch || {}).title || 'Watch', text: (ai.watch || {}).text || '' },
      { type: 'next' as const, title: (ai.next || {}).title || 'Next Steps', text: (ai.next || {}).text || '' },
    ],
  }

  return {
    id: client.id || 'unknown',
    name: client.name || 'Unknown Client',
    initials: client.initials || '??',
    gradient: `linear-gradient(135deg, ${client.color || '#6366f1'}, ${client.colorEnd || client.color || '#a855f7'})`,
    niche: client.niche || '',
    activeCampaigns: campaigns.length,
    kpis: {
      revenue: kpis.revenue || 0,
      revenueChange: kpis.revenueChange || 0,
      convRate: kpis.conversionRate || 0,
      convChange: kpis.conversionChange || 0,
      adSpend: kpis.adSpend || 0,
      spendChange: kpis.adSpendChange || 0,
      roas: kpis.roas || 0,
      roasChange: kpis.roasChange || 0,
    },
    revenue: (data.revenueData || []).map(r => ({
      week: r.label || '',
      value: r.value || 0,
      prev: r.prev || 0,
    })),
    channels,
    performance,
    campaigns,
    summary,
    _lastSynced: data.lastSynced || null,
    _isLive: true,
  }
}

// Fetch live client list from Next.js API route
export async function fetchClients(): Promise<{ id: string; name: string; initials: string; gradient: string; niche: string; activeCampaigns: number }[] | null> {
  try {
    const res = await fetch('/api/clients', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({}) })
    if (!res.ok) return null
    const data = await res.json()
    const list: DashboardApiResponse[] = Array.isArray(data) ? data : (data.clients || [])
    return list.map((c: any) => ({
      id: c.id,
      name: c.name,
      initials: c.initials || c.name.split(' ').map((w: string) => w[0]).join('').slice(0, 2).toUpperCase(),
      gradient: `linear-gradient(135deg, ${c.color || '#6366f1'}, ${c.colorEnd || c.color || '#a855f7'})`,
      niche: c.niche || '',
      activeCampaigns: c.campaignCount || 0,
    }))
  } catch {
    return null
  }
}

// Fetch full dashboard for a client+dateRange from Next.js API route
export async function fetchDashboard(clientId: string, dateRangeId: string): Promise<Client | null> {
  try {
    const res = await fetch('/api/dashboard', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ clientId, dateRange: dateRangeId }),
    })
    if (!res.ok) return null
    const data: DashboardApiResponse = await res.json()
    return normalizeDashboard(data)
  } catch {
    return null
  }
}
