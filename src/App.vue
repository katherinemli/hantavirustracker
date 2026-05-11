<script setup>
import { ref, computed, onMounted } from 'vue'
import TheHeader from './components/TheHeader.vue'
import StatBar   from './components/StatBar.vue'
import CasesMap  from './components/CasesMap.vue'
import CasesList from './components/CasesList.vue'
import NewsFeed  from './components/NewsFeed.vue'

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

const summary  = computed(() => data.value?.summary  ?? {})
const cases    = computed(() => data.value?.cases    ?? [])
const newsFeed = computed(() => data.value?.news_feed ?? [])
</script>

<template>
  <div class="app">
    <TheHeader :updated-at="data?.updated_at" />

    <div v-if="loading" class="state">Cargando datos…</div>
    <div v-else-if="error" class="state state--error">
      No se pudo cargar <code>/data/cases.json</code>: {{ error }}
    </div>

    <main v-else class="layout">
      <!--
        Mobile:  stats → map → list → feed  (columna única, scroll normal)
        Desktop: [stats / list] | [map] | [feed]  (3 cols, cada col scrollable)
      -->
      <StatBar   class="area-stats" :summary="summary" />
      <CasesMap  class="area-map"   :cases="cases" />
      <CasesList class="area-list"  :cases="cases" />
      <NewsFeed  class="area-feed"  :news-feed="newsFeed" :cases="cases" />
    </main>

    <footer v-if="!loading && !error" class="footer">
      {{ data?.source }}
    </footer>
  </div>
</template>

<style scoped>
/* ────────────────────────────────────────────────
   App shell
──────────────────────────────────────────────── */
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* ── Estados de carga / error ── */
.state {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  color: var(--c-muted);
  font-size: 14px;
}

.state--error { color: var(--c-fallecido); }

/* ────────────────────────────────────────────────
   MOBILE — columna única, scroll de página normal
──────────────────────────────────────────────── */
.layout {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr;
  grid-template-areas:
    "stats"
    "map"
    "list"
    "feed";
}

.area-stats { grid-area: stats; }
.area-map   { grid-area: map;   }
.area-list  { grid-area: list;  }
.area-feed  { grid-area: feed;  }

/* ────────────────────────────────────────────────
   DESKTOP ≥1024px — 3 columnas, viewport fijo
   Izquierda: stats (fijo) + list (scroll)
   Centro:    mapa (ocupa ambas filas)
   Derecha:   feed (scroll)
──────────────────────────────────────────────── */
@media (min-width: 1024px) {
  .app {
    height: 100vh;
    overflow: hidden;
  }

  .layout {
    /* dos filas: stats (auto) + list (1fr) */
    grid-template-columns: 300px 1fr 280px;
    grid-template-rows: auto 1fr;
    grid-template-areas:
      "stats map feed"
      "list  map feed";
    height: 100%;          /* fill flex parent */
    min-height: 0;
    overflow: hidden;
  }

  /* Bordes de separación de columnas */
  .area-stats {
    border-right: 1px solid var(--c-border);
    border-bottom: 1px solid var(--c-border);
  }

  .area-list {
    border-right: 1px solid var(--c-border);
    overflow-y: auto;
    min-height: 0;        /* clave para que el grid item pueda shrink */
  }

  .area-map {
    overflow: hidden;
  }

  .area-feed {
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
  letter-spacing: 0.02em;
  flex-shrink: 0;
}
</style>
