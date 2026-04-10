'use client'
import { useRef, useEffect } from 'react'
import type { Channel } from '@/lib/types'
import { fmt, fmtK } from '@/lib/utils'

export default function DonutChart({ channels }: { channels: Channel[] }) {
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const container = ref.current
    if (!container || !channels.length) return

    const total = channels.reduce((s, ch) => s + ch.value, 0)
    const R = 54, CX = 75, CY = 75
    const circumference = 2 * Math.PI * R

    let offset = 0
    const segments = channels.map(ch => {
      const pct = ch.value / total
      const dashLen = pct * circumference
      const dashGap = circumference - dashLen
      const seg = `<circle class="donut-segment" cx="${CX}" cy="${CY}" r="${R}"
        stroke="${ch.color}" stroke-dasharray="${dashLen} ${dashGap}"
        stroke-dashoffset="${-offset}" data-name="${ch.name}" data-value="${ch.value}" data-pct="${ch.pct}"/>`
      offset += dashLen
      return seg
    }).join('')

    container.innerHTML = `
      <div class="donut-container" id="donutContainer">
        <svg class="donut-svg" viewBox="0 0 150 150">${segments}</svg>
        <div class="donut-center">
          <span class="donut-total">${fmtK(total)}</span>
          <span class="donut-label">Total</span>
        </div>
        <div class="donut-tooltip" id="donutTooltip"></div>
      </div>
      <div class="channel-legend">
        ${channels.map(ch => `
          <div class="legend-item" data-channel="${ch.name}">
            <div class="legend-dot" style="background:${ch.color}"></div>
            <div class="legend-info">
              <span class="legend-name">${ch.name}</span>
              <span class="legend-value">${fmt(ch.value)} · ${ch.pct}%</span>
            </div>
          </div>`).join('')}
      </div>`

    container.querySelectorAll<SVGCircleElement>('.donut-segment').forEach(seg => {
      seg.addEventListener('mouseenter', () => {
        const tt = container.querySelector<HTMLElement>('#donutTooltip')!
        tt.innerHTML = `<strong>${seg.dataset.name}</strong><br>${fmt(parseInt(seg.dataset.value!))} · ${seg.dataset.pct}%`
        tt.classList.add('visible')
      })
      seg.addEventListener('mouseleave', () => {
        container.querySelector('#donutTooltip')?.classList.remove('visible')
      })
    })

    container.querySelectorAll<HTMLElement>('.legend-item').forEach(item => {
      item.addEventListener('mouseenter', () => {
        const name = item.dataset.channel
        container.querySelectorAll<SVGCircleElement>('.donut-segment').forEach(s => {
          s.style.opacity = s.dataset.name === name ? '1' : '0.25'
          if (s.dataset.name === name) s.style.strokeWidth = '34'
        })
      })
      item.addEventListener('mouseleave', () => {
        container.querySelectorAll<SVGCircleElement>('.donut-segment').forEach(s => {
          s.style.opacity = '1'
          s.style.strokeWidth = '28'
        })
      })
    })
  }, [channels])

  return <div className="channel-donut-wrap" ref={ref} />
}
