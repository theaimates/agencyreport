'use client'
import { useState } from 'react'
import type { Report, Client } from '@/lib/types'
import { MOCK_REPORTS } from '@/lib/mockData'
import { ReportModal } from '@/components/Modal'

interface Props {
  clients: Client[]
  reportClientFilter: string | null
  onFilterChange: (id: string | null) => void
}

export default function Reports({ clients, reportClientFilter, onFilterChange }: Props) {
  const [openReport, setOpenReport] = useState<Report | null>(null)

  const active = reportClientFilter || 'all'
  const filtered = active === 'all' ? MOCK_REPORTS : MOCK_REPORTS.filter(r => r.clientId === active)

  const clientFilters = [
    { id: 'all', label: 'All Clients' },
    ...clients.map(cl => ({ id: cl.id, label: cl.initials })),
  ]

  return (
    <div style={{ opacity: 0, animation: 'fadeUp .4s ease forwards' }}>
      <div className="section-header">
        <span className="section-title">Reports</span>
        <span className="section-badge">{filtered.length} report{filtered.length !== 1 ? 's' : ''}</span>
      </div>
      <div className="filter-tabs" style={{ marginBottom: 20 }}>
        {clientFilters.map(f => (
          <button
            key={f.id}
            className={`filter-tab${active === f.id ? ' active' : ''}`}
            onClick={() => onFilterChange(f.id === 'all' ? null : f.id)}
          >
            {f.label}
          </button>
        ))}
      </div>
      <div className="table-card">
        {filtered.length === 0 ? (
          <div className="no-results">No reports found</div>
        ) : (
          <table className="campaign-table">
            <thead>
              <tr>
                <th>Period</th>
                <th>Client</th>
                <th>Type</th>
                <th>Generated</th>
                <th>Status</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {filtered.map(r => (
                <tr key={r.id}>
                  <td className="campaign-name">{r.period}</td>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                      <div style={{ width: 24, height: 24, borderRadius: 6, background: r.gradient, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 9, fontWeight: 700, color: '#fff', flexShrink: 0 }}>
                        {r.initials}
                      </div>
                      {r.clientName}
                    </div>
                  </td>
                  <td><span className="platform-tag" style={{ background: 'var(--accent-dim)', color: 'var(--accent)', border: 'none' }}>{r.type}</span></td>
                  <td style={{ color: 'var(--text-muted)', fontSize: 12 }}>{r.generatedAt}</td>
                  <td><span className={`status-badge ${r.status}`}>{r.status === 'sent' ? '✓ Sent' : '⏳ Draft'}</span></td>
                  <td>
                    <button className="btn-view-report" onClick={() => setOpenReport(r)}>View →</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {openReport && <ReportModal report={openReport} onClose={() => setOpenReport(null)} />}
    </div>
  )
}
