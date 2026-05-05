<template>
  <div class="care-band" :class="{ compact }">
    <div v-for="m in METRICS" :key="m.key" class="metric">
      <Icon :name="m.icon" :size="compact ? 14 : 18" class="metric-icon" />
      <LevelMeter :value="levels[m.key] ?? 0" :style="careStyle" />
      <span v-if="!compact" class="metric-label">{{ m.label }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import Icon from './Icon.vue'
import LevelMeter from './LevelMeter.vue'
import { effectiveLevels } from '@/utils/levels.js'

const props = defineProps({
  plant:     { type: Object, required: true },
  careStyle: { type: String, default: 'bars' },
  compact:   { type: Boolean, default: false },
})

const METRICS = [
  { key: 'water',      icon: 'water',      label: 'Eau' },
  { key: 'light',      icon: 'sun',        label: 'Lumière' },
  { key: 'temp',       icon: 'temp',       label: 'Temp.' },
  { key: 'humidity',   icon: 'humidity',   label: 'Humidité' },
  { key: 'fertilizer', icon: 'fertilizer', label: 'Fert.' },
]

const levels = computed(() => effectiveLevels(props.plant))
</script>

<style scoped>
.care-band {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 12px;
  padding: 14px 0;
  border-top: 1px solid var(--color-border);
  border-bottom: 1px solid var(--color-border);
}

.care-band.compact {
  gap: 6px;
  padding: 0;
  border: none;
}

.metric {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}

.metric-icon {
  color: var(--color-accent);
  opacity: 0.85;
}

.metric-label {
  font-family: var(--font-label);
  font-size: 8px;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--color-text-muted);
}
</style>
