'use client'
import { useState, useRef } from 'react'
import { fetchClients } from '@/lib/api'

interface Props {
  onReset: () => void
}

const INTEGRATIONS = [
  { name: 'Google Analytics 4', dot: 'var(--green)', status: 'Connected', sub: 'Last sync: today at 6:00 AM' },
  { name: 'Meta Business Suite', dot: 'var(--green)', status: 'Connected', sub: 'Last sync: today at 6:00 AM' },
  { name: 'Google Ads', dot: 'var(--green)', status: 'Connected', sub: 'Last sync: today at 6:00 AM' },
  { name: 'Stripe', dot: 'var(--green)', status: 'Connected', sub: 'Last sync: today at 6:00 AM' },
  { name: 'Mailchimp', dot: 'var(--accent)', status: 'Check token', sub: 'Tokens expire every 60 days' },
]

export default function Settings({ onReset }: Props) {
  const urlRef = useRef<HTMLInputElement>(null)
  const secretRef = useRef<HTMLInputElement>(null)
  const [showSecret, setShowSecret] = useState(false)
  const [connStatus, setConnStatus] = useState<{ type: 'ok' | 'fail' | null; msg: string }>({ type: null, msg: '' })
  const [testing, setTesting] = useState(false)

  function getSavedUrl() {
    if (typeof window === 'undefined') return ''
    const saved = localStorage.getItem('reportflow_n8n_url')
    return saved && saved !== 'http://localhost:5678' ? saved : ''
  }

  function handleSave() {
    const url = urlRef.current?.value.trim()
    const secret = secretRef.current?.value.trim()
    if (url) localStorage.setItem('reportflow_n8n_url', url.replace(/\/$/, ''))
    if (secret) localStorage.setItem('reportflow_webhook_secret', secret)
    else localStorage.removeItem('reportflow_webhook_secret')
    setConnStatus({ type: 'ok', msg: '✓ Saved — reconnecting…' })
  }

  async function handleTest() {
    setTesting(true)
    setConnStatus({ type: null, msg: '' })
    const url = urlRef.current?.value.trim()
    if (url) localStorage.setItem('reportflow_n8n_url', url.replace(/\/$/, ''))
    const clients = await fetchClients()
    setTesting(false)
    if (clients && clients.length) {
      setConnStatus({ type: 'ok', msg: `✓ Connected — ${clients.length} client${clients.length !== 1 ? 's' : ''} found` })
    } else {
      setConnStatus({ type: 'fail', msg: '✗ Could not reach n8n — check URL and that WF6 is active' })
    }
  }

  function handleReset() {
    if (urlRef.current) urlRef.current.value = ''
    if (secretRef.current) secretRef.current.value = ''
    setConnStatus({ type: 'ok', msg: '✓ Reset — showing demo data' })
    onReset()
  }

  return (
    <div style={{ opacity: 0, animation: 'fadeUp .4s ease forwards' }}>
      <div className="section-header">
        <span className="section-title">Settings &amp; Integrations</span>
      </div>
      <div className="settings-grid">

        <div className="settings-card">
          <div className="settings-card-title">n8n Connection</div>
          <div className="settings-card-desc">Connect this dashboard to your self-hosted n8n instance to load live Airtable data.</div>
          <div className="settings-field">
            <label className="settings-label">n8n Instance URL</label>
            <input ref={urlRef} className="settings-input" type="url" placeholder="https://your-n8n-instance.com" defaultValue={getSavedUrl()} />
          </div>
          <div className="settings-field">
            <label className="settings-label">Webhook Secret <span style={{ color: 'var(--text-dim)' }}>(optional)</span></label>
            <div className="settings-secret-wrap">
              <input ref={secretRef} className="settings-input" type={showSecret ? 'text' : 'password'} placeholder="Leave blank if webhooks are open" />
              <button className="settings-toggle-eye" onClick={() => setShowSecret(v => !v)}>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  {showSecret
                    ? <><path d="M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94"/><path d="M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19"/><line x1="1" y1="1" x2="23" y2="23"/></>
                    : <><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></>
                  }
                </svg>
              </button>
            </div>
          </div>
          <div className="settings-actions">
            <button className="btn-settings-save" onClick={handleSave}>Save &amp; Reconnect</button>
            <button className="btn-settings-test" onClick={handleTest} disabled={testing}>{testing ? 'Testing…' : 'Test Connection'}</button>
            {connStatus.msg && (
              <span className={`conn-status${connStatus.type ? ' ' + connStatus.type : ''}`}>{connStatus.msg}</span>
            )}
          </div>
        </div>

        <div className="settings-card">
          <div className="settings-card-title">Connected Integrations</div>
          <div className="settings-card-desc">Data sources feeding into your Airtable base via n8n WF1.</div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 0 }}>
            {INTEGRATIONS.map(int => (
              <div key={int.name} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '12px 0', borderBottom: '1px solid var(--border)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                  <div style={{ width: 8, height: 8, borderRadius: '50%', background: int.dot, flexShrink: 0 }} />
                  <div>
                    <div style={{ fontSize: 13 }}>{int.name}</div>
                    <div style={{ fontSize: 11, color: 'var(--text-dim)' }}>{int.sub}</div>
                  </div>
                </div>
                <span style={{ fontSize: 11, color: int.dot === 'var(--green)' ? 'var(--green)' : 'var(--accent)' }}>{int.status}</span>
              </div>
            ))}
          </div>
          <div style={{ fontSize: 11, color: 'var(--text-dim)', marginTop: 14 }}>
            Integration status reflects mock data. In live mode, status is inferred from the most recent sync timestamps in Airtable.
          </div>
        </div>

        <div className="settings-card">
          <div className="settings-card-title">About ReportFlow</div>
          <div className="settings-card-desc">Version 1.0 — Agency Reporting Dashboard</div>
          <div className="about-stack">
            <div className="about-item"><div className="about-dot" />n8n (self-hosted) — automation &amp; API layer</div>
            <div className="about-item"><div className="about-dot" />Airtable — data warehouse (6 tables)</div>
            <div className="about-item"><div className="about-dot" style={{ background: 'var(--green)' }} />OpenAI GPT-4o — AI report generation</div>
            <div className="about-item"><div className="about-dot" style={{ background: 'var(--blue)' }} />No API keys in the frontend — all credentials live server-side</div>
          </div>
          <div style={{ marginTop: 24, paddingTop: 20, borderTop: '1px solid var(--border)' }}>
            <div className="settings-label" style={{ marginBottom: 12 }}>Demo Mode</div>
            <button className="btn-settings-reset" onClick={handleReset}>Reset to Demo Mode</button>
            <div style={{ fontSize: 11, color: 'var(--text-dim)', marginTop: 8 }}>Clears saved n8n URL and secret. The dashboard returns to offline mock data.</div>
          </div>
        </div>

      </div>
    </div>
  )
}
