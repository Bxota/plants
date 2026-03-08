<template>
  <Teleport to="body">
    <div v-if="modelValue" class="overlay" @click.self="close">
      <div class="modal">
        <!-- Header -->
        <div class="modal-header">
          <div>
            <p class="modal-label">{{ isEdit ? 'Modifier la plante' : 'Nouvelle plante' }}</p>
            <h2 class="modal-title">
              {{ isEdit ? plant?.common_name : 'Ajouter' }}
              <em v-if="aiPrefilled"> ✦ Identifié par IA</em>
            </h2>
          </div>
          <button class="close-btn" @click="close">✕</button>
        </div>

        <div class="modal-body">
          <!-- Photo upload (uniquement en mode création ou si pas encore de photo) -->
          <div v-if="!isEdit || !form.photo_url" class="form-section">
            <p class="section-label">Photo</p>
            <PhotoUpload ref="photoUploadRef" @identified="onIdentified" @file-selected="pendingFile = $event" />
          </div>

          <!-- Photo existante en mode édition -->
          <div v-if="isEdit && form.photo_url" class="form-section">
            <p class="section-label">Photo actuelle</p>
            <div class="current-photo-row">
              <img :src="form.photo_url" alt="Photo" class="current-photo" />
              <button type="button" class="btn btn-ghost" @click="form.photo_url = null">Changer la photo</button>
            </div>
            <PhotoUpload v-if="!form.photo_url" ref="photoUploadRef" @identified="onIdentified" @file-selected="pendingFile = $event" />
          </div>

          <div class="form-divider"></div>

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

          <!-- Soins -->
          <div class="form-section">
            <p class="section-label">Conseils de soin</p>
            <div class="form-row">
              <div class="form-field">
                <label>💧 Arrosage</label>
                <input v-model="form.watering" type="text" placeholder="Tous les 15 jours…" />
              </div>
              <div class="form-field">
                <label>☀️ Lumière</label>
                <input v-model="form.light" type="text" placeholder="Lumière vive indirecte…" />
              </div>
              <div class="form-field">
                <label>🌡️ Température</label>
                <input v-model="form.temperature" type="text" placeholder="18 – 24 °C" />
              </div>
              <div class="form-field">
                <label>💦 Humidité</label>
                <input v-model="form.humidity" type="text" placeholder="Élevée…" />
              </div>
              <div class="form-field form-field--wide">
                <label>🌱 Fertilisation</label>
                <input v-model="form.fertilization" type="text" placeholder="Printemps–été, tous les 15 jours…" />
              </div>
            </div>
          </div>

          <!-- Notes & Tags -->
          <div class="form-section">
            <p class="section-label">Notes & Tags</p>
            <div class="form-field">
              <label>Note</label>
              <textarea v-model="form.notes" rows="3" placeholder="Particularité botanique, conseil important…"></textarea>
            </div>
            <div class="form-field">
              <label>Tags</label>
              <TagInput v-model="form.tags" />
            </div>
          </div>
        </div>

        <!-- Footer -->
        <div class="modal-footer">
          <p v-if="error" class="form-error">{{ error }}</p>
          <div class="footer-actions">
            <button type="button" class="btn btn-ghost" @click="close">Annuler</button>
            <button type="button" class="btn btn-primary" :disabled="saving || !form.common_name" @click="save">
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
import { usePlantsStore } from '@/stores/plants'

const props = defineProps({
  modelValue: Boolean,
  plant: { type: Object, default: null }, // null = création
})
const emit = defineEmits(['update:modelValue', 'saved'])

const store = usePlantsStore()
const isEdit = computed(() => !!props.plant?.id)
const aiPrefilled = ref(false)
const pendingFile = ref(null)
const saving = ref(false)
const error = ref('')
const photoUploadRef = ref(null)

const EMOJIS = ['🌿', '🌱', '🌵', '🌴', '🌺', '🌸', '🌼', '🍃', '🎋', '🪴', '☕']

const defaultForm = () => ({
  common_name: '',
  scientific_name: '',
  emoji: '🌿',
  watering: '',
  light: '',
  temperature: '',
  humidity: '',
  fertilization: '',
  notes: '',
  tags: [],
  photo_url: null,
})

const form = ref(defaultForm())

