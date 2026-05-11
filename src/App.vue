<script setup>
import { ref, onMounted, computed } from 'vue'

// ── Estado de casos estáticos (public/data/cases.json) ──────────────────────
const casesData = ref(null)
const casesError = ref(null)

onMounted(async () => {
  try {
    const res = await fetch('/data/cases.json')
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    casesData.value = await res.json()
  } catch (err) {
    casesError.value = err.message
    console.error('[HantaTracker] cases.json error:', err)
  }
})

const totalConfirmed = computed(() => casesData.value?.summary?.confirmed ?? '—')
const totalFatalities = computed(() => casesData.value?.summary?.fatalities ?? '—')
const activeRegions = computed(() => casesData.value?.summary?.active_regions ?? '—')
const updatedAt = computed(() => casesData.value?.updated_at ?? null)

// ── Sonda de conexión al backend ─────────────────────────────────────────────
const probeStatus = ref('idle')
const probeResponse = ref(null)
const probeError = ref(null)

async function fetchDashboard() {
  probeStatus.value = 'loading'
  probeError.value = null
  probeResponse.value = null

  try {
    const res = await fetch('/api/dashboard')
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    const data = await res.json()
    probeResponse.value = data
    console.log('[HantaTracker] /api/dashboard →', data)
    probeStatus.value = 'ok'
  } catch (err) {
    probeError.value = err.message
    probeStatus.value = 'error'
    console.error('[HantaTracker] fetch error:', err)
  }
}
</script>

<template>
  <div class="layout">
    <header class="header">
      <div class="header-inner">
        <div class="header-brand">
          <span class="header-label">MINSAL · Sección Zoonosis</span>
          <h1 class="header-title">Monitor Hantavirus</h1>
        </div>
        <span class="header-badge">v0.1{{ updatedAt ? ` · ${updatedAt}` : '' }}</span>
      </div>
    </header>

    <main class="main">
      <section class="card probe-card">
        <h2 class="card-title">Verificación de conexión</h2>
        <p class="card-desc">
          Llama al endpoint <code>/api/dashboard</code> y vuelca la respuesta en consola.
          Abre DevTools → Console para inspeccionar el payload.
        </p>

        <button
          class="btn"
          :class="{ 'btn--loading': probeStatus === 'loading' }"
          :disabled="probeStatus === 'loading'"
          @click="fetchDashboard"
        >
          {{ probeStatus === 'loading' ? 'Consultando…' : 'GET /api/dashboard' }}
        </button>

        <div v-if="probeStatus === 'ok'" class="result result--ok">
          <span class="result-label">200 OK</span>
          <pre class="result-json">{{ JSON.stringify(probeResponse, null, 2) }}</pre>
        </div>

        <div v-else-if="probeStatus === 'error'" class="result result--error">
          <span class="result-label">Error</span>
          <code>{{ probeError }}</code>
        </div>
      </section>

      <section class="card" :class="{ 'placeholder-card': !casesData }">
        <h2 class="card-title">Resumen epidemiológico</h2>

        <div v-if="casesError" class="cases-error">
          No se pudo cargar cases.json: {{ casesError }}
        </div>

        <div v-else class="stat-grid">
          <div class="stat">
            <span class="stat-value">{{ totalConfirmed }}</span>
            <span class="stat-label">Casos confirmados</span>
          </div>
          <div class="stat">
            <span class="stat-value">{{ totalFatalities }}</span>
            <span class="stat-label">Fallecidos</span>
          </div>
          <div class="stat">
            <span class="stat-value">{{ activeRegions }}</span>
            <span class="stat-label">Regiones con casos activos</span>
          </div>
        </div>

        <table v-if="casesData?.cases?.length" class="cases-table">
          <thead>
            <tr>
              <th>Región</th>
              <th>Confirmación</th>
              <th>Exposición</th>
              <th>Desenlace</th>
              <th>Fuente</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="c in casesData.cases" :key="c.id">
              <td>{{ c.region }}</td>
              <td class="mono">{{ c.fecha_confirmacion }}</td>
              <td>{{ c.exposicion }}</td>
              <td>
                <span class="badge" :class="`badge--${c.desenlace}`">
                  {{ c.desenlace }}
                </span>
              </td>
              <td class="muted">{{ c.fuente }}</td>
            </tr>
          </tbody>
        </table>
      </section>

      <section class="card placeholder-card">
        <h2 class="card-title">Distribución geográfica</h2>
        <p class="card-desc card-desc--placeholder">
          Mapa de calor por región — datos ISP / SEREMI
        </p>
      </section>

      <section class="card placeholder-card">
        <h2 class="card-title">Boletín de novedades</h2>
        <p class="card-desc card-desc--placeholder">
          Alertas epidemiológicas y circulares MINSAL
        </p>
      </section>
    </main>

    <footer class="footer">
      Fuente: Protocolo oficial Hantavirus Chile · MINSAL · ISP
    </footer>
  </div>
