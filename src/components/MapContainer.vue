<script setup>
import { ref, watch, onMounted, onUnmounted, nextTick } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { useI18n } from '../composables/useI18n.js'

const props = defineProps({
  cases:     { type: Array, default: () => [] },
  shipRoute: { type: Array, default: () => [] },
})

const { t, locale } = useI18n()

const STATUS_STYLE = {
  Confirmed:  { fillColor: '#C05621', radius: 11 },
  Monitoring: { fillColor: '#2B6CB0', radius:  8 },
}

const mapEl = ref(null)
let map          = null
let markersLayer = null
let routeLayer   = null
let resizeObs    = null

/* ── Marcadores de casos ── */
function renderMarkers() {
  if (!markersLayer) return
  markersLayer.clearLayers()
  props.cases.forEach(c => {
    if (c.lat == null || c.lng == null) return
    const style      = STATUS_STYLE[c.status] ?? { fillColor: '#718096', radius: 8 }
    const statusLabel = t(`status_${c.status.toLowerCase()}`)
    const color       = style.fillColor

    L.circleMarker([c.lat, c.lng], {
      radius:      style.radius,
      fillColor:   color,
      color:       '#fff',
      weight:      2,
      fillOpacity: 0.85,
    })
    .addTo(markersLayer)
    .bindPopup(
      `<div class="lf-popup">
        <strong>${c.country}</strong>
        <span class="lf-sub">${c.region ?? ''}</span>
        <div class="lf-row"><span class="lf-field">Pathogen:</span> ${c.pathogen}</div>
        <div class="lf-row"><span class="lf-field">Date:</span> ${c.date}</div>
        ${c.notes ? `<div class="lf-notes">${c.notes}</div>` : ''}
        <div class="lf-foot">
          <span class="lf-badge"
            style="background:${color}18;color:${color};border:1px solid ${color}44">
            ${statusLabel}
          </span>
          ${c.source_url
            ? `<a class="lf-link" href="${c.source_url}" target="_blank" rel="noopener noreferrer">
                ${c.source_agency ?? 'Source'} ↗
               </a>`
            : ''}
        </div>
      </div>`,
      { maxWidth: 260 },
    )
  })
}

/* ── Ruta del barco ── */
function renderRoute() {
  if (!map || !props.shipRoute.length) return
  routeLayer?.remove()
  routeLayer = L.polyline(props.shipRoute, {
    color:     '#718096',
    weight:    1.5,
    opacity:   0.55,
    dashArray: '6, 5',
  })
  .addTo(map)
  .bindTooltip(t('ship_route'), { sticky: true, className: 'lf-ship-tip' })
}

onMounted(async () => {
  await nextTick()
  map = L.map(mapEl.value, {
    center:           [15, -30],   /* Vista mundial centrada en el Atlántico */
    zoom:             3,
    zoomControl:      true,
    attributionControl: true,
  })

  L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    attribution:
      '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> ' +
      '© <a href="https://carto.com/attributions">CARTO</a>',
    subdomains: 'abcd',
    maxZoom:    18,
  }).addTo(map)

  markersLayer = L.layerGroup().addTo(map)
  renderRoute()
  renderMarkers()

  resizeObs = new ResizeObserver(() => map?.invalidateSize())
  resizeObs.observe(mapEl.value)
})

onUnmounted(() => {
  resizeObs?.disconnect()
  map?.remove()
})

watch(() => props.cases,     renderMarkers, { deep: true })
watch(() => props.shipRoute, renderRoute)
watch(locale, () => { renderRoute(); renderMarkers() })
</script>

<template>
  <div class="map-wrap">
    <div ref="mapEl" class="map-el" />

    <div class="map-legend">
      <p class="legend-title">{{ t('cases_label') }}</p>
      <div class="legend-row">
        <span class="legend-dot" style="background:#C05621" />
        <span>{{ t('status_confirmed') }}</span>
      </div>
      <div class="legend-row">
        <span class="legend-dot" style="background:#2B6CB0" />
        <span>{{ t('status_monitoring') }}</span>
      </div>
      <hr class="legend-rule" />
      <div class="legend-row">
        <span class="legend-dash-line" />
        <span>MV Hondius</span>
      </div>
    </div>
  </div>
</template>

<!-- Popup styles — no pueden ser scoped -->
<style>
.lf-popup {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  font-size: 13px;
  line-height: 1.5;
  min-width: 200px;
}
.lf-popup strong { font-size: 14px; display: block; margin-bottom: 1px; }
.lf-sub  { display: block; font-size: 11px; color: #718096; margin-bottom: 8px; }
.lf-row  { margin-bottom: 2px; }
.lf-field { color: #718096; font-size: 11px; }
.lf-notes {
  font-size: 12px;
  color: #4a5568;
  background: #f7fafc;
  border-left: 2px solid #e2e8f0;
  padding: 4px 8px;
  margin: 8px 0;
  border-radius: 2px;
}
.lf-foot  { display: flex; align-items: center; gap: 8px; margin-top: 8px; flex-wrap: wrap; }
.lf-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 3px;
  font-size: 11px;
  font-weight: 600;
}
.lf-link {
  font-size: 11px;
  color: #1F4B8E;
  text-decoration: none;
}
.lf-link:hover { text-decoration: underline; }

/* Tooltip de la ruta */
.lf-ship-tip {
  font-family: -apple-system, sans-serif;
  font-size: 11px;
  background: rgba(255,255,255,0.92);
  border: 1px solid #e2e8f0;
  color: #4a5568;
  border-radius: 3px;
  box-shadow: none;
}
.lf-ship-tip::before { display: none; }
</style>

<style scoped>
/* ── Contenedor del mapa ── */
.map-wrap {
  position: relative;
  height: 50vh;
  min-height: 280px;
  background: #edecea;
  border-top: 1px solid var(--c-border);
  border-bottom: 1px solid var(--c-border);
}

.map-el { width: 100%; height: 100%; }

/* ── Leyenda ── */
.map-legend {
  position: absolute;
  bottom: 28px;
  right: 8px;
  z-index: 500;
  background: rgba(255, 255, 255, 0.93);
  border: 1px solid var(--c-border);
  border-radius: 4px;
  padding: 9px 12px;
  font-size: 11px;
  display: flex;
  flex-direction: column;
  gap: 5px;
  pointer-events: none;
  backdrop-filter: blur(4px);
}

.legend-title {
  font-size: 9.5px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--c-accent);
  padding-bottom: 5px;
  border-bottom: 1px solid var(--c-border);
}

.legend-rule {
  border: none;
  border-top: 1px solid var(--c-border);
  margin: 2px 0;
}

.legend-row {
  display: flex;
  align-items: center;
  gap: 7px;
  color: var(--c-text);
}

.legend-dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  border: 1.5px solid rgba(255,255,255,0.7);
  flex-shrink: 0;
}

/* Línea discontinua para la ruta del barco */
.legend-dash-line {
  width: 20px;
  height: 0;
  border-top: 2px dashed #718096;
  flex-shrink: 0;
  opacity: 0.7;
}

/* Desktop: mapa llena el área de grid */
@media (min-width: 1024px) {
  .map-wrap {
    height: 100%;
    min-height: 0;
    border-top: none;
    border-bottom: none;
  }
}
</style>
