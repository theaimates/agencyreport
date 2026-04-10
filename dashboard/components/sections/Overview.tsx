'use client'
import { useState, useEffect, useRef, useCallback } from 'react'
import type { Client, Campaign } from '@/lib/types'
import { fmt, fmtK, roasClass, platformLabel } from '@/lib/utils'
import RevenueChart from '@/components/charts/RevenueChart'
import DonutChart from '@/components/charts/DonutChart'
import { CampaignModal } from '@/components/Modal'

interface Props {
  client: Client
  searchQuery: string
  onSearchChange: (q: string) => void
  sortColumn: string | null
  sortDirection: 'asc' | 'desc' | 'default'
  onSort: (col: string) => void
  platformFilter: string
  onPlatformFilter: (f: string) => void
}

function useCounterAnimation(target: number, decimals = 0) {
  const [display, setDisplay] = useState(0)
  useEffect(() => {
    const duration = 1200
    const start = performance.now()
    const tick = (now: number) => {
      const elapsed = now - start
      const progress = Math.min(elapsed / duration, 1)
      const eased = 1 - Math.pow(1 - progress, 3)
      setDisplay(target * eased)
      if (progress < 1) requestAnimationFrame(tick)
    }
    requestAnimationFrame(tick)
  }, [target])
  return decimals > 0 ? display.toFixed(decimals) : Math.round(display).toLocaleString('en-US')
}

function KpiCounter({ value, prefix = '', suffix = '', decimals = 0 }: { value: number; prefix?: string; suffix?: string; decimals?: number }) {
  const display = useCounterAnimation(value, decimals)
  return <>{prefix}{display}{suffix}</>
}

