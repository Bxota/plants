<template>
  <svg
    :width="size"
    :height="size"
    viewBox="0 0 20 20"
    fill="none"
    :stroke="stroke"
    :stroke-width="sw"
    stroke-linecap="round"
    stroke-linejoin="round"
  >
    <template v-if="name === 'water'">
      <path d="M10 2.5 C 6 7, 4 10, 4 13 a 6 6 0 0 0 12 0 C 16 10, 14 7, 10 2.5 Z" />
      <path d="M7 13 a 3 3 0 0 0 3 3" opacity="0.5" />
    </template>
    <template v-else-if="name === 'sun'">
      <circle cx="10" cy="10" r="3.2" />
      <path d="M10 2.5 V4 M10 16 V17.5 M2.5 10 H4 M16 10 H17.5 M4.5 4.5 L5.6 5.6 M14.4 14.4 L15.5 15.5 M4.5 15.5 L5.6 14.4 M14.4 5.6 L15.5 4.5" />
    </template>
    <template v-else-if="name === 'temp'">
      <path d="M8 12 V4.5 a 2 2 0 1 1 4 0 V12" />
      <circle cx="10" cy="14.5" r="2.2" />
      <line x1="10" y1="6" x2="10" y2="12.5" opacity="0.5" />
    </template>
    <template v-else-if="name === 'humidity'">
      <path d="M10 3 C 7 6, 5 9, 5 12 a 5 5 0 0 0 10 0 C 15 9, 13 6, 10 3 Z" />
      <path d="M10 9 C 8.5 11, 7.5 12, 7.5 13.5 a 2.5 2.5 0 0 0 5 0 C 12.5 12, 11.5 11, 10 9 Z" opacity="0.5" />
    </template>
    <template v-else-if="name === 'fertilizer'">
      <path d="M10 16.5 V 9" />
      <path d="M10 9 C 7 9, 5 7, 5.5 4 C 8 4.5, 10 6, 10 9 Z" />
      <path d="M10 11 C 13 11, 15 9, 14.5 6 C 12 6.5, 10 8, 10 11 Z" />
    </template>
    <template v-else-if="name === 'plus'">
      <line x1="10" y1="4" x2="10" y2="16" />
      <line x1="4" y1="10" x2="16" y2="10" />
    </template>
    <template v-else-if="name === 'settings'">
      <circle cx="10" cy="10" r="2.2" />
      <path d="M10 2 V4 M10 16 V18 M2 10 H4 M16 10 H18 M4.5 4.5 L5.9 5.9 M14.1 14.1 L15.5 15.5 M4.5 15.5 L5.9 14.1 M14.1 5.9 L15.5 4.5" />
    </template>
    <template v-else-if="name === 'logout'">
      <path d="M12 4 H15 a 1.5 1.5 0 0 1 1.5 1.5 V14.5 a 1.5 1.5 0 0 1 -1.5 1.5 H12" />
      <path d="M9 7 L6 10 L9 13" />
      <line x1="6" y1="10" x2="13" y2="10" />
    </template>
    <template v-else-if="name === 'grid'">
      <rect x="3" y="3" width="6" height="6" />
      <rect x="11" y="3" width="6" height="6" />
      <rect x="3" y="11" width="6" height="6" />
      <rect x="11" y="11" width="6" height="6" />
    </template>
    <template v-else-if="name === 'list'">
      <line x1="6" y1="5" x2="17" y2="5" />
      <line x1="6" y1="10" x2="17" y2="10" />
      <line x1="6" y1="15" x2="17" y2="15" />
      <circle cx="3.5" cy="5" r="0.6" :fill="stroke" stroke="none" />
      <circle cx="3.5" cy="10" r="0.6" :fill="stroke" stroke="none" />
      <circle cx="3.5" cy="15" r="0.6" :fill="stroke" stroke="none" />
    </template>
    <template v-else-if="name === 'edit'">
      <path d="M3 17 L3 14 L13 4 L16 7 L6 17 Z" />
    </template>
    <template v-else-if="name === 'close'">
      <line x1="5" y1="5" x2="15" y2="15" />
      <line x1="15" y1="5" x2="5" y2="15" />
    </template>
    <template v-else-if="name === 'sparkle'">
      <path d="M10 3 L11 8 L16 10 L11 12 L10 17 L9 12 L4 10 L9 8 Z" />
    </template>
    <!-- Moon : crescent filled, pas de stroke -->
    <template v-else-if="name === 'moon'">
      <path
        d="M17.5 10.7A7.5 7.5 0 1 1 9.3 2.5 5.8 5.8 0 0 0 17.5 10.7z"
        fill="currentColor"
        stroke="none"
      />
    </template>
    <!-- User / admin : silhouette personne -->
    <template v-else-if="name === 'user'">
      <circle cx="10" cy="7.5" r="3.2" />
      <path d="M3.5 18.5c0-3.6 2.9-6.5 6.5-6.5s6.5 2.9 6.5 6.5" />
    </template>
    <!-- Gear (cog) : engrenage avec dents, distinct du soleil -->
    <template v-else-if="name === 'gear'">
      <circle cx="10" cy="10" r="3" />
      <path d="M10 1.5v2M10 16.5v2M1.5 10h2M16.5 10h2M4.4 4.4l1.4 1.4M14.2 14.2l1.4 1.4M15.6 4.4l-1.4 1.4M6.2 14.2l-1.4 1.4" stroke-width="2" />
    </template>
    <template v-else-if="name === 'trash'">
      <path d="M5 6 H15" />
      <path d="M7 6 V4 H13 V6" />
      <path d="M6 6 L7 16 H13 L14 6" />
      <line x1="9" y1="9" x2="9" y2="14" opacity="0.5" />
      <line x1="11" y1="9" x2="11" y2="14" opacity="0.5" />
    </template>
    <template v-else-if="name === 'image'">
      <rect x="3" y="4" width="14" height="12" rx="1" />
      <circle cx="7" cy="8" r="1.2" />
      <path d="M3 14 L8 10 L13 14 L17 11" />
    </template>
    <template v-else-if="name === 'upload'">
      <path d="M10 13 V3 M6 7 L10 3 L14 7" />
      <path d="M3 14 V16 a 1 1 0 0 0 1 1 H16 a 1 1 0 0 0 1 -1 V14" />
    </template>
  </svg>
</template>

<script setup>
defineProps({
  name:   { type: String, required: true },
  size:   { type: Number, default: 18 },
  stroke: { type: String, default: 'currentColor' },
  sw:     { type: Number, default: 1.4 },
})
</script>
