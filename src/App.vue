<script setup>
import { ref } from 'vue'

const status = ref('idle')
const response = ref(null)
const error = ref(null)

async function fetchDashboard() {
  status.value = 'loading'
  error.value = null
  response.value = null

  try {
    const res = await fetch('/api/dashboard')
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    const data = await res.json()
    response.value = data
    console.log('[HantaTracker] /api/dashboard →', data)
    status.value = 'ok'
  } catch (err) {
    error.value = err.message
    status.value = 'error'
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
        <span class="header-badge">v0.1 · dev</span>
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
          :class="{ 'btn--loading': status === 'loading' }"
          :disabled="status === 'loading'"
          @click="fetchDashboard"
        >
          {{ status === 'loading' ? 'Consultando…' : 'GET /api/dashboard' }}
        </button>

        <div v-if="status === 'ok'" class="result result--ok">
          <span class="result-label">200 OK</span>
          <pre class="result-json">{{ JSON.stringify(response, null, 2) }}</pre>
        </div>

        <div v-else-if="status === 'error'" class="result result--error">
          <span class="result-label">Error</span>
          <code>{{ error }}</code>
        </div>
      </section>

      <section class="card placeholder-card">
        <h2 class="card-title">Resumen epidemiológico</h2>
        <p class="card-desc card-desc--placeholder">
          Casos confirmados · Tasa de letalidad · Regiones activas
        </p>
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
</style>
