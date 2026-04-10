'use client'
import type { Client } from '@/lib/types'
import { fmtK } from '@/lib/utils'

interface Props {
  clients: Client[]
  activeClientIdx: number
  onViewDashboard: (idx: number) => void
  onViewReports: (idx: number) => void
}

export default function Clients({ clients, activeClientIdx, onViewDashboard, onViewReports }: Props) {
  return (
    <div style={{ opacity: 0, animation: 'fadeUp .4s ease forwards' }}>
      <div className="section-header">
        <span className="section-title">Clients</span>
        <span className="section-badge">{clients.length} active</span>
      </div>
      <div className="clients-grid">
        {clients.map((cl, i) => (
          <div className={`client-card${i === activeClientIdx ? ' active-client' : ''}`} key={cl.id}>
            <div className="client-card-header">
              <div className="client-card-avatar" style={{ background: cl.gradient }}>{cl.initials}</div>
              <div>
                <div className="client-card-name">{cl.name}</div>
                <div className="client-card-niche">{cl.niche} · {cl.activeCampaigns} campaigns</div>
              </div>
            </div>
            <div className="client-card-stats">
              <div>
                <div className="client-stat-label">Revenue</div>
                <div className="client-stat-value">{fmtK(cl.kpis.revenue)}</div>
              </div>
              <div>
                <div className="client-stat-label">ROAS</div>
                <div className="client-stat-value">{cl.kpis.roas}x</div>
              </div>
              <div>
                <div className="client-stat-label">MoM</div>
                <div className="client-stat-value" style={{ color: cl.kpis.revenueChange >= 0 ? 'var(--green)' : 'var(--red)' }}>
                  {cl.kpis.revenueChange >= 0 ? '+' : ''}{cl.kpis.revenueChange}%
                </div>
              </div>
            </div>
            <div style={{ display: 'flex', gap: 8 }}>
              <button
                className="btn-view-client"
                style={{ flex: 1 }}
                onClick={() => onViewDashboard(i)}
              >
                {i === activeClientIdx ? '▦ Viewing' : '→ Dashboard'}
              </button>
              <button
                className="btn-view-client"
                style={{ flex: 1, background: 'transparent', color: 'var(--text-muted)', borderColor: 'var(--border)' }}
                onClick={() => onViewReports(i)}
              >
                📋 Reports
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
