export interface KPIs {
  revenue: number
  revenueChange: number
  convRate: number
  convChange: number
  adSpend: number
  spendChange: number
  roas: number
  roasChange: number
}

export interface RevenuePoint {
  week: string
  value: number
  prev: number
}

export interface Channel {
  name: string
  pct: number
  value: number
  color: string
}

export interface ChannelPerformance {
  name: string
  roas: number
  spend: number
  revenue: number
  conv: number
  barWidth: string
  gradient: string
}

export interface Campaign {
  name: string
  platform: string
  spend: number
  revenue: number
  roas: number
  status: string
  impressions: number
  clicks: number
  ctr: number
  cpc: number
}

export interface Insight {
  type: 'win' | 'watch' | 'next'
  title: string
  text: string
}

export interface AISummary {
  body: string
  insights: Insight[]
}

export interface Client {
  id: string
  name: string
  initials: string
  gradient: string
  niche: string
  activeCampaigns: number
  kpis: KPIs
  revenue: RevenuePoint[]
  channels: Channel[]
  performance: ChannelPerformance[]
  campaigns: Campaign[]
  summary: AISummary
  _lastSynced?: string | null
  _isLive?: boolean
}

export interface Report {
  id: string
  clientId: string
  clientName: string
  initials: string
  gradient: string
  period: string
  type: string
  status: 'sent' | 'draft'
  generatedAt: string
  summary: AISummary
}

export interface DateRange {
  id: string
  label: string
  value: string
}

// Shape returned by the Next.js API routes (mirrors WF6 response)
export interface DashboardApiResponse {
  client: {
    id: string; name: string; niche: string
    color: string; colorEnd: string; initials: string
  }
  kpis: {
    revenue: number; revenueChange: number
    conversionRate: number; conversionChange: number
    adSpend: number; adSpendChange: number
    roas: number; roasChange: number
  }
  revenueData: { label: string; value: number; prev: number }[]
  channels: {
    name: string; percentage: number; spend: number
    revenue: number; roas: number; barWidthPct: number; convRate?: number
  }[]
  campaigns: {
    id: string; name: string; platform: string
    spend: number; revenue: number; roas: number; status: string
    impressions: number; clicks: number; ctr: number; cpc: number
  }[]
  aiSummary: {
    bodyHtml: string
    win: { title: string; text: string }
    watch: { title: string; text: string }
    next: { title: string; text: string }
  }
  lastSynced: string
}

export interface ClientsApiResponse {
  id: string; name: string; niche: string
  color: string; colorEnd: string; initials: string; campaignCount: number
}[]