watch(
  () => props.modelValue,
  (open) => {
    if (open) {
      aiPrefilled.value = false
      pendingFile.value = null
      error.value = ''
      if (props.plant) {
        form.value = { ...defaultForm(), ...props.plant }
      } else {
        form.value = defaultForm()
      }
    }
  }
)

function onIdentified({ data, file }) {
  pendingFile.value = file
  aiPrefilled.value = true
  form.value = {
    ...form.value,
    common_name: data.common_name || form.value.common_name,
    scientific_name: data.scientific_name || '',
    emoji: data.emoji || '🌿',
    watering: data.watering || '',
    light: data.light || '',
    temperature: data.temperature || '',
    humidity: data.humidity || '',
    fertilization: data.fertilization || '',
    notes: data.notes || '',
    tags: data.tags || [],
  }
}

async function save() {
  if (!form.value.common_name) return
  saving.value = true
  error.value = ''

  try {
    const payload = {
      common_name: form.value.common_name,
      scientific_name: form.value.scientific_name || null,
      emoji: form.value.emoji,
      watering: form.value.watering || null,
      light: form.value.light || null,
      temperature: form.value.temperature || null,
      humidity: form.value.humidity || null,
      fertilization: form.value.fertilization || null,
      notes: form.value.notes || null,
      tags: form.value.tags,
    }

    let saved
    if (isEdit.value) {
      saved = await store.update(props.plant.id, payload)
    } else {
      saved = await store.create(payload)
    }

    // Upload de la photo si une nouvelle a été sélectionnée
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
  background: rgba(26, 26, 20, 0.6);
  z-index: 1500;
  display: flex;
  align-items: flex-start;
  justify-content: flex-end;
  backdrop-filter: blur(2px);
}

.modal {
  background: var(--cream);
  width: 100%;
  max-width: 560px;
  height: 100vh;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from { transform: translateX(100%); }
  to { transform: translateX(0); }
}

/* Header */
.modal-header {
  padding: 40px 40px 24px;
  border-bottom: 1px solid var(--green-light);
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  position: sticky;
  top: 0;
  background: var(--cream);
  z-index: 10;
}

.modal-label {
  font-size: 10px;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--green-mid);
  margin-bottom: 8px;
}

.modal-title {
  font-family: 'Playfair Display', serif;
  font-size: 26px;
  font-weight: 400;
  color: var(--green-deep);
}

.modal-title em {
  font-size: 14px;
  color: var(--ochre);
  font-style: normal;
}

.close-btn {
  background: none;
  border: none;
  font-size: 18px;
  color: var(--green-light);
  cursor: pointer;
  padding: 4px;
  transition: color 0.2s;
}
.close-btn:hover { color: var(--dark); }

/* Body */
.modal-body {
  padding: 32px 40px;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.form-section {}

.section-label {
  font-size: 9px;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  color: var(--green-mid);
  margin-bottom: 16px;
}

.form-divider {
  height: 1px;
  background: var(--green-pale);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
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
  font-size: 10px;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--green-mid);
}

input, textarea {
  font-family: 'DM Mono', monospace;
  font-size: 12px;
  color: var(--dark);
  background: var(--cream);
  border: 1px solid var(--green-light);
  border-radius: 4px;
  padding: 10px 12px;
  outline: none;
  transition: border-color 0.2s;
  width: 100%;
}

input:focus, textarea:focus {
  border-color: var(--green-mid);
}

textarea {
  resize: vertical;
}

/* Emoji picker */
.emoji-picker {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.emoji-btn {
  font-size: 20px;
  width: 36px;
  height: 36px;
  border-radius: 6px;
  border: 1px solid transparent;
  background: transparent;
  cursor: pointer;
  transition: all 0.15s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.emoji-btn:hover, .emoji-btn.active {
  background: var(--green-pale);
  border-color: var(--green-light);
}

/* Current photo */
.current-photo-row {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 12px;
}

.current-photo {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 6px;
  border: 1px solid var(--green-light);
}

/* Footer */
.modal-footer {
  padding: 24px 40px;
  border-top: 1px solid var(--green-light);
  position: sticky;
  bottom: 0;
  background: var(--cream);
}

.form-error {
  font-size: 11px;
  color: var(--rust);
  margin-bottom: 12px;
}

.footer-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@media (max-width: 720px) {
  .modal { max-width: 100%; }
  .modal-header, .modal-body, .modal-footer { padding-left: 24px; padding-right: 24px; }
  .form-row { grid-template-columns: 1fr; }
}
</style>
