<template>
  <div class="plant-row" @click="$emit('select', plant)">
    <!-- index + photo thumbnail OU emoji -->
    <div class="row-id">
      <span class="row-num">{{ String(index + 1).padStart(2, '0') }}</span>
      <div v-if="plant.photo_url" class="row-thumb">
        <img :src="plant.photo_url" :alt="plant.common_name" />
      </div>
      <span v-else class="row-emoji">{{ plant.emoji || '🌿' }}</span>
    </div>

    <!-- Nom -->
    <div class="row-name">
      <div class="row-common">{{ plant.common_name }}</div>
      <div v-if="plant.scientific_name" class="row-scientific">{{ plant.scientific_name }}</div>
    </div>

    <!-- Care band compacte -->
    <CareBand :plant="plant" :care-style="careStyle" compact />

    <!-- Condition chips -->
    <div class="row-conditions">
      <template v-if="conditionTags === 'on'">
        <span
          v-for="c in conditions.slice(0, 2)"
          :key="c.label"
          class="condition-chip"
        >
          <Icon :name="c.icon" :size="10" class="chip-icon" />
          {{ c.label }}
        </span>
      </template>
    </div>

    <!-- Badge IA -->
    <div class="row-ai" :class="{ visible: plant.ai_identified }">
      <Icon name="sparkle" :size="11" />
      <span>IA</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import Icon from './Icon.vue'
import CareBand from './CareBand.vue'
import { effectiveLevels, deriveConditionTags } from '@/utils/levels.js'

const props = defineProps({
  plant:         { type: Object,  required: true },
  index:         { type: Number,  required: true },
  careStyle:     { type: String,  default: 'bars' },
  conditionTags: { type: String,  default: 'on' },
})

defineEmits(['select', 'edit', 'delete'])

const conditions = computed(() => deriveConditionTags(effectiveLevels(props.plant)))
</script>

<style scoped>
.plant-row {
  display: grid;
  grid-template-columns: 60px minmax(180px, 1.6fr) minmax(280px, 2fr) minmax(180px, 1.4fr) 80px;
  align-items: center;
  gap: 24px;
  padding: 20px 32px;
  border-bottom: 1px solid var(--color-border);
  cursor: pointer;
  transition: background 0.2s;
  animation: fadeUp 0.4s ease both;
}

.plant-row:hover {
  background: var(--color-surface-hover);
}

.row-id {
  display: flex;
  align-items: center;
  gap: 12px;
}

.row-num {
  font-family: var(--font-label);
  font-size: 10px;
  letter-spacing: 0.2em;
  color: var(--color-accent);
  opacity: 0.5;
}

.row-emoji {
  font-size: 22px;
}

.row-thumb {
  width: 32px;
  height: 32px;
  border-radius: 3px;
  overflow: hidden;
  border: 1px solid var(--color-border);
  flex-shrink: 0;
}
.row-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.row-common {
  font-family: var(--font-display);
  font-size: 17px;
  font-weight: 600;
  color: var(--color-text);
  letter-spacing: -0.01em;
}

.row-scientific {
  font-family: var(--font-label);
  font-style: italic;
  font-size: 11px;
  color: var(--color-text-muted);
  margin-top: 2px;
}

.row-conditions {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}

.condition-chip {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 3px 8px;
  border: 1px solid var(--color-border-strong);
  border-radius: 100px;
  background: var(--color-accent-dim);
  font-family: var(--font-label);
  font-size: 9px;
  letter-spacing: 0.06em;
  color: var(--color-accent);
  text-transform: lowercase;
}

.chip-icon {
  color: var(--color-accent);
}

.row-ai {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 4px;
  color: var(--color-accent);
  opacity: 0;
  font-family: var(--font-label);
  font-size: 8px;
  letter-spacing: 0.2em;
}

.row-ai.visible {
  opacity: 0.7;
}

@media (max-width: 900px) {
  .plant-row {
    grid-template-columns: 48px 1fr 1fr;
    gap: 12px;
    padding: 16px 20px;
  }
  .row-conditions, .row-ai { display: none; }
}
</style>
