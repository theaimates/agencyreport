'use client'
import type { Section } from '@/hooks/useDashboardState'

const NAV_ITEMS: { section: Section; label: string; icon: React.ReactNode }[] = [
  {
    section: 'overview', label: 'Dashboard',
    icon: <svg className="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/></svg>,
  },
  {
    section: 'clients', label: 'Clients',
    icon: <svg className="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><path d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/></svg>,
  },
  {
    section: 'reports', label: 'Reports',
    icon: <svg className="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>,
  },
  {
    section: 'settings', label: 'Settings',
    icon: <svg className="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><path d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.066 2.573c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.573 1.066c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.066-2.573c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><circle cx="12" cy="12" r="3"/></svg>,
  },
]

interface Props {
  activeSection: Section
  isOpen: boolean
  onNavigate: (section: Section) => void
  onClose: () => void
}

export default function Sidebar({ activeSection, isOpen, onNavigate, onClose }: Props) {
  return (
    <aside className={`sidebar${isOpen ? ' open' : ''}`}>
      <div className="logo">
        <div className="logo-mark">R</div>
        <span className="logo-text">ReportFlow</span>
      </div>
      <nav className="nav-section">
        {NAV_ITEMS.map(item => (
          <button
            key={item.section}
            className={`nav-item${activeSection === item.section ? ' active' : ''}`}
            onClick={() => { onNavigate(item.section); onClose() }}
          >
            {item.icon}
            {item.label}
          </button>
        ))}
      </nav>
      <div className="integrations">
        <div className="integrations-title">Connected</div>
        <div className="integration-item"><span className="status-dot" /> Google Analytics</div>
        <div className="integration-item"><span className="status-dot" /> Meta Business</div>
        <div className="integration-item"><span className="status-dot" /> Stripe</div>
        <div className="integration-item"><span className="status-dot" /> Mailchimp</div>
      </div>
      <a
        href="https://theaimates.com"
        target="_blank"
        rel="noopener noreferrer"
        className="built-by-cta"
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" className="built-by-icon"><path d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
        BUILT THIS!
      </a>
    </aside>
  )
}
