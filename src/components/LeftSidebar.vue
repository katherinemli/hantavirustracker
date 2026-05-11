<script setup>
import { computed } from 'vue'
import { useI18n } from '../composables/useI18n.js'

const props = defineProps({
  cases:        { type: Array,  default: () => [] },
  filtered:     { type: Array,  default: () => [] },
  statusFilter: { type: String, default: 'all' },
  searchQuery:  { type: String, default: '' },
})

const emit = defineEmits(['update:statusFilter', 'update:searchQuery'])

const { t } = useI18n()

const FILTERS = [
  { value: 'all',        labelKey: 'all' },
  { value: 'Confirmed',  labelKey: 'filter_confirmed' },
  { value: 'Monitoring', labelKey: 'filter_monitoring' },
]

const confirmedCount  = computed(() => props.cases.filter(c => c.status === 'Confirmed').length)
const monitoringCount = computed(() => props.cases.filter(c => c.status === 'Monitoring').length)

const AGENCY_COLORS = {
  WHO:    { bg: '#EBF5FF', text: '#005EB8' },
  CDC:    { bg: '#EBF0FF', text: '#003087' },
  ECDC:   { bg: '#EBF4FF', text: '#004B87' },
  UKHSA:  { bg: '#EBF0FF', text: '#012169' },
  PAHO:   { bg: '#F0FFF4', text: '#00853F' },
  ProMED: { bg: '#F7FAFC', text: '#4A5568' },
}

function agencyStyle(agency) {
  const s = AGENCY_COLORS[agency] ?? { bg: '#F7FAFC', text: '#4A5568' }
  return `background:${s.bg};color:${s.text}`
}
</script>

<template>
  <aside class="sidebar">
    <!-- ── Filtros ── -->
    <div class="section-head">
      <h2 class="section-title">{{ t('filters') }}</h2>
    </div>

    <div class="filter-block">
      <div class="filter-tabs" role="group">
        <button
          v-for="f in FILTERS"
          :key="f.value"
          class="filter-btn"
          :class="{ 'filter-btn--active': statusFilter === f.value }"
          @click="emit('update:statusFilter', f.value)"
        >
          {{ t(f.labelKey) }}
          <span class="filter-count">
            {{
              f.value === 'all'        ? cases.length :
              f.value === 'Confirmed'  ? confirmedCount :
              monitoringCount
            }}
          </span>
        </button>
      </div>

      <input
        class="search-input"
        type="search"
        :placeholder="t('search_placeholder')"
        :value="searchQuery"
        @input="emit('update:searchQuery', $event.target.value)"
      />
    </div>

    <!-- ── Lista de casos ── -->
    <div class="section-head section-head--list">
      <h2 class="section-title">{{ t('case_register') }}</h2>
      <span class="count-chip">{{ filtered.length }}</span>
    </div>

    <p v-if="filtered.length === 0" class="empty">{{ t('no_cases') }}</p>

    <ul v-else class="case-list">
      <li
        v-for="c in filtered"
        :key="c.id"
        class="case-item"
      >
        <div class="case-main">
          <span class="case-country">{{ c.country }}</span>
          <span class="case-region">{{ c.region }}</span>
        </div>
        <div class="case-meta">
          <time class="case-date">{{ c.date }}</time>
          <span
            class="badge"
            :class="c.status === 'Confirmed' ? 'badge--confirmed' : 'badge--monitoring'"
          >
            {{ t(`status_${c.status.toLowerCase()}`) }}
          </span>
        </div>
        <div v-if="c.source_url" class="case-source">
          <span class="agency-tag" :style="agencyStyle(c.source_agency)">
            {{ c.source_agency }}
          </span>
          <a
            :href="c.source_url"
            target="_blank"
            rel="noopener noreferrer"
            class="source-link"
          >{{ t('view_source') }}</a>
        </div>
      </li>
    </ul>
  </aside>
</template>

<style scoped>
.sidebar {
  background: var(--c-surface);
  border-top: 1px solid var(--c-border);
  display: flex;
  flex-direction: column;
}

/* ── Cabeceras de sección ── */
.section-head {
  position: sticky;
  top: 0;
  z-index: 5;
  background: var(--c-surface);
  border-bottom: 1px solid var(--c-border);
  padding: 10px 14px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.section-head--list { top: 0; }

.section-title {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--c-muted);
}

.count-chip {
  font-size: 10px;
  font-weight: 600;
  background: var(--c-accent-dim);
  color: var(--c-accent);
  padding: 1px 6px;
  border-radius: 10px;
}

/* ── Filtros ── */
.filter-block {
  padding: 10px 14px 12px;
  border-bottom: 1px solid var(--c-border);
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filter-tabs {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}

.filter-btn {
  display: inline-flex;
  align-items: center;
  gap: 5px;
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

.filter-btn--active .filter-count { background: rgba(255,255,255,0.25); color: #fff; }

.filter-btn:hover:not(.filter-btn--active) {
  background: var(--c-accent-dim);
  border-color: var(--c-accent);
  color: var(--c-accent);
}

.filter-count {
  font-size: 10px;
  font-weight: 700;
  background: var(--c-border);
  color: var(--c-muted);
  padding: 0 5px;
  border-radius: 8px;
}

.search-input {
  width: 100%;
  padding: 6px 10px;
  font-size: 12.5px;
  border: 1px solid var(--c-border);
  border-radius: 3px;
  background: var(--c-bg);
  color: var(--c-text);
  outline: none;
  transition: border-color 0.15s;
}

.search-input:focus { border-color: var(--c-accent); }

/* ── Lista ── */
.empty {
  padding: 24px 14px;
  text-align: center;
  color: var(--c-muted);
  font-size: 12.5px;
}

.case-list { list-style: none; }

.case-item {
  padding: 10px 14px;
  border-bottom: 1px solid var(--c-border);
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.case-item:last-child { border-bottom: none; }

.case-main {
  display: flex;
  align-items: baseline;
  gap: 6px;
}

.case-country {
  font-size: 13px;
  font-weight: 600;
  color: var(--c-text);
}

.case-region {
  font-size: 11px;
  color: var(--c-muted);
}

.case-meta {
  display: flex;
  align-items: center;
  gap: 8px;
}

.case-date {
  font-family: var(--mono);
  font-size: 11px;
  color: var(--c-muted);
}

.case-source {
  display: flex;
  align-items: center;
  gap: 6px;
}

.agency-tag {
  font-size: 10px;
  font-weight: 600;
  padding: 1px 6px;
  border-radius: 3px;
  letter-spacing: 0.03em;
}

.source-link {
  font-size: 11px;
  color: var(--c-accent);
  text-decoration: none;
}

.source-link:hover { text-decoration: underline; }

/* ── Badges ── */
.badge {
  display: inline-block;
  padding: 1px 7px;
  border-radius: 3px;
  font-size: 10.5px;
  font-weight: 600;
}

.badge--confirmed {
  background: var(--c-confirmed-bg);
  color: var(--c-confirmed);
  border: 1px solid var(--c-confirmed-bd);
}

.badge--monitoring {
  background: var(--c-monitoring-bg);
  color: var(--c-monitoring);
  border: 1px solid var(--c-monitoring-bd);
}

@media (min-width: 1024px) {
  .sidebar { border-top: none; }
  .section-head { position: sticky; }
}
</style>
