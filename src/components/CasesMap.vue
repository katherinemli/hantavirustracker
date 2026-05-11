<script setup>
import { ref, watch, onMounted, onUnmounted, nextTick } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const props = defineProps({
  cases: { type: Array, default: () => [] },
})

/* Coordenadas aproximadas por región administrativa de Chile */
const REGION_COORDS = {
  'Arica y Parinacota':           [-18.48, -70.33],
  'Tarapacá':                     [-20.21, -69.76],
  'Antofagasta':                  [-23.65, -70.40],
  'Atacama':                      [-27.37, -70.33],
  'Coquimbo':                     [-29.95, -71.34],
  'Valparaíso':                   [-33.04, -71.62],
  'Metropolitana de Santiago':    [-33.46, -70.65],
  "O'Higgins":                    [-34.57, -70.74],
  'Maule':                        [-35.43, -71.67],
  'Ñuble':                        [-36.72, -72.10],
  'Biobío':                       [-37.47, -72.35],
  'La Araucanía':                 [-38.73, -72.59],
  'Los Ríos':                     [-40.29, -72.14],
  'Los Lagos':                    [-41.47, -72.94],
  'Aysén':                        [-45.57, -72.07],
  'Magallanes':                   [-53.16, -70.91],
}

const DESENLACE_COLOR = {
  recuperado:   '#276749',
  hospitalizado: '#1F4B8E',
  fallecido:    '#742A2A',
}

const mapEl = ref(null)
let map = null
let markersLayer = null
let resizeObserver = null

function renderMarkers() {
  if (!markersLayer) return
  markersLayer.clearLayers()
  props.cases.forEach(c => {
    const coords = REGION_COORDS[c.region]
    if (!coords) return
    const color = DESENLACE_COLOR[c.desenlace] ?? '#718096'
    const sexLabel = c.sexo === 'M' ? 'Hombre' : 'Mujer'
    L.circleMarker(coords, {
      radius: 11,
      fillColor: color,
      color: '#fff',
      weight: 2.5,
      fillOpacity: 0.88,
    })
      .addTo(markersLayer)
      .bindPopup(
        `<div class="lf-popup">
          <strong>${c.region}</strong>
          <span class="lf-popup-sub">${c.comuna}</span>
          <div class="lf-popup-row"><b>Confirmado:</b> ${c.fecha_confirmacion}</div>
          <div class="lf-popup-row"><b>Paciente:</b> ${sexLabel}, ${c.edad} años</div>
          <div class="lf-popup-row"><b>Exposición:</b> ${c.exposicion}</div>
          <span class="lf-badge" style="background:${color}18;color:${color};border:1px solid ${color}40">
            ${c.desenlace}
          </span>
          <div class="lf-popup-source">${c.fuente}</div>
        </div>`,
        { maxWidth: 240 },
      )
  })
}

onMounted(async () => {
  await nextTick()
  map = L.map(mapEl.value, {
    center: [-37, -71],
    zoom: 5,
    zoomControl: true,
    attributionControl: true,
  })

  L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    attribution:
      '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors © <a href="https://carto.com/attributions">CARTO</a>',
    subdomains: 'abcd',
    maxZoom: 18,
  }).addTo(map)

  markersLayer = L.layerGroup().addTo(map)
  renderMarkers()

  resizeObserver = new ResizeObserver(() => map?.invalidateSize())
  resizeObserver.observe(mapEl.value)
})

onUnmounted(() => {
  resizeObserver?.disconnect()
  map?.remove()
})

watch(() => props.cases, renderMarkers, { deep: true })
</script>

<template>
  <div class="map-wrap">
    <div ref="mapEl" class="map-el" />
    <div class="map-legend">
      <div class="legend-row">
        <span class="legend-dot" style="background:#276749" />
        <span>recuperado</span>
      </div>
      <div class="legend-row">
        <span class="legend-dot" style="background:#1F4B8E" />
        <span>hospitalizado</span>
      </div>
      <div class="legend-row">
        <span class="legend-dot" style="background:#742A2A" />
        <span>fallecido</span>
      </div>
    </div>
  </div>
</template>

<style>
/* Estilos del popup de Leaflet — no pueden ser scoped */
.lf-popup {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
  font-size: 13px;
  line-height: 1.5;
  min-width: 190px;
}
.lf-popup strong { font-size: 14px; display: block; }
.lf-popup-sub {
  display: block;
  font-size: 11px;
  color: #718096;
  margin-bottom: 6px;
}
.lf-popup-row { margin-bottom: 2px; }
.lf-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 3px;
  font-size: 11px;
  font-weight: 600;
  margin-top: 6px;
  margin-bottom: 6px;
}
.lf-popup-source {
  font-size: 10px;
  color: #718096;
}
</style>

<style scoped>
.map-wrap {
  position: relative;
  height: 45vh;
  min-height: 260px;
  background: #edecea;
  border-top: 1px solid var(--c-border);
  border-bottom: 1px solid var(--c-border);
}

.map-el {
  width: 100%;
  height: 100%;
}

.map-legend {
  position: absolute;
  bottom: 28px;
  right: 8px;
  z-index: 500;
  background: rgba(255, 255, 255, 0.93);
  border: 1px solid var(--c-border);
  border-radius: 4px;
  padding: 8px 11px;
  font-size: 11px;
  display: flex;
  flex-direction: column;
  gap: 5px;
  pointer-events: none;
  backdrop-filter: blur(4px);
}

.legend-row {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--c-text);
}

.legend-dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  flex-shrink: 0;
  border: 1.5px solid rgba(255,255,255,0.6);
}

@media (min-width: 1024px) {
  .map-wrap {
    height: 100%;
    min-height: 0;
    border-top: none;
    border-bottom: none;
  }
}
</style>
