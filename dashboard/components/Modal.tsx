'use client'
import { useEffect } from 'react'
import type { Campaign, Report } from '@/lib/types'
import { fmt, platformLabel } from '@/lib/utils'

interface CampaignModalProps {
  campaign: Campaign
  allCampaigns: Campaign[]
  onClose: () => void
}

function roasColor(r: number) {
  if (r >= 4) return 'var(--green)'
  if (r >= 2.5) return 'var(--accent)'
  return 'var(--red)'
}

export function CampaignModal({ campaign, allCampaigns, onClose }: CampaignModalProps) {
  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === 'Escape') onClose() }
    document.addEventListener('keydown', handler)
    return () => document.removeEventListener('keydown', handler)
  }, [onClose])

  const maxImp = Math.max(...allCampaigns.map(c => c.impressions))
  const maxClick = Math.max(...allCampaigns.map(c => c.clicks))
  const maxSpend = Math.max(...allCampaigns.map(c => c.spend))
  const maxRev = Math.max(...allCampaigns.map(c => c.revenue))

  return (
    <div className="modal-overlay visible" onClick={e => { if (e.target === e.currentTarget) onClose() }}>
      <div className="modal">
        <div className="modal-header">
          <span style={{ fontFamily: "'Syne',sans-serif", fontWeight: 600 }}>Campaign Details</span>
          <button className="modal-close" onClick={onClose}>&times;</button>
        </div>
        <div className="modal-body">
          <div className="modal-campaign-name">{campaign.name}</div>
          <div className="modal-campaign-platform">
            <span className={`platform-tag ${campaign.platform}`}>
              <span className="dot" />{platformLabel(campaign.platform)}
            </span>
            <span className={`status-badge ${campaign.status}`} style={{ marginLeft: 8 }}>
              {campaign.status.charAt(0).toUpperCase() + campaign.status.slice(1)}
            </span>
          </div>
          <div className="modal-stats-grid">
            <div className="modal-stat"><div className="modal-stat-label">Spend</div><div className="modal-stat-value">{fmt(campaign.spend)}</div></div>
            <div className="modal-stat"><div className="modal-stat-label">Revenue</div><div className="modal-stat-value">{fmt(campaign.revenue)}</div></div>
            <div className="modal-stat"><div className="modal-stat-label">ROAS</div><div className="modal-stat-value" style={{ color: roasColor(campaign.roas) }}>{campaign.roas}x</div></div>
          </div>
          <div className="modal-section-title">Performance Breakdown</div>
          {[
            { label: 'Impressions', value: campaign.impressions.toLocaleString(), width: (campaign.impressions / maxImp * 100) + '%', color: 'var(--accent)' },
            { label: 'Clicks', value: campaign.clicks.toLocaleString(), width: (campaign.clicks / maxClick * 100) + '%', color: 'var(--blue)' },
            { label: 'CTR', value: campaign.ctr + '%', width: Math.min(campaign.ctr * 5, 100) + '%', color: 'var(--green)' },
            { label: 'CPC', value: '$' + campaign.cpc.toFixed(2), width: Math.min(campaign.cpc * 60, 100) + '%', color: 'var(--purple)' },
          ].map(row => (
            <div className="modal-bar" key={row.label}>
              <div className="modal-bar-label"><span>{row.label}</span><span>{row.value}</span></div>
              <div className="modal-bar-bg">
                <div className="modal-bar-fill" style={{ width: row.width, background: row.color }} />
              </div>
            </div>
          ))}
          <div className="modal-section-title" style={{ marginTop: 24 }}>Spend vs Revenue</div>
          {[
            { label: 'Spend', value: fmt(campaign.spend), width: (campaign.spend / maxSpend * 100) + '%', color: 'var(--red)' },
            { label: 'Revenue', value: fmt(campaign.revenue), width: (campaign.revenue / maxRev * 100) + '%', color: 'var(--green)' },
          ].map(row => (
            <div className="modal-bar" key={row.label}>
              <div className="modal-bar-label"><span>{row.label}</span><span>{row.value}</span></div>
              <div className="modal-bar-bg">
                <div className="modal-bar-fill" style={{ width: row.width, background: row.color }} />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

interface ReportModalProps {
  report: Report
  onClose: () => void
}

export function ReportModal({ report, onClose }: ReportModalProps) {
  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === 'Escape') onClose() }
    document.addEventListener('keydown', handler)
    return () => document.removeEventListener('keydown', handler)
  }, [onClose])

  const s = report.summary
  return (
    <div className="modal-overlay visible" onClick={e => { if (e.target === e.currentTarget) onClose() }}>
      <div className="modal">
        <div className="modal-header">
          <span style={{ fontFamily: "'Syne',sans-serif", fontWeight: 600 }}>
            {report.clientName}
            <span style={{ color: 'var(--text-muted)', fontWeight: 400, fontSize: 13, marginLeft: 10 }}>{report.period}</span>
          </span>
          <button className="modal-close" onClick={onClose}>&times;</button>
        </div>
        <div className="modal-body">
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 20, flexWrap: 'wrap' }}>
            <span className="platform-tag" style={{ background: 'var(--accent-dim)', color: 'var(--accent)', border: 'none' }}>{report.type}</span>
            <span className={`status-badge ${report.status}`}>{report.status === 'sent' ? '✓ Sent' : '⏳ Draft'}</span>
            <span style={{ fontSize: 12, color: 'var(--text-muted)', marginLeft: 'auto' }}>Generated {report.generatedAt}</span>
          </div>
          <div className="summary-body" style={{ marginBottom: 20 }} dangerouslySetInnerHTML={{ __html: s.body }} />
          <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
            {s.insights.map(ins => (
              <div className="insight-item" key={ins.type}>
                <div className={`insight-icon ${ins.type}`}>{ins.type === 'win' ? '🏆' : ins.type === 'watch' ? '⚠️' : '🚀'}</div>
                <div className="insight-text"><strong>{ins.title}</strong> {ins.text}</div>
              </div>
            ))}
          </div>
          <div style={{ display: 'flex', gap: 10, marginTop: 24, paddingTop: 20, borderTop: '1px solid var(--border)' }}>
            <button className="btn-print" onClick={() => window.print()} style={{ fontSize: 12, padding: '8px 16px' }}>
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <polyline points="6 9 6 2 18 2 18 9" /><path d="M6 18H4a2 2 0 01-2-2v-5a2 2 0 012-2h16a2 2 0 012 2v5a2 2 0 01-2 2h-2" /><rect x="6" y="14" width="12" height="8" />
              </svg>
              Print
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
