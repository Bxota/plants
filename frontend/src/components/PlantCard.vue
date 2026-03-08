<template>
  <div
    class="plant-card"
    :style="{ '--card-accent': accent.circle, '--card-bg': accent.bg }"
    :class="{ 'card-wide': wide }"
  >
    <!-- Actions hover -->
    <div class="card-actions">
      <button class="action-btn" title="Modifier" @click.stop="$emit('edit', plant)">✎</button>
      <button class="action-btn action-btn--danger" title="Supprimer" @click.stop="$emit('delete', plant)">✕</button>
    </div>

    <p class="card-number">{{ String(index + 1).padStart(2, '0') }} —</p>

    <!-- Photo ou emoji -->
    <div class="plant-media">
      <img v-if="plant.photo_url" :src="plant.photo_url" :alt="plant.common_name" class="plant-photo" />
      <span v-else class="plant-icon">{{ plant.emoji || '🌿' }}</span>
    </div>

    <h2 class="plant-common">{{ plant.common_name }}</h2>
    <p v-if="plant.scientific_name" class="plant-scientific">{{ plant.scientific_name }}</p>

    <div class="divider"></div>

    <div class="care-grid">
      <div v-if="plant.watering" class="care-item">
        <p class="care-label">💧 Arrosage</p>
        <p class="care-value">{{ plant.watering }}</p>
      </div>
      <div v-if="plant.light" class="care-item">
        <p class="care-label">☀️ Lumière</p>
        <p class="care-value">{{ plant.light }}</p>
      </div>
      <div v-if="plant.temperature" class="care-item">
        <p class="care-label">🌡️ Température</p>
        <p class="care-value">{{ plant.temperature }}</p>
      </div>
      <div v-if="plant.humidity" class="care-item">
        <p class="care-label">💦 Humidité</p>
        <p class="care-value">{{ plant.humidity }}</p>
      </div>
      <div v-if="plant.fertilization" class="care-item">
        <p class="care-label">🌱 Fertilisation</p>
        <p class="care-value">{{ plant.fertilization }}</p>
      </div>
    </div>

    <p v-if="plant.notes" class="plant-note">{{ plant.notes }}</p>

    <div v-if="plant.tags?.length" class="tags">
      <span v-for="tag in plant.tags" :key="tag" class="tag">{{ tag }}</span>
    </div>

    <span v-if="plant.ai_identified" class="ai-badge">✦ IA</span>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  plant: { type: Object, required: true },
  index: { type: Number, required: true },
  wide: { type: Boolean, default: false },
})

defineEmits(['edit', 'delete'])

const ACCENTS = [
  { circle: '#8ab89a', bg: 'rgba(138,184,154,0.08)' },
  { circle: '#c8dfc8', bg: 'rgba(200,223,200,0.10)' },
  { circle: '#c4923a', bg: 'rgba(196,146,58,0.07)' },
  { circle: '#a05c2c', bg: 'rgba(160,92,44,0.06)' },
  { circle: '#4a7c59', bg: 'rgba(74,124,89,0.08)' },
]

const accent = computed(() => ACCENTS[props.index % ACCENTS.length])
</script>

<style scoped>
.plant-card {
  border-right: 1px solid var(--green-light);
  border-bottom: 1px solid var(--green-light);
  padding: 52px 48px;
  position: relative;
  overflow: hidden;
  transition: background 0.4s ease;
  animation: fadeUp 0.8s ease both;
  cursor: default;
}

.plant-card::before {
  content: '';
  position: absolute;
  bottom: -60px;
  right: -60px;
  width: 200px;
  height: 200px;
  border-radius: 50%;
  background: var(--card-accent, var(--green-pale));
  opacity: 0.25;
  transition: transform 0.5s ease, opacity 0.5s ease;
}

.plant-card:hover::before {
  transform: scale(1.4);
  opacity: 0.4;
}

.plant-card:hover {
  background: var(--card-bg, rgba(200, 223, 200, 0.12));
}

.card-wide {
  grid-column: 1 / -1;
}

/* Actions */
.card-actions {
  position: absolute;
  top: 20px;
  right: 20px;
  display: flex;
  gap: 8px;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.plant-card:hover .card-actions {
  opacity: 1;
}

.action-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 1px solid var(--green-light);
  background: var(--cream);
  color: var(--green-mid);
  cursor: pointer;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.action-btn:hover {
  background: var(--green-pale);
}

.action-btn--danger {
  color: var(--rust);
  border-color: var(--rust);
}

.action-btn--danger:hover {
  background: rgba(160, 92, 44, 0.1);
}

/* Media */
.plant-media {
  margin-bottom: 20px;
}

.plant-icon {
  font-size: 52px;
  display: block;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.1));
  transition: transform 0.3s ease;
}

.plant-card:hover .plant-icon {
  transform: rotate(-5deg) scale(1.1);
}

.plant-photo {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 8px;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.15));
  transition: transform 0.3s ease;
}

.plant-card:hover .plant-photo {
  transform: rotate(-2deg) scale(1.05);
}

/* Text */
.card-number {
  font-size: 11px;
  letter-spacing: 0.2em;
  color: var(--green-light);
  margin-bottom: 28px;
}

.plant-common {
  font-family: 'Playfair Display', serif;
  font-size: 28px;
  font-weight: 400;
  color: var(--green-deep);
  margin-bottom: 4px;
  line-height: 1.2;
}

.plant-scientific {
  font-size: 12px;
  font-style: italic;
  color: var(--ochre);
  margin-bottom: 28px;
  font-family: 'Playfair Display', serif;
}

.divider {
  width: 40px;
  height: 1px;
  background: var(--green-light);
  margin-bottom: 28px;
}

.care-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px 24px;
  margin-bottom: 28px;
}

.care-label {
  font-size: 9px;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--green-mid);
  margin-bottom: 4px;
}

.care-value {
  font-size: 12px;
  color: var(--dark);
  line-height: 1.5;
}

.plant-note {
  font-size: 11px;
  color: var(--green-mid);
  line-height: 1.7;
  border-left: 2px solid var(--green-pale);
  padding-left: 14px;
  font-style: italic;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 24px;
}

.tag {
  font-size: 9px;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  padding: 5px 12px;
  border: 1px solid var(--green-light);
  color: var(--green-mid);
  border-radius: 100px;
}

.ai-badge {
  position: absolute;
  bottom: 16px;
  right: 20px;
  font-size: 9px;
  letter-spacing: 0.15em;
  color: var(--ochre);
  opacity: 0.6;
}

@media (max-width: 720px) {
  .plant-card { padding: 40px 32px; border-right: none; }
  .care-grid { grid-template-columns: 1fr; }
}
</style>
