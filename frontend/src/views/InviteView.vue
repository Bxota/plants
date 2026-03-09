<template>
  <div class="invite-page">
    <div class="invite-card">
      <div class="invite-header">
        <p class="label">Invitation</p>
        <h1>Créer<br /><em>un compte</em></h1>
      </div>

      <!-- Chargement / validation du token -->
      <div v-if="checking" class="state-msg">Vérification du lien…</div>

      <!-- Token invalide / expiré -->
      <div v-else-if="tokenError" class="state-msg error">{{ tokenError }}</div>

      <!-- Compte créé -->
      <div v-else-if="success" class="state-msg success">
        Compte créé ! <RouterLink to="/login">Se connecter →</RouterLink>
      </div>

      <!-- Formulaire -->
      <form v-else class="invite-form" @submit.prevent="submit">
        <div class="form-field">
          <label>Identifiant</label>
          <input
            v-model="username"
            type="text"
            autocomplete="username"
            placeholder="marie"
            required
          />
        </div>
        <div class="form-field">
          <label>Mot de passe</label>
          <input
            v-model="password"
            type="password"
            autocomplete="new-password"
            placeholder="••••••••"
            required
          />
        </div>

        <p v-if="error" class="form-error">{{ error }}</p>

        <button type="submit" class="btn btn-primary btn-block" :disabled="loading">
          {{ loading ? 'Création…' : 'Créer mon compte' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import client from '@/api/client'

const route = useRoute()
const token = route.params.token

const checking = ref(true)
const tokenError = ref('')
const success = ref(false)
const loading = ref(false)
const error = ref('')
const username = ref('')
const password = ref('')

onMounted(async () => {
  try {
    await client.get(`/api/invite/${token}`)
  } catch (e) {
    tokenError.value = e.response?.data?.detail || 'Lien invalide ou expiré'
  } finally {
    checking.value = false
  }
})

async function submit() {
  error.value = ''
  loading.value = true
  try {
    await client.post(`/api/invite/${token}`, {
      username: username.value,
      password: password.value,
    })
    success.value = true
  } catch (e) {
    error.value = e.response?.data?.detail || 'Erreur lors de la création du compte'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.invite-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 24px;
  animation: fadeUp 0.7s ease;
}

.invite-card {
  width: 100%;
  max-width: 400px;
  border: 1px solid var(--green-light);
  padding: 56px 48px;
}

.invite-header {
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

.invite-form {
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

.state-msg {
  font-size: 13px;
  color: var(--green-mid);
}

.state-msg.error {
  color: var(--rust);
}

.state-msg.success {
  color: var(--green-deep);
}

.state-msg.success a {
  color: var(--ochre);
  text-decoration: underline;
}

.form-error {
  font-size: 11px;
  color: var(--rust);
}

.btn-block {
  width: 100%;
  padding: 14px;
  text-align: center;
}
</style>
