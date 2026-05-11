<script setup>
import { computed } from 'vue'

const props = defineProps({
  newsFeed: { type: Array, default: () => [] },
  cases:    { type: Array, default: () => [] },
})

/* Si el JSON no trae news_feed, derivamos entradas desde los casos */
const items = computed(() => {
  if (props.newsFeed.length) return props.newsFeed
  return [...props.cases]
    .sort((a, b) => b.fecha_confirmacion.localeCompare(a.fecha_confirmacion))
    .map(c => ({
      date:      c.fecha_confirmacion,
      title:     `Caso confirmado — ${c.region}`,
      body:      `${c.sexo === 'M' ? 'Hombre' : 'Mujer'} de ${c.edad} años. ` +
                 `Factor de exposición: ${c.exposicion.toLowerCase()}.`,
      source:    c.fuente,
      desenlace: c.desenlace,
    }))
})
</script>

<template>
  <aside class="feed">
    <div class="feed-head">
      <h2 class="feed-title">Actividad reciente</h2>
    </div>

    <p v-if="items.length === 0" class="feed-empty">Sin entradas disponibles.</p>

    <ul v-else class="feed-list">
      <li v-for="(item, i) in items" :key="i" class="feed-item">
        <time class="feed-date">{{ item.date }}</time>
        <p class="feed-item-title">{{ item.title }}</p>
        <p class="feed-body">{{ item.body }}</p>
        <div class="feed-foot">
          <span
            v-if="item.desenlace"
            class="badge"
            :class="`badge--${item.desenlace}`"
          >{{ item.desenlace }}</span>
          <span v-if="item.source" class="feed-source">{{ item.source }}</span>
        </div>
      </li>
    </ul>
  </aside>
</template>

<style scoped>
.feed {
  background: var(--c-surface);
  border-top: 1px solid var(--c-border);
}

.feed-head {
  position: sticky;
  top: 0;
  z-index: 5;
  background: var(--c-surface);
  border-bottom: 1px solid var(--c-border);
  padding: 12px 16px;
}

.feed-title {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--c-muted);
}

.feed-empty {
  padding: 32px 16px;
  text-align: center;
  color: var(--c-muted);
  font-size: 13px;
}

.feed-list { list-style: none; }

.feed-item {
  padding: 16px;
  border-bottom: 1px solid var(--c-border);
}

.feed-item:last-child { border-bottom: none; }

.feed-date {
  display: block;
  font-family: var(--mono);
  font-size: 11px;
  color: var(--c-muted);
  margin-bottom: 5px;
}

.feed-item-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--c-text);
  line-height: 1.35;
  margin-bottom: 6px;
}

.feed-body {
  font-size: 12.5px;
  color: var(--c-muted);
  line-height: 1.55;
  margin-bottom: 10px;
}

.feed-foot {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.feed-source {
  font-size: 10.5px;
  color: var(--c-accent);
}

/* Badges reutilizados — mismas variables que CasesList */
.badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 3px;
  font-size: 10.5px;
  font-weight: 600;
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
  .feed {
    border-top: none;
  }
}
</style>
