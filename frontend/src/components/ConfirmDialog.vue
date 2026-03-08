<template>
  <Teleport to="body">
    <div v-if="modelValue" class="overlay" @click.self="$emit('update:modelValue', false)">
      <div class="dialog">
        <p class="dialog-title">{{ title }}</p>
        <p class="dialog-body">{{ message }}</p>
        <div class="dialog-actions">
          <button class="btn btn-ghost" @click="$emit('update:modelValue', false)">Annuler</button>
          <button class="btn btn-danger" @click="confirm">{{ confirmLabel }}</button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
const props = defineProps({
  modelValue: Boolean,
  title: { type: String, default: 'Confirmer' },
  message: { type: String, default: 'Cette action est irréversible.' },
  confirmLabel: { type: String, default: 'Supprimer' },
})
const emit = defineEmits(['update:modelValue', 'confirm'])

function confirm() {
  emit('confirm')
  emit('update:modelValue', false)
}
</script>

<style scoped>
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(26, 26, 20, 0.5);
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(2px);
}

.dialog {
  background: var(--cream);
  border: 1px solid var(--green-light);
  padding: 40px;
  max-width: 420px;
  width: 90%;
  animation: fadeUp 0.2s ease;
}

.dialog-title {
  font-family: 'Playfair Display', serif;
  font-size: 22px;
  color: var(--green-deep);
  margin-bottom: 12px;
}

.dialog-body {
  font-size: 12px;
  color: var(--green-mid);
  line-height: 1.6;
  margin-bottom: 32px;
}

.dialog-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}
</style>
