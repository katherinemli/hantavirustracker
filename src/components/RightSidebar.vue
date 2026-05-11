<script setup>
import { useI18n } from '../composables/useI18n.js'

defineProps({
  newsFeed: { type: Array, default: () => [] },
})

const { t } = useI18n()

const AGENCY_STYLE = {
  WHO:    { bg: '#EBF5FF', text: '#005EB8' },
  CDC:    { bg: '#EBF0FF', text: '#003087' },
  ECDC:   { bg: '#EBF4FF', text: '#004B87' },
  PAHO:   { bg: '#F0FFF4', text: '#00853F' },
  UKHSA:  { bg: '#EBF0FF', text: '#012169' },
  ProMED: { bg: '#F7FAFC', text: '#4A5568' },
}

function agencyStyle(agency) {
  const s = AGENCY_STYLE[agency] ?? { bg: '#F7FAFC', text: '#4A5568' }
  return `background:${s.bg};color:${s.text}`
}
</script>

<template>
  <aside class="feed">
    <div class="feed-head">
      <h2 class="feed-title">{{ t('recent_activity') }}</h2>
    </div>

    <p v-if="newsFeed.length === 0" class="feed-empty">{{ t('no_news') }}</p>

    <ul v-else class="feed-list">
      <li v-for="(item, i) in newsFeed" :key="i" class="feed-item">
        <div class="feed-meta">
          <time class="feed-date">{{ item.date }}</time>
          <span class="feed-agency" :style="agencyStyle(item.agency)">
            {{ item.agency }}
          </span>
        </div>

        <a
          v-if="item.url"
          :href="item.url"
          target="_blank"
          rel="noopener noreferrer"
          class="feed-title-link"
        >
          {{ item.title }}
        </a>
        <p v-else class="feed-title-text">{{ item.title }}</p>

        <div v-if="item.langs?.length" class="feed-langs">
          <span
            v-for="lang in item.langs"
            :key="lang"
            class="lang-dot"
          >{{ lang.toUpperCase() }}</span>
        </div>
      </li>
    </ul>
  </aside>
</template>

<style scoped>
.feed {
  background: var(--c-surface);
  border-top: 1px solid var(--c-border);
  display: flex;
  flex-direction: column;
}

.feed-head {
  position: sticky;
  top: 0;
  z-index: 5;
  background: var(--c-surface);
  border-bottom: 1px solid var(--c-border);
  padding: 10px 14px;
}

.feed-title {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--c-muted);
}

.feed-empty {
  padding: 32px 14px;
  text-align: center;
  color: var(--c-muted);
  font-size: 13px;
}

.feed-list { list-style: none; }

.feed-item {
  padding: 13px 14px;
  border-bottom: 1px solid var(--c-border);
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.feed-item:last-child { border-bottom: none; }

.feed-meta {
  display: flex;
  align-items: center;
  gap: 8px;
}

.feed-date {
  font-family: var(--mono);
  font-size: 11px;
  color: var(--c-muted);
}

.feed-agency {
  font-size: 10px;
  font-weight: 700;
  padding: 1px 6px;
  border-radius: 3px;
  letter-spacing: 0.04em;
}

.feed-title-link {
  font-size: 12.5px;
  font-weight: 500;
  color: var(--c-text);
  text-decoration: none;
  line-height: 1.4;
}

.feed-title-link:hover { color: var(--c-accent); text-decoration: underline; }

.feed-title-text {
  font-size: 12.5px;
  font-weight: 500;
  color: var(--c-text);
  line-height: 1.4;
}

.feed-langs {
  display: flex;
  gap: 4px;
}

.lang-dot {
  font-size: 9px;
  font-weight: 600;
  letter-spacing: 0.04em;
  color: var(--c-muted);
  background: var(--c-bg);
  border: 1px solid var(--c-border);
  padding: 0 4px;
  border-radius: 2px;
}

@media (min-width: 1024px) {
  .feed { border-top: none; }
}
</style>
