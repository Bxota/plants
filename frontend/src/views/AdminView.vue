<template>
  <div>
    <header class="site-header">
      <div class="header-left">
        <p class="label">Administration</p>
        <h1>Gestion<br /><em>des users</em></h1>
      </div>
      <div class="header-right">
        <RouterLink to="/" class="btn btn-ghost">← Retour</RouterLink>
      </div>
    </header>

    <div class="admin-body">
      <!-- Liste des utilisateurs -->
      <section class="section">
        <p class="section-label">Utilisateurs ({{ users.length }})</p>

        <div class="users-list">
          <div v-for="u in users" :key="u.id" class="user-row">
            <div class="user-info">
              <span class="user-name">{{ u.username }}</span>
              <span v-if="u.is_admin" class="badge-admin">admin</span>
            </div>
            <button
              v-if="u.id !== auth.user?.id"
              class="btn btn-danger btn-sm"
              :disabled="deleting === u.id"
              @click="deleteUser(u)"
            >
              {{ deleting === u.id ? '…' : 'Supprimer' }}
            </button>
            <span v-else class="self-label">vous</span>
          </div>
        </div>
      </section>

      <div class="section-divider"></div>

      <!-- Formulaire ajout -->
      <section class="section">
        <p class="section-label">Ajouter un utilisateur</p>

        <form class="add-form" @submit.prevent="createUser">
          <div class="form-row">
            <div class="form-field">
              <label>Identifiant</label>
              <input v-model="newUser.username" type="text" placeholder="marie" required />
            </div>
            <div class="form-field">
              <label>Mot de passe</label>
              <input v-model="newUser.password" type="password" placeholder="••••••••" required />
            </div>
          </div>
          <div class="form-field checkbox-field">
            <label class="checkbox-label">
              <input v-model="newUser.is_admin" type="checkbox" />
              <span>Rôle admin</span>
            </label>
          </div>

          <p v-if="createError" class="form-error">{{ createError }}</p>

          <button type="submit" class="btn btn-primary" :disabled="creating">
            {{ creating ? 'Création…' : 'Créer le compte' }}
          </button>
        </form>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import client from '@/api/client'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const users = ref([])
const deleting = ref(null)
const creating = ref(false)
const createError = ref('')

const newUser = ref({ username: '', password: '', is_admin: false })

onMounted(fetchUsers)

async function fetchUsers() {
  const res = await client.get('/api/admin/users')
  users.value = res.data
}

async function createUser() {
  creating.value = true
  createError.value = ''
  try {
    await client.post('/api/admin/users', newUser.value)
    newUser.value = { username: '', password: '', is_admin: false }
    await fetchUsers()
  } catch (e) {
    createError.value = e.response?.data?.detail || 'Erreur lors de la création'
  } finally {
    creating.value = false
  }
}

async function deleteUser(u) {
  if (!confirm(`Supprimer « ${u.username} » et toutes ses plantes ?`)) return
  deleting.value = u.id
  try {
    await client.delete(`/api/admin/users/${u.id}`)
    await fetchUsers()
  } finally {
    deleting.value = null
  }
}
</script>

<style scoped>
.site-header {
  padding: 80px 60px 40px;
  border-bottom: 1px solid var(--green-light);
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 40px;
  flex-wrap: wrap;
  animation: fadeUp 0.9s ease both;
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
  font-size: clamp(40px, 6vw, 72px);
  line-height: 0.9;
  color: var(--green-deep);
  font-weight: 400;
}

h1 em { font-style: italic; color: var(--ochre); }

.admin-body {
  max-width: 640px;
  margin: 0 auto;
  padding: 60px 40px;
  display: flex;
  flex-direction: column;
  gap: 40px;
  animation: fadeUp 0.6s ease;
}

.section-label {
  font-size: 9px;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  color: var(--green-mid);
  margin-bottom: 20px;
}

.section-divider {
  height: 1px;
  background: var(--green-pale);
}

/* Users list */
.users-list {
  display: flex;
  flex-direction: column;
  gap: 0;
  border: 1px solid var(--green-light);
}

.user-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid var(--green-pale);
}
.user-row:last-child { border-bottom: none; }

.user-info { display: flex; align-items: center; gap: 10px; }

.user-name {
  font-size: 13px;
  color: var(--dark);
}

.badge-admin {
  font-size: 9px;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  padding: 3px 8px;
  border: 1px solid var(--ochre);
  color: var(--ochre);
  border-radius: 100px;
}

.self-label {
  font-size: 10px;
  color: var(--green-light);
  letter-spacing: 0.1em;
}

.btn-sm { padding: 8px 14px; font-size: 10px; }

/* Add form */
.add-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
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

label {
  font-size: 10px;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--green-mid);
}

input[type="text"],
input[type="password"] {
  font-family: 'DM Mono', monospace;
  font-size: 12px;
  color: var(--dark);
  background: var(--cream);
  border: 1px solid var(--green-light);
  border-radius: 4px;
  padding: 10px 12px;
  outline: none;
  transition: border-color 0.2s;
}
input:focus { border-color: var(--green-mid); }

.checkbox-field { flex-direction: row; align-items: center; }
.checkbox-label {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  font-size: 12px;
  color: var(--dark);
  text-transform: none;
  letter-spacing: 0;
}
.checkbox-label input { width: auto; }

.form-error {
  font-size: 11px;
  color: var(--rust);
}

@media (max-width: 720px) {
  .site-header { padding: 48px 32px 32px; }
  .admin-body { padding: 40px 24px; }
  .form-row { grid-template-columns: 1fr; }
}
</style>
