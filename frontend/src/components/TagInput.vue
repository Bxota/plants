<template>
  <div class="tag-input">
    <div class="tags-list">
      <span v-for="tag in modelValue" :key="tag" class="tag-pill">
        {{ tag }}
        <button type="button" class="tag-remove" @click="removeTag(tag)">×</button>
      </span>
    </div>
    <input
      v-model="inputValue"
      type="text"
      class="tag-field"
      placeholder="Ajouter un tag, appuyer sur Entrée"
      @keydown.enter.prevent="addTag"
      @keydown.comma.prevent="addTag"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  modelValue: { type: Array, default: () => [] },
})
const emit = defineEmits(['update:modelValue'])

const inputValue = ref('')

function addTag() {
  const tag = inputValue.value.trim().replace(/,$/, '')
  if (tag && !props.modelValue.includes(tag)) {
    emit('update:modelValue', [...props.modelValue, tag])
  }
  inputValue.value = ''
}

function removeTag(tag) {
  emit('update:modelValue', props.modelValue.filter((t) => t !== tag))
}
</script>

<style scoped>
.tag-input {
  border: 1px solid var(--green-light);
  border-radius: 4px;
  padding: 8px 12px;
  background: var(--cream);
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
}

.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.tag-pill {
  font-size: 10px;
  letter-spacing: 0.1em;
  padding: 4px 10px;
  background: var(--green-pale);
  color: var(--green-deep);
  border-radius: 100px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.tag-remove {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--green-mid);
  font-size: 14px;
  line-height: 1;
  padding: 0;
}

.tag-field {
  border: none;
  outline: none;
  background: transparent;
  font-family: 'DM Mono', monospace;
  font-size: 12px;
  color: var(--dark);
  min-width: 200px;
  flex: 1;
}

.tag-field::placeholder {
  color: var(--green-light);
}
</style>
