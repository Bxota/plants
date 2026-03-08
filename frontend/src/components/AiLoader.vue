<template>
  <div class="ai-loader">
    <div class="loader-icon">{{ currentEmoji }}</div>
    <p class="loader-text">{{ currentPhrase }}</p>
    <div class="loader-dots">
      <span></span><span></span><span></span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const EMOJIS = ['🌿', '🌱', '🍃', '🌺', '🪴']
const PHRASES = [
  'Identification en cours…',
  'Analyse botanique…',
  'Consultation de l\'herbier…',
  'Reconnaissance de l\'espèce…',
  'Préparation des conseils de soin…',
]

const currentEmoji = ref(EMOJIS[0])
const currentPhrase = ref(PHRASES[0])
let interval = null
let i = 0

onMounted(() => {
  interval = setInterval(() => {
    i = (i + 1) % PHRASES.length
    currentEmoji.value = EMOJIS[i % EMOJIS.length]
    currentPhrase.value = PHRASES[i]
  }, 1200)
})

onUnmounted(() => clearInterval(interval))
</script>

<style scoped>
.ai-loader {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 48px 24px;
}

.loader-icon {
  font-size: 48px;
  animation: spin 2s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg) scale(1); }
  50% { transform: rotate(15deg) scale(1.1); }
  100% { transform: rotate(0deg) scale(1); }
}

.loader-text {
  font-size: 13px;
  color: var(--green-mid);
  letter-spacing: 0.05em;
  text-align: center;
}

.loader-dots {
  display: flex;
  gap: 6px;
}

.loader-dots span {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--green-light);
  animation: bounce 1.2s infinite ease-in-out;
}

.loader-dots span:nth-child(2) { animation-delay: 0.2s; }
.loader-dots span:nth-child(3) { animation-delay: 0.4s; }

@keyframes bounce {
  0%, 80%, 100% { transform: translateY(0); opacity: 0.4; }
  40% { transform: translateY(-8px); opacity: 1; }
}
</style>
