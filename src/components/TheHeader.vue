<script setup>
defineProps({
  updatedAt: { type: String, default: null },
})
</script>

<template>
  <header class="header">
    <div class="header-brand">
      <p class="header-org">MINSAL · ISP Chile · Sección Zoonosis</p>
      <h1 class="header-title">Monitor Hantavirus</h1>
    </div>
    <div v-if="updatedAt" class="header-meta">
      <span class="header-meta-label">Actualizado</span>
      <span class="header-meta-date">{{ updatedAt }}</span>
    </div>
  </header>
</template>

<style scoped>
.header {
  height: var(--header-h);
  background: var(--c-surface);
  border-bottom: 1px solid var(--c-border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  flex-shrink: 0;
  position: relative;
  z-index: 10;
}

.header-org {
  font-size: 10px;
  font-weight: 500;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--c-muted);
  margin-bottom: 2px;
}

.header-title {
  font-size: 17px;
  font-weight: 700;
  color: var(--c-accent);
  letter-spacing: -0.01em;
}

.header-meta {
  display: none;
  flex-direction: column;
  align-items: flex-end;
  gap: 1px;
}

.header-meta-label {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--c-muted);
}

.header-meta-date {
  font-family: var(--mono);
  font-size: 12px;
  color: var(--c-text);
}

@media (min-width: 600px) {
  .header-meta { display: flex; }
}
</style>
