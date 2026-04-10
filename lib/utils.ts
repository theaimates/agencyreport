export function fmt(n: number): string {
  return '$' + (n >= 1000 ? n.toLocaleString('en-US') : n)
}

export function fmtK(n: number): string {
  return n >= 1000 ? '$' + (n / 1000).toFixed(0) + 'k' : '$' + n
}

export function roasClass(r: number): string {
  if (r >= 4) return 'roas-good'
  if (r >= 2.5) return 'roas-ok'
  return 'roas-low'
}

export function platformLabel(p: string): string {
  const labels: Record<string, string> = { meta: 'Meta', google: 'Google', email: 'Email' }
  return labels[p] || p
}

const CHANNEL_COLORS: Record<string, string> = {
  'meta ads': '#d4a843',
  'google ads': '#6366f1',
  'email': '#3ecf8e',
  'email funnels': '#3ecf8e',
  'organic': '#a855f7',
  'linkedin': '#3ecf8e',
  'content/seo': '#d4a843',
  'instagram ads': '#f59e0b',
  'youtube': '#ef4444',
  'referral': '#6366f1',
  'stripe': '#a855f7',
  'direct': '#6366f1',
}

const CHANNEL_GRADIENTS: Record<string, string> = {
  'meta ads': 'linear-gradient(90deg,#d4a843,#e8c547)',
  'google ads': 'linear-gradient(90deg,#6366f1,#818cf8)',
  'email': 'linear-gradient(90deg,#3ecf8e,#6ee7a8)',
  'email funnels': 'linear-gradient(90deg,#3ecf8e,#6ee7a8)',
  'organic': 'linear-gradient(90deg,#a855f7,#c084fc)',
  'linkedin': 'linear-gradient(90deg,#3ecf8e,#6ee7a8)',
  'content/seo': 'linear-gradient(90deg,#d4a843,#e8c547)',
  'instagram ads': 'linear-gradient(90deg,#f59e0b,#fbbf24)',
  'youtube': 'linear-gradient(90deg,#ef4444,#f87171)',
  'referral': 'linear-gradient(90deg,#6366f1,#818cf8)',
}

export function channelColor(name: string): string {
  return CHANNEL_COLORS[name.toLowerCase()] || '#7a7570'
}

export function channelGradient(name: string): string {
  return CHANNEL_GRADIENTS[name.toLowerCase()] || 'linear-gradient(90deg,#7a7570,#a0a0a0)'
}
