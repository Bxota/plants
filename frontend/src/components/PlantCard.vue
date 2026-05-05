<template>
  <div
    class="plant-card"
    :style="{ animationDelay: index * 0.06 + 's' }"
    @mouseenter="hovered = true"
    @mouseleave="hovered = false"
    @click="$emit('select', plant)"
  >
    <!-- Glow accent -->
    <div class="card-glow" :class="{ expanded: hovered }" />

    <!-- Actions hover -->
    <div class="card-actions">
      <button class="action-btn" title="Modifier" @click.stop="$emit('edit', plant)">
        <Icon name="edit" :size="13" />
      </button>
      <button class="action-btn action-btn--danger" title="Supprimer" @click.stop="$emit('delete', plant)">
        <Icon name="close" :size="13" />
      </button>
    </div>

    <!-- Badge IA -->
    <div v-if="plant.ai_identified" class="ai-badge">
      <Icon name="sparkle" :size="11" />
      <span>IA</span>
    </div>

    <!-- Top : index + emoji -->
    <div class="card-top">
      <p class="card-num">{{ String(index + 1).padStart(2, '0') }}</p>
      <span class="card-emoji" :class="{ rotated: hovered }">
        {{ plant.emoji || '🌿' }}
      </span>
    </div>

    <!-- Photo -->
    <div v-if="plant.photo_url" class="card-photo-row">
      <img :src="plant.photo_url" alt="Photo" class="plant-image" />
    </div>
    <!-- Noms -->
    <div class="card-names">
      <h2 class="plant-common">{{ plant.common_name }}</h2>
      <p v-if="plant.scientific_name" class="plant-scientific">{{ plant.scientific_name }}</p>
    </div>

    <!-- Bandeau soins -->
    <CareBand :plant="plant" :care-style="careStyle" />

    <!-- Condition chips -->
    <div v-if="conditionTags === 'on' && conditions.length" class="card-conditions">
      <span v-for="c in conditions" :key="c.label" class="condition-chip">
        <Icon :name="c.icon" :size="10" class="chip-icon" />
        {{ c.label }}
      </span>
    </div>

    <!-- Tags utilisateur -->
    <div v-if="plant.tags?.length" class="card-tags">
      <span v-for="tag in plant.tags" :key="tag" class="tag">{{ tag }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import Icon from './Icon.vue'
import CareBand from './CareBand.vue'
import { effectiveLevels, deriveConditionTags } from '@/utils/levels.js'

const props = defineProps({
  plant:         { type: Object,  required: true },
  index:         { type: Number,  required: true },
  careStyle:     { type: String,  default: 'bars' },
  conditionTags: { type: String,  default: 'on' },
})

defineEmits(['edit', 'delete', 'select'])

const hovered = ref(false)

const conditions = computed(() =>
  deriveConditionTags(effectiveLevels(props.plant))
)
</script>

<style scoped>
.plant-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  padding: 32px 30px 28px;
  position: relative;
  overflow: hidden;
  cursor: pointer;
  transition: background 0.3s ease, border-color 0.3s ease;
  animation: fadeUp 0.5s ease both;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.plant-card:hover {
  background: var(--color-surface-hover);
  border-color: var(--color-border-strong);
}

/* Glow */
.card-glow {
  position: absolute;
  bottom: -50px;
  right: -50px;
  width: 180px;
  height: 180px;
  border-radius: 50%;
  background: var(--color-accent-glow);
  transform: scale(1);
  transition: transform 0.5s ease;
  pointer-events: none;
}
.card-glow.expanded {
  transform: scale(1.4);
}

/* Actions */
.card-actions {
  position: absolute;
  top: 14px;
  left: 14px;
  display: flex;
  gap: 6px;
  opacity: 0;
  transition: opacity 0.2s ease;
}
.plant-card:hover .card-actions {
  opacity: 1;
}

.action-btn {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  border: 1px solid var(--color-border);
  background: var(--color-surface);
  color: var(--color-text-muted);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}
.action-btn:hover {
  border-color: var(--color-border-strong);
  color: var(--color-text);
}
.action-btn--danger:hover {
  color: var(--color-warn);
  border-color: var(--color-warn);
}

/* Badge IA */
.ai-badge {
  position: absolute;
  top: 14px;
  right: 14px;
  display: flex;
  align-items: center;
  gap: 4px;
  color: var(--color-accent);
  opacity: 0.7;
  font-family: var(--font-label);
  font-size: 8px;
  letter-spacing: 0.2em;
}

/* Top */
.card-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  position: relative;
}

.card-num {
  font-family: var(--font-label);
  font-size: 10px;
  letter-spacing: 0.25em;
  color: var(--color-accent);
  opacity: 0.6;
}

.card-emoji {
  font-size: 32px;
  transition: transform 0.3s ease;
  display: block;
}
.card-emoji.rotated {
  transform: rotate(-8deg) scale(1.1);
}

/* Noms */
.plant-common {
  font-family: var(--font-display);
  font-size: 24px;
  font-weight: 700;
  color: var(--color-text);
  line-height: 1.1;
  letter-spacing: -0.02em;
  margin-bottom: 4px;
}

.plant-scientific {
  font-family: var(--font-label);
  font-style: italic;
  font-size: 11px;
  color: var(--color-text-muted);
  letter-spacing: 0.02em;
}

/* Conditions */
.card-conditions {
  display: flex;
  gap: 6px;
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

/* Tags */
.card-tags {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  margin-top: auto;
}

.tag {
  font-family: var(--font-label);
  font-size: 9px;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  padding: 3px 9px;
  border: 1px solid var(--color-border);
  border-radius: 2px;
  color: var(--color-text-muted);
}

/* Photo */
.card-photo-row {
  width: 100%;
}
.plant-image {
  width: 100%;
  aspect-ratio: 16 / 10;
  height: auto;
  object-fit: cover;
  border-radius: 8px;
  border: 1px solid var(--color-border);
}

@media (max-width: 720px) {
  .plant-card {
    padding: 24px 20px 22px;
    gap: 16px;
  }

  .plant-common {
    font-size: 21px;
  }

  .card-actions {
    opacity: 1;
  }
}
</style>
