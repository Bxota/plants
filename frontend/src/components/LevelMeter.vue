<template>
  <!-- bars (défaut) -->
  <div v-if="style === 'bars'" class="level-bars">
    <span v-for="i in 5" :key="i" class="bar" :class="{ active: i <= value }" />
  </div>

  <!-- dots -->
  <div v-else-if="style === 'dots'" class="level-dots">
    <span v-for="i in 5" :key="i" class="dot" :class="{ active: i <= value }" />
  </div>

  <!-- ticks -->
  <div v-else class="level-ticks">
    <span
      v-for="i in 5"
      :key="i"
      class="tick"
      :class="{ active: i <= value }"
      :style="{ height: (4 + (i - 1) * 2) + 'px' }"
    />
  </div>
</template>

<script setup>
defineProps({
  value: { type: Number, required: true },
  style: { type: String, default: 'bars' },
})
</script>

<style scoped>
/* ── bars ── */
.level-bars {
  display: flex;
  gap: 2px;
  height: 3px;
  width: 54px;
}
.bar {
  flex: 1;
  background: var(--color-text-dim);
  opacity: 0.35;
}
.bar.active {
  background: var(--color-accent);
  opacity: 1;
}

/* ── dots ── */
.level-dots {
  display: flex;
  gap: 3px;
  align-items: center;
}
.dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  border: 1px solid var(--color-text-dim);
  background: transparent;
}
.dot.active {
  background: var(--color-accent);
  border-color: var(--color-accent);
}

/* ── ticks ── */
.level-ticks {
  display: flex;
  gap: 2px;
  align-items: flex-end;
  height: 12px;
}
.tick {
  width: 2px;
  background: var(--color-text-dim);
  opacity: 0.4;
}
.tick.active {
  background: var(--color-accent);
  opacity: 1;
}
</style>
