<template>
  <div class="photo-upload">
    <!-- Zone de drop -->
    <div
      v-if="state === 'idle' || state === 'error'"
      class="drop-zone"
      :class="{ 'drop-zone--over': isDragOver, 'drop-zone--error': state === 'error' }"
      @dragover.prevent="isDragOver = true"
      @dragleave="isDragOver = false"
      @drop.prevent="onDrop"
      @click="fileInput.click()"
    >
      <span class="drop-icon">📷</span>
      <p class="drop-text">Glissez une photo ici ou cliquez</p>
      <p class="drop-hint">JPG, PNG, WEBP — max 10 Mo</p>
      <p v-if="state === 'error'" class="drop-error">{{ errorMessage }}</p>
      <input
        ref="fileInput"
        type="file"
        accept="image/jpeg,image/png,image/webp"
        class="file-input"
        @change="onFileSelected"
      />
    </div>

    <!-- Preview -->
    <div v-if="state === 'preview'" class="preview-zone">
      <img :src="previewUrl" alt="Aperçu" class="preview-img" />
      <div class="preview-actions">
        <button type="button" class="btn btn-primary" @click="identify">
          Identifier par IA ✦
        </button>
        <button type="button" class="btn btn-ghost" @click="reset">Changer</button>
      </div>
    </div>

    <!-- Chargement IA -->
    <div v-if="state === 'loading'">
      <AiLoader />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import AiLoader from './AiLoader.vue'
import { usePlantsStore } from '@/stores/plants'

const emit = defineEmits(['identified', 'file-selected'])

const store = usePlantsStore()
const fileInput = ref(null)
const state = ref('idle') // idle | preview | loading | error
const isDragOver = ref(false)
const previewUrl = ref(null)
const currentFile = ref(null)
const errorMessage = ref('')

function onDrop(e) {
  isDragOver.value = false
  const file = e.dataTransfer.files[0]
  if (file) loadFile(file)
}

function onFileSelected(e) {
  const file = e.target.files[0]
  if (file) loadFile(file)
}

function loadFile(file) {
  if (!file.type.startsWith('image/')) {
    errorMessage.value = 'Format non supporté'
    state.value = 'error'
    return
  }
  if (file.size > 10 * 1024 * 1024) {
    errorMessage.value = 'Fichier trop volumineux (max 10 Mo)'
    state.value = 'error'
    return
  }

  currentFile.value = file
  previewUrl.value = URL.createObjectURL(file)
  state.value = 'preview'
  emit('file-selected', file)
}

async function identify() {
  if (!currentFile.value) return
  state.value = 'loading'

  try {
    const data = await store.identify(currentFile.value)
    emit('identified', { data, file: currentFile.value })
    state.value = 'preview'
  } catch (e) {
    errorMessage.value = 'Identification impossible. Remplissez manuellement.'
    state.value = 'error'
  }
}

function reset() {
  state.value = 'idle'
  previewUrl.value = null
  currentFile.value = null
  if (fileInput.value) fileInput.value.value = ''
}

defineExpose({ reset })
</script>

<style scoped>
.drop-zone {
  border: 2px dashed var(--green-light);
  border-radius: 8px;
  padding: 48px 24px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s ease;
  background: var(--cream);
  position: relative;
}

.drop-zone:hover,
.drop-zone--over {
  border-color: var(--green-mid);
  background: rgba(200, 223, 200, 0.15);
}

.drop-zone--error {
  border-color: var(--rust);
}

.drop-icon {
  font-size: 36px;
  display: block;
  margin-bottom: 12px;
}

.drop-text {
  font-size: 13px;
  color: var(--green-deep);
  margin-bottom: 6px;
}

.drop-hint {
  font-size: 10px;
  color: var(--green-light);
  letter-spacing: 0.1em;
}

.drop-error {
  font-size: 11px;
  color: var(--rust);
  margin-top: 8px;
}

.file-input {
  display: none;
}

/* Preview */
.preview-zone {
  display: flex;
  align-items: center;
  gap: 24px;
  padding: 16px;
  border: 1px solid var(--green-light);
  border-radius: 8px;
  background: var(--cream);
}

.preview-img {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 6px;
  flex-shrink: 0;
}

.preview-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>