function Clock() {
  const [time, setTime] = useState('')
  useEffect(() => {
    const update = () => setTime('Last synced: ' + new Date().toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', second: '2-digit' }))
    update()
    const id = setInterval(update, 1000)
    return () => clearInterval(id)
  }, [])
  return <span id="live-clock">{time}</span>
}

const COLS = [
  { key: 'name', label: 'Campaign' },
  { key: 'platform', label: 'Platform' },
  { key: 'spend', label: 'Spend' },
  { key: 'revenue', label: 'Revenue' },
  { key: 'roas', label: 'ROAS' },
  { key: 'status', label: 'Status' },
]

export default function Overview({ client, searchQuery, onSearchChange, sortColumn, sortDirection, onSort, platformFilter, onPlatformFilter }: Props) {
  const [modalCampaign, setModalCampaign] = useState<Campaign | null>(null)
  const k = client.kpis

  let campaigns = [...(client.campaigns || [])]
  if (platformFilter && platformFilter !== 'all') {
    campaigns = campaigns.filter(c => c.platform === platformFilter)
  }
  if (searchQuery) {
    const q = searchQuery.toLowerCase()
    campaigns = campaigns.filter(c =>
      c.name.toLowerCase().includes(q) || c.platform.toLowerCase().includes(q) || c.status.toLowerCase().includes(q)
    )
  }
  if (sortColumn) {
    campaigns.sort((a, b) => {
      let va = (a as any)[sortColumn], vb = (b as any)[sortColumn]
      if (typeof va === 'string') va = va.toLowerCase()
      if (typeof vb === 'string') vb = vb.toLowerCase()
      if (sortDirection === 'asc') return va > vb ? 1 : va < vb ? -1 : 0
      return va < vb ? 1 : va > vb ? -1 : 0
    })
  }

  function sortArrow(key: string) {
    if (sortColumn !== key) return <span className="sort-arrow">↕</span>
    return <span className="sort-arrow">{sortDirection === 'asc' ? '↑' : '↓'}</span>
  }

  return (
    <>
      {/* KPIs */}
      <div className="section-header">
        <span className="section-title">Key Metrics</span>
        <span className="section-badge">vs. Previous Period</span>
      </div>
      <div className="kpi-grid">
        {[
          { label: 'Total Revenue', value: k.revenue, change: k.revenueChange, prefix: '$', context: `${k.revenueChange >= 0 ? '+' : ''}${fmt(Math.round(k.revenue * k.revenueChange / 100))}` },
          { label: 'Conversion Rate', value: k.convRate, change: k.convChange, suffix: '%', decimals: 1, context: `from ${(k.convRate - k.convChange).toFixed(1)}%` },
          { label: 'Ad Spend', value: k.adSpend, change: k.spendChange, prefix: '$', invertColor: true, context: `${k.spendChange <= 0 ? '' : '+'}${fmt(Math.round(Math.abs(k.adSpend * k.spendChange / 100)))} ${k.spendChange <= 0 ? 'saved' : 'added'}` },
          { label: 'ROAS', value: k.roas, change: k.roasChange, suffix: 'x', decimals: 2, context: `from ${(k.roas - k.roasChange).toFixed(2)}x` },
        ].map(kpi => {
          const positive = kpi.invertColor ? kpi.change <= 0 : kpi.change >= 0
          return (
            <div className="kpi-card" key={kpi.label}>
              <div className="kpi-label">{kpi.label}</div>
              <div className="kpi-value">
                <KpiCounter value={kpi.value} prefix={kpi.prefix} suffix={kpi.suffix} decimals={kpi.decimals} />
              </div>
              <div className="kpi-meta">
                <span className={`kpi-change ${positive ? 'positive' : 'negative'}`}>
                  {kpi.change >= 0 ? '+' : ''}{kpi.change}{kpi.suffix || (kpi.prefix ? '' : '')}
                </span>
                <span className="kpi-context">{kpi.context}</span>
              </div>
            </div>
          )
        })}
      </div>

      {/* Charts */}
      <div className="charts-grid">
        <div className="chart-card">
          <div className="section-header" style={{ marginBottom: 6 }}>
            <span className="section-title">Revenue Trend</span>
            <span className="section-badge">Weekly</span>
          </div>
          <RevenueChart data={client.revenue} />
        </div>
        <div className="chart-card">
          <div className="section-header" style={{ marginBottom: 6 }}>
            <span className="section-title">Channel Mix</span>
            <span className="section-badge">By Revenue</span>
          </div>
          <DonutChart channels={client.channels} />
        </div>
      </div>

      {/* Performance */}
      <div className="performance-section">
        <div className="section-header">
          <span className="section-title">Channel Performance</span>
          <span className="section-badge">Current Period</span>
        </div>
        <div className="perf-grid">
          {(client.performance || []).map(p => (
            <div className="perf-card" key={p.name}>
              <div className="perf-header">
                <span className="perf-channel">{p.name}</span>
                <span className="perf-roas">ROAS <strong>{p.roas === Infinity ? '∞' : p.roas + 'x'}</strong></span>
              </div>
              <div className="perf-bar-bg">
                <div className="perf-bar-fill" style={{ ['--bar-width' as any]: p.barWidth, background: p.gradient }} />
              </div>
              <div className="perf-stats">
                <div className="perf-stat"><span className="perf-stat-label">Spend</span><span className="perf-stat-value">{fmt(p.spend)}</span></div>
                <div className="perf-stat"><span className="perf-stat-label">Revenue</span><span className="perf-stat-value">{fmt(p.revenue)}</span></div>
                <div className="perf-stat"><span className="perf-stat-label">Conv.</span><span className="perf-stat-value">{p.conv}%</span></div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Campaign Table */}
      <div className="table-section">
        <div className="section-header">
          <span className="section-title">Top Campaigns</span>
          <div className="table-controls">
            <div className="search-wrap">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="11" cy="11" r="8" /><path d="M21 21l-4.35-4.35" /></svg>
              <input
                className="search-input"
                type="text"
                placeholder="Search campaigns..."
                value={searchQuery}
                onChange={e => onSearchChange(e.target.value)}
              />
            </div>
            <span className="section-badge">{campaigns.length} active</span>
          </div>
        </div>
        <div className="table-card">
          {campaigns.length === 0 ? (
            <div className="no-results">No campaigns match &ldquo;{searchQuery}&rdquo;</div>
          ) : (
            <table className="campaign-table">
              <thead>
                <tr>
                  {COLS.map(col => (
                    <th
                      key={col.key}
                      data-col={col.key}
                      className={sortColumn === col.key ? 'sorted' : ''}
                      onClick={() => onSort(col.key)}
                    >
                      {col.label} {sortArrow(col.key)}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {campaigns.map(camp => (
                  <tr key={camp.name} onClick={() => setModalCampaign(camp)} style={{ cursor: 'pointer' }}>
                    <td className="campaign-name">{camp.name}</td>
                    <td><span className={`platform-tag ${camp.platform}`}><span className="dot" />{platformLabel(camp.platform)}</span></td>
                    <td>{fmt(camp.spend)}</td>
                    <td>{fmt(camp.revenue)}</td>
                    <td className={roasClass(camp.roas)}>{camp.roas}x</td>
                    <td><span className={`status-badge ${camp.status}`}>{camp.status.charAt(0).toUpperCase() + camp.status.slice(1)}</span></td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>

      {/* AI Summary */}
      <div className="summary-section">
        <div className="section-header">
          <span className="section-title">AI Analysis</span>
          <span className="section-badge">{client._isLive ? 'Live · Auto-generated' : 'Demo data'}</span>
        </div>
        <div className="summary-card">
          <div className="summary-header">
            <div className="ai-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
            </div>
            <span className="summary-title">Performance Summary</span>
            <span className="summary-subtitle">
              Auto-generated · {new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
            </span>
          </div>
          <div className="summary-body" dangerouslySetInnerHTML={{ __html: client.summary.body }} />
          <div className="summary-insights">
            {client.summary.insights.map(ins => (
              <div className="insight-item" key={ins.type}>
                <div className={`insight-icon ${ins.type}`}>{ins.type === 'win' ? '🏆' : ins.type === 'watch' ? '⚠️' : '🚀'}</div>
                <div className="insight-text"><strong>{ins.title}</strong> {ins.text}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="dashboard-footer">
        <div className="footer-brand"><span className="footer-dot" />ReportFlow</div>
        <Clock />
      </div>

      {modalCampaign && (
        <CampaignModal
          campaign={modalCampaign}
          allCampaigns={client.campaigns}
          onClose={() => setModalCampaign(null)}
        />
      )}
    </>
  )
}
