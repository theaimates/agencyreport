import type { Client, Report, DateRange } from './types'

export const MOCK_CLIENTS: Client[] = [
  {
    id: 'brightedge', name: 'BrightEdge Digital', initials: 'BE',
    gradient: 'linear-gradient(135deg,#6366f1,#a855f7)',
    niche: 'E-commerce', activeCampaigns: 14,
    kpis: { revenue: 187420, revenueChange: 32.1, convRate: 4.8, convChange: 1.2, adSpend: 42180, spendChange: -8.4, roas: 4.44, roasChange: 0.92 },
    revenue: [
      { week: 'Wk 1', value: 28400, prev: 24200 }, { week: 'Wk 2', value: 35200, prev: 28100 },
      { week: 'Wk 3', value: 48600, prev: 38500 }, { week: 'Wk 4', value: 52100, prev: 41800 },
      { week: 'Wk 5', value: 23120, prev: 29240 },
    ],
    channels: [
      { name: 'Meta Ads', pct: 42, value: 78716, color: '#d4a843' },
      { name: 'Google Ads', pct: 28, value: 52478, color: '#6366f1' },
      { name: 'Email', pct: 18, value: 33736, color: '#3ecf8e' },
      { name: 'Organic', pct: 12, value: 22490, color: '#a855f7' },
    ],
    performance: [
      { name: 'Meta Ads', roas: 5.2, spend: 15140, revenue: 78716, conv: 5.6, barWidth: '87%', gradient: 'linear-gradient(90deg,#d4a843,#e8c547)' },
      { name: 'Google Ads', roas: 3.8, spend: 13810, revenue: 52478, conv: 4.2, barWidth: '63%', gradient: 'linear-gradient(90deg,#6366f1,#818cf8)' },
      { name: 'Email', roas: 28.1, spend: 1200, revenue: 33736, conv: 8.1, barWidth: '56%', gradient: 'linear-gradient(90deg,#3ecf8e,#6ee7a8)' },
      { name: 'Organic', roas: Infinity, spend: 0, revenue: 22490, conv: 3.4, barWidth: '37%', gradient: 'linear-gradient(90deg,#a855f7,#c084fc)' },
    ],
    campaigns: [
      { name: 'Spring Collection Launch', platform: 'meta', spend: 8420, revenue: 52180, roas: 6.20, status: 'active', impressions: 245000, clicks: 12800, ctr: 5.2, cpc: 0.66 },
      { name: 'Brand Awareness Q1', platform: 'meta', spend: 4200, revenue: 18900, roas: 4.50, status: 'active', impressions: 890000, clicks: 8900, ctr: 1.0, cpc: 0.47 },
      { name: 'Shopping Ads — Bestsellers', platform: 'google', spend: 6100, revenue: 28670, roas: 4.70, status: 'active', impressions: 180000, clicks: 9200, ctr: 5.1, cpc: 0.66 },
      { name: 'Retargeting — Cart Abandon', platform: 'meta', spend: 2520, revenue: 7636, roas: 3.03, status: 'active', impressions: 45000, clicks: 3200, ctr: 7.1, cpc: 0.79 },
      { name: 'Search — Branded Terms', platform: 'google', spend: 3200, revenue: 12480, roas: 3.90, status: 'active', impressions: 62000, clicks: 4100, ctr: 6.6, cpc: 0.78 },
      { name: 'Weekly Newsletter', platform: 'email', spend: 400, revenue: 18200, roas: 45.5, status: 'active', impressions: 28000, clicks: 4200, ctr: 15.0, cpc: 0.10 },
      { name: 'Search — Generic Keywords', platform: 'google', spend: 4510, revenue: 11328, roas: 2.51, status: 'paused', impressions: 220000, clicks: 6800, ctr: 3.1, cpc: 0.66 },
      { name: 'Win-Back Series', platform: 'email', spend: 800, revenue: 15536, roas: 19.4, status: 'active', impressions: 15000, clicks: 2800, ctr: 18.7, cpc: 0.29 },
    ],
    summary: {
      body: `<p>March was a <strong>breakout month</strong> for BrightEdge Digital. Revenue hit <span class="hl">$187,420</span> — a <strong>32.1% increase</strong> over February — while ad spend actually <strong>decreased 8.4%</strong>, pushing ROAS from 3.52x to 4.44x.</p><p>The <strong>Spring Collection Launch</strong> on Meta was the standout campaign, generating $52,180 on just $8,420 in spend (6.20x ROAS). Email continues to punch well above its weight: the <strong>Weekly Newsletter</strong> alone drove $18,200 at a 45.5x return.</p><p>One area to watch: <strong>Google Generic Keywords</strong> was paused mid-month after ROAS dipped below 2.5x. Recommend reallocating that $4,510 budget to the Shopping Ads campaign, which is converting at 4.70x with room to scale.</p>`,
      insights: [
        { type: 'win', title: 'Biggest Win', text: 'Spring Collection Launch drove 28% of total revenue on 20% of ad spend.' },
        { type: 'watch', title: 'Watch Closely', text: 'Google Generic Keywords paused — $4,510 budget needs reallocation.' },
        { type: 'next', title: 'Next Move', text: 'Scale Shopping Ads budget by 40% and test new email segments.' },
      ],
    },
  },
  {
    id: 'nova', name: 'NovaTech Solutions', initials: 'NT',
    gradient: 'linear-gradient(135deg,#3ecf8e,#0ea5e9)',
    niche: 'SaaS', activeCampaigns: 9,
    kpis: { revenue: 94200, revenueChange: 18.5, convRate: 3.2, convChange: 0.4, adSpend: 28400, spendChange: -5.1, roas: 3.32, roasChange: 0.48 },
    revenue: [
      { week: 'Wk 1', value: 16800, prev: 14200 }, { week: 'Wk 2', value: 19200, prev: 16800 },
      { week: 'Wk 3', value: 24100, prev: 20500 }, { week: 'Wk 4', value: 22800, prev: 19200 },
      { week: 'Wk 5', value: 11300, prev: 8580 },
    ],
    channels: [
      { name: 'Google Ads', pct: 48, value: 45216, color: '#6366f1' },
      { name: 'LinkedIn', pct: 26, value: 24492, color: '#3ecf8e' },
      { name: 'Content/SEO', pct: 16, value: 15072, color: '#d4a843' },
      { name: 'Email', pct: 10, value: 9420, color: '#a855f7' },
    ],
    performance: [
      { name: 'Google Ads', roas: 3.8, spend: 11900, revenue: 45216, conv: 3.8, barWidth: '82%', gradient: 'linear-gradient(90deg,#6366f1,#818cf8)' },
      { name: 'LinkedIn', roas: 2.6, spend: 9420, revenue: 24492, conv: 2.1, barWidth: '53%', gradient: 'linear-gradient(90deg,#3ecf8e,#6ee7a8)' },
      { name: 'Content/SEO', roas: Infinity, spend: 2100, revenue: 15072, conv: 4.5, barWidth: '33%', gradient: 'linear-gradient(90deg,#d4a843,#e8c547)' },
      { name: 'Email', roas: 15.7, spend: 600, revenue: 9420, conv: 6.2, barWidth: '20%', gradient: 'linear-gradient(90deg,#a855f7,#c084fc)' },
    ],
    campaigns: [
      { name: 'SaaS Demo Campaign', platform: 'google', spend: 5200, revenue: 22400, roas: 4.31, status: 'active', impressions: 142000, clicks: 5600, ctr: 3.9, cpc: 0.93 },
      { name: 'LinkedIn Thought Leadership', platform: 'meta', spend: 4800, revenue: 14400, roas: 3.00, status: 'active', impressions: 320000, clicks: 3200, ctr: 1.0, cpc: 1.50 },
      { name: 'Free Trial Retargeting', platform: 'google', spend: 3200, revenue: 12800, roas: 4.00, status: 'active', impressions: 38000, clicks: 2800, ctr: 7.4, cpc: 1.14 },
      { name: 'Onboarding Drip', platform: 'email', spend: 200, revenue: 5200, roas: 26.0, status: 'active', impressions: 8500, clicks: 1700, ctr: 20.0, cpc: 0.12 },
      { name: 'LinkedIn Lead Gen', platform: 'meta', spend: 4620, revenue: 10092, roas: 2.18, status: 'active', impressions: 280000, clicks: 2800, ctr: 1.0, cpc: 1.65 },
      { name: 'Search — Competitor Terms', platform: 'google', spend: 3500, revenue: 10016, roas: 2.86, status: 'paused', impressions: 95000, clicks: 3200, ctr: 3.4, cpc: 1.09 },
      { name: 'Blog SEO Traffic', platform: 'google', spend: 2100, revenue: 15072, roas: 7.18, status: 'active', impressions: 520000, clicks: 18200, ctr: 3.5, cpc: 0.12 },
      { name: 'Churn Prevention', platform: 'email', spend: 400, revenue: 4220, roas: 10.55, status: 'active', impressions: 5200, clicks: 980, ctr: 18.8, cpc: 0.41 },
      { name: 'Product Hunt Launch', platform: 'meta', spend: 2800, revenue: 8200, roas: 2.93, status: 'active', impressions: 450000, clicks: 6800, ctr: 1.5, cpc: 0.41 },
    ],
    summary: {
      body: `<p>NovaTech had a <strong>solid March</strong> with <span class="hl">$94,200</span> in revenue — up <strong>18.5%</strong> month-over-month. Google Ads remains the primary driver at 48% of revenue, with the <strong>SaaS Demo Campaign</strong> delivering 4.31x ROAS.</p><p>The <strong>Blog SEO</strong> channel is quietly becoming a powerhouse — generating $15,072 in revenue on just $2,100 in content investment (7.18x ROAS). LinkedIn is performing adequately but the <strong>cost per click ($1.50+)</strong> needs attention.</p><p>Recommendation: <strong>Double down on content marketing</strong> and reduce LinkedIn spend by 30%, reallocating to Google retargeting where conversion rates are highest.</p>`,
      insights: [
        { type: 'win', title: 'Biggest Win', text: 'Blog SEO generated $15k on $2.1k spend — 7.18x ROAS with compounding value.' },
        { type: 'watch', title: 'Watch Closely', text: 'LinkedIn CPC at $1.50+ is above industry average. Needs creative refresh.' },
        { type: 'next', title: 'Next Move', text: 'Scale content budget 2x and test LinkedIn video ads to lower CPC.' },
      ],
    },
  },
  {
    id: 'elevate', name: 'Elevate Coaching', initials: 'EC',
    gradient: 'linear-gradient(135deg,#f59e0b,#ef4444)',
    niche: 'Coaching & Courses', activeCampaigns: 6,
    kpis: { revenue: 52800, revenueChange: 44.2, convRate: 6.1, convChange: 2.3, adSpend: 12600, spendChange: 12.0, roas: 4.19, roasChange: 0.68 },
    revenue: [
      { week: 'Wk 1', value: 8200, prev: 5800 }, { week: 'Wk 2', value: 11400, prev: 7200 },
      { week: 'Wk 3', value: 14800, prev: 9600 }, { week: 'Wk 4', value: 12600, prev: 10200 },
      { week: 'Wk 5', value: 5800, prev: 3890 },
    ],
    channels: [
      { name: 'Instagram Ads', pct: 38, value: 20064, color: '#f59e0b' },
      { name: 'YouTube', pct: 28, value: 14784, color: '#ef4444' },
      { name: 'Email Funnels', pct: 22, value: 11616, color: '#3ecf8e' },
      { name: 'Referral', pct: 12, value: 6336, color: '#6366f1' },
    ],
    performance: [
      { name: 'Instagram Ads', roas: 4.8, spend: 4180, revenue: 20064, conv: 7.2, barWidth: '78%', gradient: 'linear-gradient(90deg,#f59e0b,#fbbf24)' },
      { name: 'YouTube', roas: 3.4, spend: 4350, revenue: 14784, conv: 4.8, barWidth: '58%', gradient: 'linear-gradient(90deg,#ef4444,#f87171)' },
      { name: 'Email Funnels', roas: 19.4, spend: 600, revenue: 11616, conv: 9.8, barWidth: '45%', gradient: 'linear-gradient(90deg,#3ecf8e,#6ee7a8)' },
      { name: 'Referral', roas: Infinity, spend: 0, revenue: 6336, conv: 12.4, barWidth: '25%', gradient: 'linear-gradient(90deg,#6366f1,#818cf8)' },
    ],
    campaigns: [
      { name: 'Instagram Reels — Testimonial', platform: 'meta', spend: 2400, revenue: 12800, roas: 5.33, status: 'active', impressions: 680000, clicks: 14200, ctr: 2.1, cpc: 0.17 },
      { name: 'YouTube Pre-Roll', platform: 'google', spend: 2800, revenue: 10200, roas: 3.64, status: 'active', impressions: 920000, clicks: 9200, ctr: 1.0, cpc: 0.30 },
      { name: 'Webinar Funnel', platform: 'email', spend: 200, revenue: 6800, roas: 34.0, status: 'active', impressions: 12000, clicks: 3600, ctr: 30.0, cpc: 0.06 },
      { name: 'Instagram Story Ads', platform: 'meta', spend: 1780, revenue: 7264, roas: 4.08, status: 'active', impressions: 420000, clicks: 8400, ctr: 2.0, cpc: 0.21 },
      { name: 'YouTube Retargeting', platform: 'google', spend: 1550, revenue: 4584, roas: 2.96, status: 'active', impressions: 180000, clicks: 5400, ctr: 3.0, cpc: 0.29 },
      { name: 'Nurture Sequence', platform: 'email', spend: 400, revenue: 4816, roas: 12.04, status: 'active', impressions: 6800, clicks: 1360, ctr: 20.0, cpc: 0.29 },
    ],
    summary: {
      body: `<p>Elevate Coaching had its <strong>best month ever</strong> — <span class="hl">$52,800</span> in revenue, a <strong>44.2% jump</strong> from February. The Instagram Reels testimonial campaign was the star, driving $12,800 on just $2,400 in spend.</p><p>The <strong>Webinar Funnel</strong> email campaign delivered an exceptional 34x ROAS, proving that the high-touch coaching model thrives on email automation. YouTube is solid but the <strong>pre-roll format</strong> shows diminishing returns — consider shifting to long-form sponsorships.</p><p>Key insight: <strong>Referral revenue ($6,336) came at zero ad cost.</strong> Building a formal referral program could unlock significant growth.</p>`,
      insights: [
        { type: 'win', title: 'Biggest Win', text: "Webinar funnel hit 34x ROAS — email automation is this business's superpower." },
        { type: 'watch', title: 'Watch Closely', text: 'YouTube pre-roll CTR is declining. Creative fatigue setting in.' },
        { type: 'next', title: 'Next Move', text: 'Launch a formal referral program and double the webinar funnel frequency.' },
      ],
    },
  },
]

