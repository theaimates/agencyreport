import { NextRequest, NextResponse } from 'next/server'

const N8N_BASE_URL = (process.env.N8N_BASE_URL || 'http://localhost:5678').replace(/\/$/, '')
const N8N_WEBHOOK_SECRET = process.env.N8N_WEBHOOK_SECRET || ''

export async function POST(req: NextRequest) {
  try {
    const body = await req.json()
    const { clientId, dateRange } = body

    if (!clientId) {
      return NextResponse.json({ error: 'clientId required' }, { status: 400 })
    }

    const headers: Record<string, string> = { 'Content-Type': 'application/json' }
    if (N8N_WEBHOOK_SECRET) headers['X-Webhook-Secret'] = N8N_WEBHOOK_SECRET

    const upstream = await fetch(`${N8N_BASE_URL}/webhook/reportflow/dashboard`, {
      method: 'POST',
      headers,
      body: JSON.stringify({ clientId, dateRange: dateRange || 'this_month' }),
    })

    if (!upstream.ok) {
      return NextResponse.json({ error: 'Upstream error' }, { status: upstream.status })
    }

    const data = await upstream.json()
    return NextResponse.json(data)
  } catch (err) {
    // n8n unreachable — frontend falls back to mock data
    return NextResponse.json({ error: 'n8n unreachable' }, { status: 503 })
  }
}
