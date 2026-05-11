<script setup>
import { useI18n } from '../composables/useI18n.js'

defineProps({
  summary: {
    type: Object,
    default: () => ({ confirmed: '—', monitoring: '—', countries_alert: '—' }),
  },
})

const { t } = useI18n()
</script>

<template>
  <section class="statbar">
    <div class="stat">
      <span class="stat-value stat-value--confirmed">{{ summary.confirmed }}</span>
      <span class="stat-label">{{ t('confirmed') }}</span>
    </div>

    <div class="stat-divider" />

    <div class="stat">
      <span class="stat-value stat-value--monitoring">{{ summary.monitoring }}</span>
      <span class="stat-label">{{ t('monitoring') }}</span>
    </div>

    <div class="stat-divider" />

    <div class="stat">
      <span class="stat-value">{{ summary.countries_alert }}</span>
      <span class="stat-label">{{ t('countries') }}</span>
    </div>
  </section>
</template>

<style scoped>
.statbar {
  display: grid;
  grid-template-columns: 1fr auto 1fr auto 1fr;
  align-items: center;
  background: var(--c-surface);
  padding: 20px 8px;
}

.stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  padding: 10px 4px;
}

/* Mobile: números gigantes */
.stat-value {
  font-size: 42px;
  font-weight: 700;
  color: var(--c-accent);
  line-height: 1;
  letter-spacing: -0.03em;
  font-variant-numeric: tabular-nums;
}

.stat-value--confirmed  { color: var(--c-confirmed); }
.stat-value--monitoring { color: var(--c-monitoring); }

.stat-label {
  font-size: 10px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--c-muted);
  text-align: center;
  line-height: 1.3;
}

.stat-divider {
  width: 1px;
  height: 44px;
  background: var(--c-border);
  flex-shrink: 0;
}

@media (min-width: 1024px) {
  .statbar { padding: 12px 8px; }
  .stat-value { font-size: 28px; }
  .stat-divider { height: 30px; }
}
</style>
