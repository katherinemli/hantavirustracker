<script setup>
import { ref, computed, onMounted } from 'vue'
import TheHeader    from './components/TheHeader.vue'
import StatBar      from './components/StatBar.vue'
import MapContainer from './components/MapContainer.vue'
import LeftSidebar  from './components/LeftSidebar.vue'
import RightSidebar from './components/RightSidebar.vue'
import { useI18n }  from './composables/useI18n.js'

const { t } = useI18n()

/* ── Fetch ── */
const data    = ref(null)
const error   = ref(null)
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await fetch('/data/cases.json')
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    data.value = await res.json()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
})

/* ── Datos derivados ── */
const cases     = computed(() => data.value?.cases     ?? [])
const shipRoute = computed(() => data.value?.ship_route ?? [])
const newsFeed  = computed(() => data.value?.news_feed  ?? [])

const summary = computed(() => ({
  confirmed:       cases.value.filter(c => c.status === 'Confirmed').length,
  monitoring:      cases.value.filter(c => c.status === 'Monitoring').length,
  countries_alert: new Set(cases.value.map(c => c.country)).size,
}))

/* ── Estado de filtros (gestionado aquí para que el mapa y la lista compartan estado) ── */
const statusFilter = ref('all')
const searchQuery  = ref('')

const filteredCases = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()
  return cases.value
    .filter(c => statusFilter.value === 'all' || c.status === statusFilter.value)
    .filter(c => !q || c.country.toLowerCase().includes(q) || (c.region ?? '').toLowerCase().includes(q))
})
</script>

<template>
  <div class="app">
    <TheHeader :updated-at="data?.updated_at" />

    <div v-if="loading" class="state">{{ t('loading') }}</div>

    <div v-else-if="error" class="state state--error">
      {{ t('error_prefix') }} {{ error }}
    </div>

    <template v-else>
      <!--
        MOBILE:  stats → map → left (filtros+lista) → right (feed)
        DESKTOP: [stats full-width] / [left | map | right]
      -->
      <main class="layout">
        <StatBar
          class="area-stats"
          :summary="summary"
        />

        <MapContainer
          class="area-map"
          :cases="filteredCases"
          :ship-route="shipRoute"
        />

        <LeftSidebar
          class="area-left"
          :cases="cases"
          :filtered="filteredCases"
          :status-filter="statusFilter"
          :search-query="searchQuery"
          @update:status-filter="statusFilter = $event"
          @update:search-query="searchQuery = $event"
        />

        <RightSidebar
          class="area-right"
          :news-feed="newsFeed"
        />
      </main>

      <footer class="footer">
        <span>{{ data?.source }}</span>
        <span class="footer-sep">·</span>
        <span class="footer-disclaimer">{{ t('disclaimer') }}</span>
      </footer>
    </template>
  </div>
</template>

<style scoped>
/* ── Shell ── */
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* ── Estados ── */
.state {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px 20px;
  color: var(--c-muted);
  font-size: 14px;
}

.state--error { color: var(--c-confirmed); }

/* ────────────────────────────────────
   MOBILE — columna única, scroll libre
──────────────────────────────────── */
.layout {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr;
  grid-template-areas:
    "stats"
    "map"
    "left"
    "right";
}

.area-stats { grid-area: stats; }
.area-map   { grid-area: map;   }
.area-left  { grid-area: left;  }
.area-right { grid-area: right; }

/* ────────────────────────────────────
   DESKTOP ≥1024px — viewport fijo
   Stats: banner full-width
   Fila 2: [left | map | right]
──────────────────────────────────── */
@media (min-width: 1024px) {
  .app {
    height: 100vh;
    overflow: hidden;
  }

  .layout {
    grid-template-columns: 280px 1fr 280px;
    grid-template-rows: auto 1fr;
    grid-template-areas:
      "stats stats stats"
      "left  map   right";
    height: 100%;
    min-height: 0;
    overflow: hidden;
  }

  .area-stats {
    grid-column: 1 / -1;           /* banner full-width */
    border-bottom: 1px solid var(--c-border);
  }

  .area-left {
    border-right: 1px solid var(--c-border);
    overflow-y: auto;
    min-height: 0;
  }

  .area-map  { overflow: hidden; }

  .area-right {
    border-left: 1px solid var(--c-border);
    overflow-y: auto;
    min-height: 0;
  }
}

/* ── Footer ── */
.footer {
  border-top: 1px solid var(--c-border);
  padding: 8px 20px;
  font-size: 11px;
  color: var(--c-muted);
  letter-spacing: 0.01em;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.footer-sep { opacity: 0.4; }

.footer-disclaimer {
  font-style: italic;
  color: var(--c-accent);
  opacity: 0.7;
}
</style>
