<template>
  <div class="login-page">
    <div class="login-card">
      <div class="login-header">
        <p class="label">Accès privé</p>
        <h1>Mes<br /><em>Plantes</em></h1>
      </div>

      <form class="login-form" @submit.prevent="submit">
        <div class="form-field">
          <label>Identifiant</label>
          <input
            v-model="username"
            type="text"
            autocomplete="username"
            placeholder="thomas"
            required
          />
        </div>
        <div class="form-field">
          <label>Mot de passe</label>
          <input
            v-model="password"
            type="password"
            autocomplete="current-password"
            placeholder="••••••••"
            required
          />
        </div>

        <p v-if="error" class="login-error">{{ error }}</p>

        <button type="submit" class="btn btn-primary btn-block" :disabled="loading">
          {{ loading ? 'Connexion…' : 'Se connecter' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function submit() {
  error.value = ''
  loading.value = true
  try {
    await auth.login(username.value, password.value)
    router.push('/')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Identifiants incorrects'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 24px;
  animation: fadeUp 0.7s ease;
}

.login-card {
  width: 100%;
  max-width: 400px;
  border: 1px solid var(--green-light);
  padding: 56px 48px;
}

.login-header {
  margin-bottom: 48px;
}

.label {
  font-size: 10px;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  color: var(--green-mid);
  margin-bottom: 12px;
}

h1 {
  font-family: 'Playfair Display', serif;
  font-size: 52px;
  line-height: 0.9;
  color: var(--green-deep);
  font-weight: 400;
}

h1 em {
  font-style: italic;
  color: var(--ochre);
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

label {
  font-size: 10px;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--green-mid);
}

input {
  font-family: 'DM Mono', monospace;
  font-size: 13px;
  color: var(--dark);
  background: var(--cream);
  border: 1px solid var(--green-light);
  border-radius: 4px;
  padding: 12px 16px;
  outline: none;
  transition: border-color 0.2s;
}

input:focus {
  border-color: var(--green-mid);
}

.login-error {
  font-size: 11px;
  color: var(--rust);
}

.btn-block {
  width: 100%;
  padding: 14px;
  text-align: center;
}
</style>
