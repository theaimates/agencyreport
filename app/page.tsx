'use client'
import { useEffect, useState } from 'react'
import { useDashboardState } from '@/hooks/useDashboardState'
import { DATE_RANGES } from '@/lib/mockData'
import Sidebar from '@/components/Sidebar'
import Topbar from '@/components/Topbar'
import Overview from '@/components/sections/Overview'
import Clients from '@/components/sections/Clients'
import Reports from '@/components/sections/Reports'
import Settings from '@/components/sections/Settings'

export default function Page() {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const {
    state, setState,
    getClients, getClient,
    loadDashboard, initLiveClients,
    setSection, setActiveClient, setActiveDateRange,
    setSort, toggleClientDropdown, toggleDateDropdown,
    resetToDemo,
  } = useDashboardState()

  // On mount: try to fetch live clients, then load dashboard
  useEffect(() => {
    initLiveClients().then(() => loadDashboard())
  }, []) // eslint-disable-line react-hooks/exhaustive-deps

  const client = getClient()
  const clients = getClients()

  function handleSelectClient(idx: number) {
    setActiveClient(idx)
    loadDashboard(idx, state.activeDateRangeIdx)
  }

  function handleSelectDateRange(idx: number) {
    setActiveDateRange(idx)
    loadDashboard(state.activeClientIdx, idx)
  }

  function handleViewDashboard(idx: number) {
    setActiveClient(idx)
    setSection('overview')
    loadDashboard(idx, state.activeDateRangeIdx)
  }

  function handleViewReports(idx: number) {
    setActiveClient(idx)
    setState(s => ({ ...s, reportClientFilter: clients[idx].id, activeSection: 'reports' }))
  }

  return (
    <>
      {/* Mobile toggle */}
      <button className="mobile-toggle" aria-label="Toggle menu" onClick={() => setSidebarOpen(v => !v)}>
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>

      <Sidebar
        activeSection={state.activeSection}
        isOpen={sidebarOpen}
        onNavigate={section => { setSection(section); setSidebarOpen(false) }}
        onClose={() => setSidebarOpen(false)}
      />

      <Topbar
        client={client}
        clients={clients as any}
        activeClientIdx={state.activeClientIdx}
        dateRanges={DATE_RANGES}
        activeDateRangeIdx={state.activeDateRangeIdx}
        clientDropdownOpen={state.clientDropdownOpen}
        dateDropdownOpen={state.dateDropdownOpen}
        onToggleClientDropdown={toggleClientDropdown}
        onToggleDateDropdown={toggleDateDropdown}
        onSelectClient={handleSelectClient}
        onSelectDateRange={handleSelectDateRange}
        onCloseAll={() => { toggleClientDropdown(false); toggleDateDropdown(false) }}
      />

      <main className="main">
        <div className="content">
          {state.loading && (
            <div className="loading-overlay visible">
              <div className="loading-spinner" />
            </div>
          )}

          {state.activeSection === 'overview' && (
            <Overview
              client={client}
              searchQuery={state.searchQuery}
              onSearchChange={q => setState(s => ({ ...s, searchQuery: q }))}
              sortColumn={state.sortColumn}
              sortDirection={state.sortDirection}
              onSort={setSort}
              platformFilter={state.platformFilter}
              onPlatformFilter={f => setState(s => ({ ...s, platformFilter: f }))}
            />
          )}

          {state.activeSection === 'clients' && (
            <Clients
              clients={clients as any}
              activeClientIdx={state.activeClientIdx}
              onViewDashboard={handleViewDashboard}
              onViewReports={handleViewReports}
            />
          )}

          {state.activeSection === 'reports' && (
            <Reports
              clients={clients as any}
              reportClientFilter={state.reportClientFilter}
              onFilterChange={id => setState(s => ({ ...s, reportClientFilter: id }))}
            />
          )}

          {state.activeSection === 'settings' && (
            <Settings onReset={resetToDemo} />
          )}
        </div>
      </main>

      {/* Demo mode toast */}
      {!state.liveClientData && !state.loading && (
        <div className="error-toast visible">
          <strong>Demo mode</strong>
          Connect n8n in Settings to load live data.
        </div>
      )}
    </>
  )
}
