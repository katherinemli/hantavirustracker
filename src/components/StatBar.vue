<script setup>
defineProps({
  summary: {
    type: Object,
    default: () => ({ confirmed: '—', fatalities: '—', active_regions: '—', fatality_rate: null }),
  },
})
</script>

<template>
  <section class="statbar">
    <div class="stat">
      <span class="stat-value">{{ summary.confirmed }}</span>
      <span class="stat-label">Casos confirmados</span>
    </div>
    <div class="stat-divider" />
    <div class="stat">
      <span class="stat-value">{{ summary.fatalities }}</span>
      <span class="stat-label">Fallecidos</span>
    </div>
    <div class="stat-divider" />
    <div class="stat">
      <span class="stat-value">{{ summary.active_regions }}</span>
      <span class="stat-label">Regiones activas</span>
    </div>
  </section>
</template>

<style scoped>
.statbar {
  display: grid;
  grid-template-columns: 1fr auto 1fr auto 1fr;
  align-items: center;
  background: var(--c-surface);
  border-bottom: 1px solid var(--c-border);
  padding: 20px 8px;
}

.stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  padding: 10px 4px;
}

/* Mobile: números gigantes (requisito crítico) */
.stat-value {
  font-size: 42px;
  font-weight: 700;
  color: var(--c-accent);
  line-height: 1;
  letter-spacing: -0.03em;
  font-variant-numeric: tabular-nums;
}

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

/* Desktop: columna izquierda de 300px — reducimos la fuente */
@media (min-width: 1024px) {
  .statbar {
    padding: 14px 8px;
  }

  .stat-value {
    font-size: 30px;
  }

  .stat-divider {
    height: 32px;
  }
}
</style>