</template>

<style scoped>
.layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* ── Header ── */
.header {
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  padding: 0 24px;
}

.header-inner {
  max-width: 1100px;
  margin: 0 auto;
  padding: 16px 0;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
}

.header-label {
  display: block;
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--color-text-muted);
  margin-bottom: 2px;
}

.header-title {
  font-size: 20px;
  color: var(--color-accent);
}

.header-badge {
  font-size: 11px;
  font-family: var(--font-mono);
  color: var(--color-text-muted);
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  padding: 2px 8px;
  border-radius: 3px;
}

/* ── Main grid ── */
.main {
  flex: 1;
  max-width: 1100px;
  width: 100%;
  margin: 32px auto;
  padding: 0 24px;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(480px, 1fr));
  gap: 20px;
  align-items: start;
}

/* ── Cards ── */
.card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 4px;
  padding: 24px;
}

.card-title {
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--color-text-muted);
  margin-bottom: 8px;
}

.card-desc {
  font-size: 13px;
  color: var(--color-text-muted);
  margin-bottom: 20px;
}

.card-desc--placeholder {
  margin-bottom: 0;
  font-style: italic;
}

.placeholder-card {
  opacity: 0.55;
}

/* ── Button ── */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 18px;
  font-size: 13px;
  font-family: var(--font-mono);
  font-weight: 500;
  color: var(--color-surface);
  background: var(--color-accent);
  border: none;
  border-radius: 3px;
  cursor: pointer;
  transition: opacity 0.15s;
}

.btn:hover:not(:disabled) {
  opacity: 0.88;
}

.btn:disabled,
.btn--loading {
  opacity: 0.55;
  cursor: not-allowed;
}

/* ── Result block ── */
.result {
  margin-top: 16px;
  border-radius: 3px;
  padding: 14px 16px;
  font-size: 13px;
}

.result--ok {
  background: var(--color-accent-light);
  border: 1px solid #b8d0e8;
}

.result--error {
  background: #fdf0f0;
  border: 1px solid #e8b8b8;
  color: #7a2020;
}

.result-label {
  display: block;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  margin-bottom: 8px;
  opacity: 0.7;
}

.result-json {
  font-family: var(--font-mono);
  font-size: 12px;
  white-space: pre-wrap;
  word-break: break-all;
}

/* ── Footer ── */
.footer {
  border-top: 1px solid var(--color-border);
  padding: 14px 24px;
  font-size: 11px;
  color: var(--color-text-muted);
  text-align: center;
  letter-spacing: 0.02em;
}

/* ── Stat grid ── */
.stat-grid {
  display: flex;
  gap: 32px;
  margin-bottom: 24px;
}

.stat {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.stat-value {
  font-size: 28px;
  font-weight: 600;
  letter-spacing: -0.02em;
  color: var(--color-accent);
  line-height: 1;
}

.stat-label {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-text-muted);
}

/* ── Cases table ── */
.cases-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12.5px;
}

.cases-table th {
  text-align: left;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--color-text-muted);
  border-bottom: 1px solid var(--color-border);
  padding: 6px 10px 6px 0;
}

.cases-table td {
  padding: 8px 10px 8px 0;
  border-bottom: 1px solid var(--color-bg);
  vertical-align: top;
}

.cases-table tr:last-child td {
  border-bottom: none;
}

.mono {
  font-family: var(--font-mono);
  font-size: 12px;
}

.muted {
  color: var(--color-text-muted);
}

/* ── Desenlace badges ── */
.badge {
  display: inline-block;
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.03em;
  padding: 2px 7px;
  border-radius: 2px;
}

.badge--recuperado {
  background: #eaf3ea;
  color: #2a5a2a;
  border: 1px solid #b8d8b8;
}

.badge--hospitalizado {
  background: var(--color-accent-light);
  color: var(--color-accent);
  border: 1px solid #b8d0e8;
}

.badge--fallecido {
  background: #f0eded;
  color: #5a2a2a;
  border: 1px solid #d8b8b8;
}

/* ── Error inline ── */
.cases-error {
  font-size: 12px;
  color: #7a2020;
  background: #fdf0f0;
  border: 1px solid #e8b8b8;
  padding: 10px 14px;
  border-radius: 3px;
}
</style>