export const MOCK_REPORTS: Report[] = [
  { id: 'r1', clientId: 'brightedge', clientName: 'BrightEdge Digital', initials: 'BE', gradient: 'linear-gradient(135deg,#6366f1,#a855f7)', period: 'Mar 24–30, 2026', type: 'Weekly AI', status: 'sent', generatedAt: 'Mar 31, 2026', summary: MOCK_CLIENTS[0].summary },
  { id: 'r2', clientId: 'nova', clientName: 'NovaTech Solutions', initials: 'NT', gradient: 'linear-gradient(135deg,#3ecf8e,#0ea5e9)', period: 'Mar 24–30, 2026', type: 'Weekly AI', status: 'sent', generatedAt: 'Mar 31, 2026', summary: MOCK_CLIENTS[1].summary },
  { id: 'r3', clientId: 'elevate', clientName: 'Elevate Coaching', initials: 'EC', gradient: 'linear-gradient(135deg,#f59e0b,#ef4444)', period: 'Mar 24–30, 2026', type: 'Weekly AI', status: 'draft', generatedAt: 'Mar 31, 2026', summary: MOCK_CLIENTS[2].summary },
  { id: 'r4', clientId: 'brightedge', clientName: 'BrightEdge Digital', initials: 'BE', gradient: 'linear-gradient(135deg,#6366f1,#a855f7)', period: 'Mar 17–23, 2026', type: 'Weekly AI', status: 'sent', generatedAt: 'Mar 24, 2026', summary: { body: `<p>A solid mid-month week for BrightEdge Digital. Revenue reached <span class="hl">$47,200</span> with Meta campaigns leading at 5.1x ROAS. The Spring Collection creative continues to perform well, while Google Shopping saw a slight CTR dip worth monitoring.</p>`, insights: [{ type: 'win', title: 'Biggest Win', text: 'Meta Spring Collection maintained 5.1x ROAS through the full week.' }, { type: 'watch', title: 'Watch Closely', text: 'Google Shopping CTR dropped 0.4% — may need fresh ad creative.' }, { type: 'next', title: 'Next Move', text: 'Test a lookalike audience on Meta based on top 5% purchasers.' }] } },
  { id: 'r5', clientId: 'nova', clientName: 'NovaTech Solutions', initials: 'NT', gradient: 'linear-gradient(135deg,#3ecf8e,#0ea5e9)', period: 'Mar 17–23, 2026', type: 'Weekly AI', status: 'sent', generatedAt: 'Mar 24, 2026', summary: { body: `<p>NovaTech closed the week at <span class="hl">$22,800</span>. SaaS Demo Campaign continues to be the primary revenue driver. Blog SEO traffic grew 12% week-over-week, reinforcing the content strategy.</p>`, insights: [{ type: 'win', title: 'Biggest Win', text: 'Blog SEO traffic +12% WoW — organic compound growth taking hold.' }, { type: 'watch', title: 'Watch Closely', text: 'LinkedIn lead quality dropped slightly. Review targeting parameters.' }, { type: 'next', title: 'Next Move', text: 'Publish two more long-form SEO articles targeting high-intent keywords.' }] } },
  { id: 'r6', clientId: 'brightedge', clientName: 'BrightEdge Digital', initials: 'BE', gradient: 'linear-gradient(135deg,#6366f1,#a855f7)', period: 'March 2026', type: 'Monthly AI', status: 'sent', generatedAt: 'Apr 1, 2026', summary: MOCK_CLIENTS[0].summary },
]

export const DATE_RANGES: DateRange[] = [
  { id: 'this_month', label: 'This Month', value: 'Mar 1 – Mar 31, 2026' },
  { id: 'last_month', label: 'Last Month', value: 'Feb 1 – Feb 28, 2026' },
  { id: 'q1', label: 'Q1 2026', value: 'Jan 1 – Mar 31, 2026' },
  { id: 'last_90', label: 'Last 90 Days', value: 'Jan 2 – Mar 31, 2026' },
  { id: 'ytd', label: 'Year to Date', value: 'Jan 1 – Mar 31, 2026' },
]
