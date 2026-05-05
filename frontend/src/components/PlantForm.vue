<template>
  <Teleport to="body">
    <div v-if="modelValue" class="overlay" @click.self="close">
      <div class="panel">

        <!-- Header sticky -->
        <div class="panel-header">
          <div class="header-top">
            <p class="eyebrow">{{ isEdit ? 'Modifier la plante' : 'Nouvelle plante' }}</p>
            <button class="close-btn" @click="close">
              <Icon name="close" :size="14" />
            </button>
          </div>
          <h2 class="panel-title">
            {{ isEdit ? plant?.common_name : 'Ajouter' }}
            <span v-if="aiPrefilled" class="ai-badge">
              <Icon name="sparkle" :size="11" /> identifié par IA
            </span>
          </h2>
        </div>

        <!-- Body -->
        <div class="panel-body">

          <!-- Photo -->
          <div class="form-section">
            <p class="section-label">Photo</p>
            <div v-if="isEdit && form.photo_url" class="current-photo-row">
              <img :src="form.photo_url" alt="Photo" class="current-photo" />
              <button type="button" class="btn btn-ghost" @click="form.photo_url = null">
                Changer
              </button>
            </div>
            <PhotoUpload
              v-if="!isEdit || !form.photo_url"
              ref="photoUploadRef"
              @identified="onIdentified"
              @file-selected="pendingFile = $event"
            />
          </div>

          <div class="form-divider" />

          <!-- Identité -->
          <div class="form-section">
            <p class="section-label">Identité</p>
            <div class="form-row">
              <div class="form-field form-field--wide">
                <label>Nom commun *</label>
                <input v-model="form.common_name" type="text" placeholder="Caféier" required />
              </div>
              <div class="form-field">
                <label>Emoji</label>
                <div class="emoji-picker">
                  <button
                    v-for="e in EMOJIS"
                    :key="e"
                    type="button"
                    class="emoji-btn"
                    :class="{ active: form.emoji === e }"
                    @click="form.emoji = e"
                  >{{ e }}</button>
                </div>
              </div>
            </div>
            <div class="form-field">
              <label>Nom scientifique</label>
              <input v-model="form.scientific_name" type="text" placeholder="Coffea arabica" />
            </div>
          </div>

          <div class="form-divider" />

          <!-- Niveaux 1-5 -->
          <div class="form-section">
            <p class="section-label">Niveaux de soin</p>
            <p class="section-hint">Remplis automatiquement par l'IA, ajustables manuellement.</p>
            <div class="levels-list">
              <div v-for="m in METRICS" :key="m.key" class="level-row">
                <Icon :name="m.icon" :size="16" class="level-icon" />
                <span class="level-label">{{ m.label }}</span>
                <div class="level-btns">
                  <button
                    v-for="n in 5"
                    :key="n"
                    type="button"
                    class="level-btn"
                    :class="{ active: editLevels[m.key] >= n }"
                    @click="setLevel(m.key, n)"
                  />
                </div>
                <span class="level-val">{{ editLevels[m.key] }}/5</span>
              </div>
            </div>
          </div>

          <div class="form-divider" />

          <!-- Soins textuels -->
          <div class="form-section">
            <p class="section-label">Détail des soins</p>
            <div class="form-row">
              <div class="form-field">
                <label>Arrosage</label>
                <input v-model="form.watering" type="text" placeholder="Tous les 15 jours…" />
              </div>
              <div class="form-field">
                <label>Lumière</label>
                <input v-model="form.light" type="text" placeholder="Lumière vive indirecte…" />
              </div>
              <div class="form-field">
                <label>Température</label>
                <input v-model="form.temperature" type="text" placeholder="18 – 24 °C" />
              </div>
              <div class="form-field">
                <label>Humidité</label>
                <input v-model="form.humidity" type="text" placeholder="Élevée…" />
              </div>
              <div class="form-field form-field--wide">
                <label>Fertilisation</label>
                <input v-model="form.fertilization" type="text" placeholder="Printemps–été, tous les 15 jours…" />
              </div>
            </div>
          </div>

          <div class="form-divider" />

          <!-- Notes & Tags -->
          <div class="form-section">
            <p class="section-label">Notes & Tags</p>
            <div class="form-field">
              <label>Note</label>
              <textarea v-model="form.notes" rows="3" placeholder="Particularité botanique, conseil important…" />
            </div>
            <div class="form-field">
              <label>Tags</label>
              <TagInput v-model="form.tags" />
            </div>
          </div>
        </div>

        <!-- Footer sticky -->
        <div class="panel-footer">
          <p v-if="error" class="form-error">{{ error }}</p>
          <div class="footer-actions">
            <button type="button" class="btn btn-ghost" @click="close">Annuler</button>
            <button
              type="button"
              class="btn btn-primary"
              :disabled="saving || !form.common_name"
              @click="save"
            >
              {{ saving ? 'Enregistrement…' : (isEdit ? 'Mettre à jour' : 'Ajouter la plante') }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import PhotoUpload from './PhotoUpload.vue'
import TagInput from './TagInput.vue'
import Icon from './Icon.vue'
import { usePlantsStore } from '@/stores/plants'

const props = defineProps({
  modelValue: Boolean,
  plant: { type: Object, default: null },
})
const emit = defineEmits(['update:modelValue', 'saved'])

const store      = usePlantsStore()
const isEdit     = computed(() => !!props.plant?.id)
const aiPrefilled  = ref(false)
const pendingFile  = ref(null)
const saving       = ref(false)
const error        = ref('')
const photoUploadRef = ref(null)

const EMOJIS = ['🌿', '🌱', '🌵', '🌴', '🌺', '🌸', '🌼', '🍃', '🎋', '🪴', '☕']

const METRICS = [
  { key: 'water',      icon: 'water',      label: 'Arrosage' },
  { key: 'light',      icon: 'sun',        label: 'Lumière' },
  { key: 'temp',       icon: 'temp',       label: 'Température' },
  { key: 'humidity',   icon: 'humidity',   label: 'Humidité' },
  { key: 'fertilizer', icon: 'fertilizer', label: 'Fertilisation' },
]

const DEFAULT_LEVELS = { water: 3, light: 3, temp: 3, humidity: 3, fertilizer: 3 }

const defaultForm = () => ({
  common_name: '',
  scientific_name: '',
  emoji: '🌿',
  watering: '',
  light: '',
  temperature: '',
  humidity: '',
  fertilization: '',
  levels: null,
  notes: '',
  tags: [],
  photo_url: null,
})

const form = ref(defaultForm())

const editLevels = computed(() => form.value.levels ?? DEFAULT_LEVELS)

function setLevel(key, val) {
  form.value.levels = { ...editLevels.value, [key]: val }
}

watch(
  () => props.modelValue,
  (open) => {
    if (open) {
      aiPrefilled.value = false
      pendingFile.value = null
      error.value = ''
      form.value = props.plant ? { ...defaultForm(), ...props.plant } : defaultForm()
    }
  }
)

function onIdentified({ data, file }) {
  pendingFile.value = file
  aiPrefilled.value = true
  form.value = {
    ...form.value,
    common_name:    data.common_name    || form.value.common_name,
    scientific_name: data.scientific_name || '',
    emoji:          data.emoji          || '🌿',
    watering:       data.watering       || '',
    light:          data.light          || '',
    temperature:    data.temperature    || '',
    humidity:       data.humidity       || '',
    fertilization:  data.fertilization  || '',
    levels:         data.levels         || null,
    notes:          data.notes          || '',
    tags:           data.tags           || [],
  }
}

async function save() {
  if (!form.value.common_name) return
  saving.value = true
  error.value = ''

  try {
    const payload = {
      common_name:     form.value.common_name,
      scientific_name: form.value.scientific_name || null,
      emoji:           form.value.emoji,
      watering:        form.value.watering        || null,
      light:           form.value.light           || null,
      temperature:     form.value.temperature     || null,
      humidity:        form.value.humidity        || null,
      fertilization:   form.value.fertilization   || null,
      levels:          form.value.levels          || null,
      notes:           form.value.notes           || null,
      tags:            form.value.tags,
    }

    let saved
    if (isEdit.value) {
      saved = await store.update(props.plant.id, payload)
    } else {
      saved = await store.create(payload)
    }

    if (pendingFile.value) {
      await store.uploadPhoto(saved.id, pendingFile.value)
    }

    emit('saved', saved)
    close()
  } catch (e) {
    error.value = e.response?.data?.detail || 'Une erreur est survenue'
  } finally {
    saving.value = false
  }
}

function close() {
  emit('update:modelValue', false)
}
</script>

<style scoped>
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  z-index: 1500;
  display: flex;
  align-items: flex-start;
  justify-content: flex-end;
  backdrop-filter: blur(4px);
  animation: fadeIn 0.2s ease;
}

