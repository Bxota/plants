<template>
  <Teleport to="body">
    <div class="overlay" @click.self="$emit('close')">
      <div class="panel">
        <!-- Header sticky -->
        <div class="panel-header">
          <div class="header-top">
            <p class="eyebrow">Fiche plante</p>
            <button class="close-btn" @click="$emit('close')">
              <Icon name="close" :size="14" />
            </button>
          </div>

          <div class="plant-identity">
            <div v-if="plant.photo_url" class="identity-thumb">
              <img :src="plant.photo_url" :alt="plant.common_name" />
            </div>
            <span v-else class="plant-emoji">{{ plant.emoji || '🌿' }}</span>
            <div>
              <h2 class="plant-common">{{ plant.common_name }}</h2>
              <p v-if="plant.scientific_name" class="plant-scientific">{{ plant.scientific_name }}</p>
            </div>
          </div>

          <div v-if="conditions.length" class="conditions">
            <span v-for="c in conditions" :key="c.label" class="condition-chip">
              <Icon :name="c.icon" :size="12" class="chip-icon" />
              {{ c.label }}
            </span>
          </div>
        </div>

        <!-- Body -->
        <div class="panel-body">
          <p class="section-label">Besoins</p>

          <div v-for="m in METRICS" :key="m.key" class="metric-row">
            <Icon :name="m.icon" :size="18" class="metric-icon" />
            <div class="metric-info">
              <div class="metric-name">{{ m.label }}</div>
              <div class="metric-detail">{{ detailFor(m.key) || '—' }}</div>
            </div>
            <LevelMeter :value="levels[m.key] ?? 3" :style="careStyle" />
          </div>

          <!-- Notes -->
          <div v-if="plant.notes" class="notes-section">
            <p class="section-label">Note</p>
            <p class="notes-text">{{ plant.notes }}</p>
          </div>

          <!-- Tags -->
          <div v-if="plant.tags?.length" class="tags-section">
            <p class="section-label">Tags</p>
            <div class="tags">
              <span v-for="tag in plant.tags" :key="tag" class="tag">{{ tag }}</span>
            </div>
          </div>
        </div>

        <!-- Footer sticky -->
        <div class="panel-footer">
          <button class="btn btn-danger" @click="$emit('delete', plant)">
            <Icon name="trash" :size="12" />
            Supprimer
          </button>
          <button class="btn btn-primary" @click="$emit('edit', plant)">
            <Icon name="edit" :size="12" />
            Modifier
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { computed } from 'vue'
import Icon from './Icon.vue'
import LevelMeter from './LevelMeter.vue'
import { effectiveLevels, deriveConditionTags } from '@/utils/levels.js'

const props = defineProps({
  plant:     { type: Object, required: true },
  careStyle: { type: String, default: 'bars' },
})

defineEmits(['close', 'edit', 'delete'])

const METRICS = [
  { key: 'water',      icon: 'water',      label: 'Arrosage' },
  { key: 'light',      icon: 'sun',        label: 'Lumière' },
  { key: 'temp',       icon: 'temp',       label: 'Température' },
  { key: 'humidity',   icon: 'humidity',   label: 'Humidité' },
  { key: 'fertilizer', icon: 'fertilizer', label: 'Fertilisation' },
]

const DETAIL_KEYS = {
  water:      'watering',
  light:      'light',
  temp:       'temperature',
  humidity:   'humidity',
  fertilizer: 'fertilization',
}

const levels     = computed(() => effectiveLevels(props.plant))
const conditions = computed(() => deriveConditionTags(levels.value))

function detailFor(key) {
  return props.plant[DETAIL_KEYS[key]] ?? null
}
</script>

<style scoped>
.overlay {
  position: fixed;
  inset: 0;
  z-index: 500;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(4px);
  display: flex;
  justify-content: flex-end;
  animation: fadeIn 0.2s ease;
}

.panel {
  width: 100%;
  max-width: 540px;
  height: 100vh;
  background: var(--color-surface);
  border-left: 1px solid var(--color-border-strong);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  animation: slideIn 0.3s ease;
}

