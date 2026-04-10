'use client'
import { useRef, useEffect } from 'react'
import type { Client, DateRange } from '@/lib/types'

interface Props {
  client: Client
  dateRanges: DateRange[]
  activeDateRangeIdx: number
  clientDropdownOpen: boolean
  dateDropdownOpen: boolean
  clients: Client[]
  activeClientIdx: number
  onToggleClientDropdown: () => void
  onToggleDateDropdown: () => void
  onSelectClient: (idx: number) => void
  onSelectDateRange: (idx: number) => void
  onCloseAll: () => void
}

export default function Topbar({
  client, dateRanges, activeDateRangeIdx,
  clientDropdownOpen, dateDropdownOpen,
  clients, activeClientIdx,
  onToggleClientDropdown, onToggleDateDropdown,
  onSelectClient, onSelectDateRange, onCloseAll,
}: Props) {
  const clientRef = useRef<HTMLDivElement>(null)
  const dateRef = useRef<HTMLDivElement>(null)

  // Close dropdowns on outside click
  useEffect(() => {
    function handler(e: MouseEvent) {
      if (!clientRef.current?.contains(e.target as Node)) {
        if (clientDropdownOpen) onCloseAll()
      }
      if (!dateRef.current?.contains(e.target as Node)) {
        if (dateDropdownOpen) onCloseAll()
      }
    }
    document.addEventListener('mousedown', handler)
    return () => document.removeEventListener('mousedown', handler)
  }, [clientDropdownOpen, dateDropdownOpen, onCloseAll])

  return (
    <header className="topbar">
      <div
        className={`client-selector${clientDropdownOpen ? ' open' : ''}`}
        ref={clientRef}
        onClick={onToggleClientDropdown}
      >
        <div className="client-avatar" style={{ background: client.gradient }}>{client.initials}</div>
        <div className="client-info">
          <h2>{client.name}</h2>
          <span>{client.niche} &middot; {client.activeCampaigns} campaigns active</span>
        </div>
        <svg className="chevron-down" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M6 9l6 6 6-6" />
        </svg>
        <div className="client-dropdown">
          {clients.map((c, i) => (
            <div
              key={c.id}
              className={`client-option${i === activeClientIdx ? ' selected' : ''}`}
              onClick={e => { e.stopPropagation(); onSelectClient(i) }}
            >
              <div className="client-option-avatar" style={{ background: c.gradient }}>{c.initials}</div>
              <div className="client-option-info">
                <span className="client-option-name">{c.name}</span>
                <span className="client-option-meta">{c.niche} · {c.activeCampaigns} campaigns</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="topbar-actions">
        <div className="date-badge" ref={dateRef} onClick={e => { e.stopPropagation(); onToggleDateDropdown() }}>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
            <rect x="3" y="4" width="18" height="18" rx="2" /><path d="M16 2v4M8 2v4M3 10h18" />
          </svg>
          <span>{dateRanges[activeDateRangeIdx].value}</span>
          <div className={`date-dropdown${dateDropdownOpen ? ' open' : ''}`}>
            {dateRanges.map((d, i) => (
              <div
                key={d.id}
                className={`date-option${i === activeDateRangeIdx ? ' selected' : ''}`}
                onClick={e => { e.stopPropagation(); onSelectDateRange(i) }}
              >
                {d.label}
              </div>
            ))}
          </div>
        </div>
        <button className="btn-export" onClick={() => window.print()}>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <span>Export PDF</span>
        </button>
      </div>
    </header>
  )
}