.panel {
  background: var(--color-surface);
  border-left: 1px solid var(--color-border-strong);
  width: 100%;
  max-width: 560px;
  height: 100vh;
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
  margin-bottom: 12px;
}

.eyebrow {
  font-family: var(--font-label);
  font-size: 10px;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  color: var(--color-accent);
  opacity: 0.7;
}

.panel-title {
  font-family: var(--font-display);
  font-size: 28px;
  font-weight: 700;
  color: var(--color-text);
  letter-spacing: -0.02em;
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.ai-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-family: var(--font-label);
  font-size: 10px;
  font-weight: 400;
  letter-spacing: 0.15em;
  color: var(--color-accent);
  opacity: 0.8;
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

/* ── Body ── */
.panel-body {
  padding: 28px 36px;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 28px;
}

.form-section {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.section-label {
  font-family: var(--font-label);
  font-size: 9px;
  letter-spacing: 0.3em;
  text-transform: uppercase;
  color: var(--color-accent);
  opacity: 0.6;
}

.section-hint {
  font-family: var(--font-label);
  font-size: 11px;
  color: var(--color-text-muted);
  margin-top: -6px;
}

.form-divider {
  height: 1px;
  background: var(--color-border);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-field--wide {
  grid-column: 1 / -1;
}

label {
  font-family: var(--font-label);
  font-size: 9px;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--color-text-muted);
}

input, textarea {
  font-family: var(--font-label);
  font-size: 13px;
  color: var(--color-text);
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: 2px;
  padding: 10px 12px;
  outline: none;
  transition: border-color 0.2s;
  width: 100%;
}
input:focus, textarea:focus {
  border-color: var(--color-accent);
}
textarea { resize: vertical; }

input::placeholder, textarea::placeholder {
  color: var(--color-text-dim);
}

/* ── Emoji picker ── */
.emoji-picker {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.emoji-btn {
  font-size: 20px;
  width: 36px;
  height: 36px;
  border-radius: 4px;
  border: 1px solid transparent;
  background: transparent;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s;
}
.emoji-btn:hover, .emoji-btn.active {
  background: var(--color-accent-dim);
  border-color: var(--color-border-strong);
}

/* ── Niveaux ── */
.levels-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.level-row {
  display: grid;
  grid-template-columns: 20px 90px 1fr auto;
  align-items: center;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px solid var(--color-border);
}

.level-icon {
  color: var(--color-accent);
  opacity: 0.85;
}

.level-label {
  font-family: var(--font-label);
  font-size: 10px;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--color-text-muted);
}

.level-btns {
  display: flex;
  gap: 5px;
}

.level-btn {
  width: 28px;
  height: 6px;
  border: none;
  border-radius: 1px;
  background: var(--color-text-dim);
  opacity: 0.3;
  cursor: pointer;
  transition: background 0.15s, opacity 0.15s;
  padding: 0;
}
.level-btn.active {
  background: var(--color-accent);
  opacity: 1;
}
.level-btn:hover {
  opacity: 0.7;
}

.level-val {
  font-family: var(--font-label);
  font-size: 10px;
  letter-spacing: 0.1em;
  color: var(--color-accent);
  min-width: 28px;
  text-align: right;
}

/* ── Photo ── */
.current-photo-row {
  display: flex;
  align-items: center;
  gap: 16px;
}

.current-photo {
  width: 72px;
  height: 72px;
  object-fit: cover;
  border-radius: 2px;
  border: 1px solid var(--color-border);
}

/* ── Footer ── */
.panel-footer {
  padding: 20px 36px;
  border-top: 1px solid var(--color-border);
  position: sticky;
  bottom: 0;
  background: var(--color-surface);
}

.form-error {
  font-family: var(--font-label);
  font-size: 11px;
  color: var(--color-warn);
  margin-bottom: 12px;
}

.footer-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

@media (max-width: 600px) {
  .panel { max-width: 100%; }
  .panel-header, .panel-body, .panel-footer { padding-left: 20px; padding-right: 20px; }
  .form-row { grid-template-columns: 1fr; }
  .level-row { grid-template-columns: 20px 1fr; grid-template-rows: auto auto; }
  .level-btns { grid-column: 1 / -1; }
  .level-val { display: none; }
}
</style>
