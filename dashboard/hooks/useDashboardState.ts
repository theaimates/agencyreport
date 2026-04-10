'use client'
import { useState, useEffect, useCallback } from 'react'
import type { Client } from '@/lib/types'
import { MOCK_CLIENTS, DATE_RANGES } from '@/lib/mockData'
import { fetchClients, fetchDashboard } from '@/lib/api'

export type Section = 'overview' | 'clients' | 'reports' | 'settings'
export type SortDirection = 'asc' | 'desc' | 'default'

interface DashboardState {
  activeClientIdx: number
  activeSection: Section
  activeDateRangeIdx: number
  platformFilter: string
  reportClientFilter: string | null
  sortColumn: string | null
  sortDirection: SortDirection
  searchQuery: string
  liveClients: typeof MOCK_CLIENTS | null
  liveClientData: Client | null
  loading: boolean
  clientDropdownOpen: boolean
  dateDropdownOpen: boolean
}

const STORAGE_KEY = 'reportflow_state'

function loadPersistedState(): Partial<DashboardState> {
  if (typeof window === 'undefined') return {}
  try {
    const s = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}')
    return {
      activeClientIdx: s.activeClient ?? 0,
      activeSection: s.activeSection ?? 'overview',
      activeDateRangeIdx: s.activeDateRange ?? 0,
      platformFilter: s.platformFilter ?? 'all',
      reportClientFilter: s.reportClientFilter ?? null,
    }
  } catch { return {} }
}

export function useDashboardState() {
  const [state, setState] = useState<DashboardState>(() => ({
    activeClientIdx: 0,
    activeSection: 'overview',
    activeDateRangeIdx: 0,
    platformFilter: 'all',
    reportClientFilter: null,
    sortColumn: null,
    sortDirection: 'default',
    searchQuery: '',
    liveClients: null,
    liveClientData: null,
    loading: false,
    clientDropdownOpen: false,
    dateDropdownOpen: false,
  }))

  // Hydrate from localStorage on mount
  useEffect(() => {
    const persisted = loadPersistedState()
    if (Object.keys(persisted).length) {
      setState(s => ({ ...s, ...persisted }))
    }
  }, [])

  // Persist key state on change
  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify({
        activeClient: state.activeClientIdx,
        activeSection: state.activeSection,
        activeDateRange: state.activeDateRangeIdx,
        platformFilter: state.platformFilter,
        reportClientFilter: state.reportClientFilter,
      }))
    } catch {}
  }, [state.activeClientIdx, state.activeSection, state.activeDateRangeIdx, state.platformFilter, state.reportClientFilter])

  const getClients = useCallback(() => state.liveClients || MOCK_CLIENTS, [state.liveClients])

  const getClient = useCallback((): Client => {
    if (state.liveClientData) return state.liveClientData
    const clients = state.liveClients || MOCK_CLIENTS
    return clients[Math.min(state.activeClientIdx, clients.length - 1)]
  }, [state.liveClientData, state.liveClients, state.activeClientIdx])

  const loadDashboard = useCallback(async (clientIdxOverride?: number, dateIdxOverride?: number) => {
    const clients = state.liveClients || MOCK_CLIENTS
    const clientIdx = clientIdxOverride ?? state.activeClientIdx
    const dateIdx = dateIdxOverride ?? state.activeDateRangeIdx
    const clientId = clients[clientIdx]?.id
    const dateRangeId = DATE_RANGES[dateIdx].id
    if (!clientId) return

    setState(s => ({ ...s, loading: true }))
    const data = await fetchDashboard(clientId, dateRangeId)
    setState(s => ({
      ...s,
      loading: false,
      liveClientData: data || null,
    }))
  }, [state.liveClients, state.activeClientIdx, state.activeDateRangeIdx])

  const initLiveClients = useCallback(async () => {
    const live = await fetchClients()
    if (live && live.length) {
      setState(s => {
        const safeIdx = s.activeClientIdx >= live.length ? 0 : s.activeClientIdx
        return { ...s, liveClients: live as any, activeClientIdx: safeIdx }
      })
    }
  }, [])

  const setSection = useCallback((section: Section) => {
    setState(s => ({ ...s, activeSection: section }))
  }, [])

  const setActiveClient = useCallback((idx: number) => {
    setState(s => ({
      ...s,
      activeClientIdx: idx,
      liveClientData: null,
      sortColumn: null,
      sortDirection: 'default',
      searchQuery: '',
      clientDropdownOpen: false,
    }))
  }, [])

  const setActiveDateRange = useCallback((idx: number) => {
    setState(s => ({ ...s, activeDateRangeIdx: idx, liveClientData: null, dateDropdownOpen: false }))
  }, [])

  const setSort = useCallback((col: string) => {
    setState(s => {
      if (s.sortColumn === col) {
        const next: SortDirection = s.sortDirection === 'asc' ? 'desc' : s.sortDirection === 'desc' ? 'default' : 'asc'
        return { ...s, sortDirection: next, sortColumn: next === 'default' ? null : col }
      }
      return { ...s, sortColumn: col, sortDirection: 'asc' }
    })
  }, [])

  const toggleClientDropdown = useCallback((force?: boolean) => {
    setState(s => ({
      ...s,
      clientDropdownOpen: force !== undefined ? force : !s.clientDropdownOpen,
      dateDropdownOpen: false,
    }))
  }, [])

  const toggleDateDropdown = useCallback((force?: boolean) => {
    setState(s => ({
      ...s,
      dateDropdownOpen: force !== undefined ? force : !s.dateDropdownOpen,
      clientDropdownOpen: false,
    }))
  }, [])

  const resetToDemo = useCallback(() => {
    localStorage.removeItem(STORAGE_KEY)
    localStorage.removeItem('reportflow_n8n_url')
    localStorage.removeItem('reportflow_webhook_secret')
    setState(s => ({ ...s, liveClients: null, liveClientData: null }))
  }, [])

  return {
    state,
    setState,
    getClients,
    getClient,
    loadDashboard,
    initLiveClients,
    setSection,
    setActiveClient,
    setActiveDateRange,
    setSort,
    toggleClientDropdown,
    toggleDateDropdown,
    resetToDemo,
  }
}
