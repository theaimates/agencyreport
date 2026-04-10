'use client'
import { useRef, useEffect } from 'react'
import type { RevenuePoint } from '@/lib/types'
import { fmt, fmtK } from '@/lib/utils'

export default function RevenueChart({ data }: { data: RevenuePoint[] }) {
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const container = ref.current
    if (!container || !data.length) return

    const maxVal = Math.max(...data.map(d => d.value)) * 1.15
    const W = 700, H = 200, PL = 60, PR = 30, PT = 20, PB = 30
    const chartW = W - PL - PR
    const chartH = H - PT - PB

    const xPos = (i: number) => PL + (i / (data.length - 1)) * chartW
    const yPos = (v: number) => PT + chartH - (v / maxVal) * chartH

    const gridLines = [0, 15000, 30000, 45000, 60000]
    const gridSvg = gridLines.map(v => {
      const y = yPos(v)
      return `<line x1="${PL}" y1="${y}" x2="${W - PR}" y2="${y}" stroke="#1e2130" stroke-width="1"/>
              <text x="${PL - 8}" y="${y + 4}" text-anchor="end" fill="#504d48" font-family="DM Mono" font-size="10">${fmtK(v)}</text>`
    }).join('')

    const linePath = data.map((d, i) => `${i === 0 ? 'M' : 'L'}${xPos(i)},${yPos(d.value)}`).join(' ')
    const areaPath = linePath + ` L${xPos(data.length - 1)},${PT + chartH} L${xPos(0)},${PT + chartH} Z`

    const points = data.map((d, i) => {
      const x = xPos(i), y = yPos(d.value)
      const change = d.prev ? ((d.value - d.prev) / d.prev * 100).toFixed(1) : 0
      return `<circle cx="${x}" cy="${y}" r="4" fill="#08090c" stroke="#d4a843" stroke-width="2" class="chart-point"/>
              <circle cx="${x}" cy="${y}" r="20" fill="transparent" class="chart-dot-hover"
                data-week="${d.week}" data-value="${d.value}" data-prev="${d.prev}" data-change="${change}" data-x="${x}" data-y="${y}"/>`
    }).join('')

    const xLabels = data.map((d, i) => {
      const x = xPos(i)
      const isLast = i === data.length - 1
      return `<text x="${x}" y="${H - 8}" text-anchor="middle" fill="${isLast ? '#d4a843' : '#504d48'}" font-family="DM Mono" font-size="10" ${isLast ? 'font-weight="500"' : ''}>${d.week}</text>`
    }).join('')

    container.innerHTML = `
      <svg viewBox="0 0 ${W} ${H}" class="chart-svg">
        <defs>
          <linearGradient id="areaGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#d4a843" stop-opacity="0.2"/>
            <stop offset="100%" stop-color="#d4a843" stop-opacity="0"/>
          </linearGradient>
        </defs>
        ${gridSvg}
        <path d="${areaPath}" fill="url(#areaGrad)" opacity="0.8"/>
        <path d="${linePath}" fill="none" stroke="#d4a843" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
        ${points}
        <line class="chart-crosshair" id="crosshairV" x1="0" y1="${PT}" x2="0" y2="${PT + chartH}"/>
        <line class="chart-crosshair" id="crosshairH" x1="${PL}" y1="0" x2="${W - PR}" y2="0"/>
        ${xLabels}
      </svg>
      <div class="chart-tooltip" id="chartTooltip">
        <div class="tt-label" id="ttLabel"></div>
        <div class="tt-value" id="ttValue"></div>
        <div class="tt-change" id="ttChange"></div>
      </div>`

    container.querySelectorAll<SVGCircleElement>('.chart-dot-hover').forEach(dot => {
      dot.addEventListener('mouseenter', () => {
        const rect = container.getBoundingClientRect()
        const svgRect = container.querySelector('svg')!.getBoundingClientRect()
        const scale = svgRect.width / W
        const dotX = parseFloat(dot.dataset.x!) * scale
        const dotY = parseFloat(dot.dataset.y!) * scale
        const tt = container.querySelector<HTMLElement>('#chartTooltip')!
        const change = parseFloat(dot.dataset.change!)
        container.querySelector('#ttLabel')!.textContent = dot.dataset.week!
        container.querySelector('#ttValue')!.textContent = fmt(parseInt(dot.dataset.value!))
        const ttChange = container.querySelector('#ttChange')!
        ttChange.textContent = `${change >= 0 ? '↑' : '↓'} ${Math.abs(change)}% vs prev`
        ttChange.className = `tt-change ${change >= 0 ? 'up' : 'down'}`
        tt.style.left = Math.min(dotX - 50, rect.width - 160) + 'px'
        tt.style.top = (dotY - 80) + 'px'
        tt.classList.add('visible')
        const cv = container.querySelector<SVGLineElement>('#crosshairV')!
        const ch = container.querySelector<SVGLineElement>('#crosshairH')!
        cv.setAttribute('x1', dot.dataset.x!); cv.setAttribute('x2', dot.dataset.x!); cv.style.opacity = '1'
        ch.setAttribute('y1', dot.dataset.y!); ch.setAttribute('y2', dot.dataset.y!); ch.style.opacity = '1'
        dot.previousElementSibling?.setAttribute('r', '6')
      })
      dot.addEventListener('mouseleave', () => {
        container.querySelector('#chartTooltip')?.classList.remove('visible')
        const cv = container.querySelector<SVGLineElement>('#crosshairV')
        const ch = container.querySelector<SVGLineElement>('#crosshairH')
        if (cv) cv.style.opacity = '0'
        if (ch) ch.style.opacity = '0'
        dot.previousElementSibling?.setAttribute('r', '4')
      })
    })
  }, [data])

  return <div className="revenue-chart" ref={ref} />
}