/* ── Header ── */
.panel-header {
  padding: 36px 36px 28px;
  border-bottom: 1px solid var(--color-border);
  position: sticky;
  top: 0;
  background: var(--color-surface);
  z-index: 10;
}

.header-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
}

.eyebrow {
  font-family: var(--font-label);
  font-size: 10px;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  color: var(--color-accent);
  opacity: 0.7;
}

.close-btn {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  border: 1px solid var(--color-border);
  background: transparent;
  color: var(--color-text-muted);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: border-color 0.2s, color 0.2s;
}
.close-btn:hover {
  border-color: var(--color-border-strong);
  color: var(--color-text);
}

.plant-identity {
  display: flex;
  gap: 20px;
  align-items: flex-end;
  margin-bottom: 20px;
}

.plant-emoji {
  font-size: 52px;
  line-height: 1;
}

.identity-thumb {
  width: 88px;
  height: 88px;
  border-radius: 4px;
  overflow: hidden;
  border: 1px solid var(--color-border-strong);
  flex-shrink: 0;
}
.identity-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.plant-common {
  font-family: var(--font-display);
  font-size: 30px;
  font-weight: 700;
  color: var(--color-text);
  line-height: 1.05;
  letter-spacing: -0.02em;
}

.plant-scientific {
  font-family: var(--font-label);
  font-style: italic;
  font-size: 13px;
  color: var(--color-text-muted);
  margin-top: 4px;
}

.conditions {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.condition-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 5px 10px;
  border: 1px solid var(--color-border-strong);
  border-radius: 100px;
  background: var(--color-accent-dim);
  font-family: var(--font-label);
  font-size: 10px;
  letter-spacing: 0.06em;
  color: var(--color-accent);
  text-transform: lowercase;
}

.chip-icon {
  color: var(--color-accent);
}

/* ── Body ── */
.panel-body {
  padding: 28px 36px;
  flex: 1;
}

.section-label {
  font-family: var(--font-label);
  font-size: 9px;
  letter-spacing: 0.3em;
  text-transform: uppercase;
  color: var(--color-accent);
  opacity: 0.6;
  margin-bottom: 16px;
}

.metric-row {
  display: grid;
  grid-template-columns: 24px 1fr auto;
  align-items: center;
  gap: 14px;
  padding: 14px 0;
  border-bottom: 1px solid var(--color-border);
}

.metric-icon {
  color: var(--color-accent);
  opacity: 0.85;
}

.metric-name {
  font-family: var(--font-label);
  font-size: 10px;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--color-text-muted);
  margin-bottom: 3px;
}

.metric-detail {
  font-family: var(--font-label);
  font-size: 13px;
  color: var(--color-text);
}

/* Notes */
.notes-section {
  margin-top: 28px;
}

.notes-text {
  font-family: var(--font-label);
  font-size: 13px;
  color: var(--color-text-muted);
  line-height: 1.7;
  border-left: 2px solid var(--color-accent);
  padding-left: 16px;
}

/* Tags */
.tags-section {
  margin-top: 28px;
}

.tags {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.tag {
  font-family: var(--font-label);
  font-size: 10px;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  padding: 5px 12px;
  border: 1px solid var(--color-border);
  color: var(--color-text-muted);
  border-radius: 2px;
}

/* ── Footer ── */
.panel-footer {
  padding: 20px 36px;
  border-top: 1px solid var(--color-border);
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  position: sticky;
  bottom: 0;
  background: var(--color-surface);
}

@media (max-width: 600px) {
  .overlay { align-items: stretch; }
  .panel { max-width: 100%; height: 100dvh; }
  .panel-header, .panel-body, .panel-footer { padding-left: 24px; padding-right: 24px; }
  .panel-header { padding-top: calc(36px + env(safe-area-inset-top)); top: env(safe-area-inset-top); }
  .panel-footer { padding-bottom: calc(20px + env(safe-area-inset-bottom)); }
  .plant-identity { align-items: center; }
  .plant-emoji { font-size: 44px; }
  .plant-common { font-size: 26px; }
  .metric-row { grid-template-columns: 24px 1fr; }
  .metric-row :deep(.level-meter) { grid-column: 1 / -1; }
}
</style>
