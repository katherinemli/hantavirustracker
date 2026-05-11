<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  cases: { type: Array, default: () => [] },
})

const FILTERS = [
  { value: 'todos',         label: 'Todos' },
  { value: 'recuperado',    label: 'Recuperado' },
  { value: 'hospitalizado', label: 'Hospitalizado' },
  { value: 'fallecido',     label: 'Fallecido' },
]

const active = ref('todos')

const displayed = computed(() =>
  active.value === 'todos'
    ? props.cases
    : props.cases.filter(c => c.desenlace === active.value),
)
</script>

<template>
  <section class="cases-list">
    <div class="list-header">
      <h2 class="list-title">Registro de casos</h2>
      <div class="filter-tabs" role="group" aria-label="Filtrar por desenlace">
        <button
          v-for="f in FILTERS"
          :key="f.value"
          class="filter-btn"
          :class="{ 'filter-btn--active': active === f.value }"
          @click="active = f.value"
        >
          {{ f.label }}
        </button>
      </div>
    </div>

    <p v-if="displayed.length === 0" class="empty">Sin casos para el filtro seleccionado.</p>

    <div v-else class="table-wrap">
      <table class="table">
        <thead>
          <tr>
            <th>Región / Comuna</th>
            <th>Confirmación</th>
            <th class="hide-xs">Exposición</th>
            <th>Estado</th>
            <th class="hide-sm">Fuente</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="c in displayed" :key="c.id">
            <td>
              <span class="region-name">{{ c.region }}</span>
              <span class="comuna-name">{{ c.comuna }}</span>
            </td>
            <td class="mono">{{ c.fecha_confirmacion }}</td>
            <td class="exposicion hide-xs">{{ c.exposicion }}</td>
            <td>
              <span class="badge" :class="`badge--${c.desenlace}`">{{ c.desenlace }}</span>
            </td>
            <td class="fuente hide-sm">{{ c.fuente }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<style scoped>
.cases-list {
  background: var(--c-surface);
  border-top: 1px solid var(--c-border);
}

/* Sticky header con filtros */
.list-header {
  position: sticky;
  top: 0;
  z-index: 5;
  background: var(--c-surface);
  border-bottom: 1px solid var(--c-border);
  padding: 12px 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.list-title {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--c-muted);
}

.filter-tabs {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}

.filter-btn {
  padding: 4px 10px;
  font-size: 12px;
  border: 1px solid var(--c-border);
  border-radius: 3px;
  background: var(--c-bg);
  color: var(--c-muted);
  cursor: pointer;
  transition: background 0.1s, color 0.1s, border-color 0.1s;
}

.filter-btn--active {
  background: var(--c-accent);
  border-color: var(--c-accent);
  color: #fff;
}

.filter-btn:hover:not(.filter-btn--active) {
  background: var(--c-accent-dim);
  border-color: var(--c-accent);
  color: var(--c-accent);
}

.empty {
  padding: 32px 16px;
  text-align: center;
  color: var(--c-muted);
  font-size: 13px;
}

/* Tabla con scroll horizontal en mobile */
.table-wrap {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

.table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12.5px;
  white-space: nowrap;
}

.table th {
  padding: 8px 14px;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--c-muted);
  text-align: left;
  background: var(--c-bg);
  border-bottom: 1px solid var(--c-border);
}

.table td {
  padding: 10px 14px;
  border-bottom: 1px solid var(--c-border);
  vertical-align: top;
}

.table tr:last-child td {
  border-bottom: none;
}

.region-name {
  display: block;
  font-weight: 500;
  white-space: normal;
}

.comuna-name {
  display: block;
  font-size: 11px;
  color: var(--c-muted);
}

.mono { font-family: var(--mono); font-size: 12px; }

.exposicion {
  white-space: normal;
  max-width: 200px;
  color: var(--c-muted);
}

.fuente { font-size: 11px; color: var(--c-muted); }

/* Columnas progresivas según ancho disponible */
.hide-xs { display: none; }
.hide-sm { display: none; }

@media (min-width: 520px) { .hide-xs { display: table-cell; } }
@media (min-width: 768px) { .hide-sm { display: table-cell; } }

/* ── Badges de desenlace ── */
.badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 3px;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.02em;
  white-space: nowrap;
}

.badge--recuperado {
  background: var(--c-recuperado-bg);
  color: var(--c-recuperado);
  border: 1px solid var(--c-recuperado-bd);
}

.badge--hospitalizado {
  background: var(--c-hospitalizado-bg);
  color: var(--c-hospitalizado);
  border: 1px solid var(--c-hospitalizado-bd);
}

.badge--fallecido {
  background: var(--c-fallecido-bg);
  color: var(--c-fallecido);
  border: 1px solid var(--c-fallecido-bd);
}

@media (min-width: 1024px) {
  .list-header {
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
  }
}
</style>
