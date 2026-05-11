<script setup>
import { useI18n } from '../composables/useI18n.js'

defineProps({
  updatedAt: { type: String, default: null },
})

const { locale, t } = useI18n()
</script>

<template>
  <header class="header">
    <div class="header-brand">
      <p class="header-org">{{ t('org') }}</p>
      <h1 class="header-title">
        {{ t('title') }}
        <abbr class="header-abbr" :title="t('title')">{{ t('abbr') }}</abbr>
      </h1>
    </div>

    <div class="header-right">
      <div v-if="updatedAt" class="header-meta">
        <span class="header-meta-label">{{ t('updated') }}</span>
        <span class="header-meta-date">{{ updatedAt }}</span>
      </div>

      <div class="lang-switcher" role="group" aria-label="Language">
        <button
          v-for="lang in ['es', 'en', 'fr']"
          :key="lang"
          class="lang-btn"
          :class="{ 'lang-btn--active': locale === lang }"
          @click="locale = lang"
        >
          {{ lang.toUpperCase() }}
        </button>
      </div>
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
  padding: 0 16px;
  flex-shrink: 0;
  z-index: 20;
  position: relative;
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
  font-size: 16px;
  font-weight: 700;
  color: var(--c-accent);
  letter-spacing: -0.01em;
  display: flex;
  align-items: baseline;
  gap: 5px;
  flex-wrap: wrap;
}

.header-abbr {
  font-size: 11px;
  font-weight: 500;
  color: var(--c-muted);
  text-decoration: none;
  cursor: default;
  letter-spacing: 0.02em;
}

/* ── Lado derecho ── */
.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-shrink: 0;
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

/* ── Selector de idioma ── */
.lang-switcher {
  display: flex;
  gap: 2px;
  border: 1px solid var(--c-border);
  border-radius: 4px;
  overflow: hidden;
  flex-shrink: 0;
}

.lang-btn {
  padding: 3px 8px;
  font-size: 10.5px;
  font-weight: 600;
  letter-spacing: 0.04em;
  border: none;
  background: transparent;
  color: var(--c-muted);
  cursor: pointer;
  transition: background 0.1s, color 0.1s;
}

.lang-btn:not(:last-child) {
  border-right: 1px solid var(--c-border);
}

.lang-btn--active {
  background: var(--c-accent);
  color: #fff;
}

.lang-btn:hover:not(.lang-btn--active) {
  background: var(--c-accent-dim);
  color: var(--c-accent);
}

@media (min-width: 600px) {
  .header-meta { display: flex; }
}
</style>
