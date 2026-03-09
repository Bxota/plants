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

      <!-- Invitations -->
      <section class="section">
        <p class="section-label">Invitations</p>

        <form class="invite-form" @submit.prevent="generateInvite">
          <div class="invite-input-row">
            <input
              v-model="inviteEmail"
              type="email"
              placeholder="marie@exemple.com (optionnel)"
            />
            <button type="submit" class="btn btn-primary btn-sm" :disabled="generatingInvite">
              {{ generatingInvite ? '…' : 'Envoyer' }}
            </button>
          </div>
          <p v-if="inviteError" class="form-error">{{ inviteError }}</p>
          <p v-if="inviteSent" class="invite-sent">{{ inviteSent }}</p>
        </form>

        <div v-if="invitations.length > 0" class="invites-list">
          <div v-for="inv in invitations" :key="inv.id" class="invite-row">
            <div class="invite-info">
              <span v-if="inv.used_at" class="badge-used">utilisée</span>
              <span v-else-if="isExpired(inv)" class="badge-expired">expirée</span>
              <span v-else class="badge-active">active</span>
              <span class="invite-target">{{ inv.invited_email || 'lien manuel' }}</span>
              <span class="invite-date">{{ formatDate(inv.created_at) }}</span>
            </div>
            <div class="invite-actions">
              <button
                v-if="!inv.used_at && !isExpired(inv)"
                class="btn btn-ghost btn-sm"
                @click="copyInviteLink(inv.token)"
              >
                Copier
              </button>
              <button
                class="btn btn-danger btn-sm"
                :disabled="revoking === inv.token"
                @click="revokeInvite(inv)"
              >
                {{ revoking === inv.token ? '…' : 'Supprimer' }}
              </button>
            </div>
          </div>
        </div>

        <p v-if="copiedToken" class="copy-confirm">Lien copié !</p>
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
const invitations = ref([])
const generatingInvite = ref(false)
const revoking = ref(null)
const copiedToken = ref(false)
const inviteEmail = ref('')
const inviteError = ref('')
const inviteSent = ref('')

onMounted(() => {
  fetchUsers()
  fetchInvitations()
})

async function fetchUsers() {
  const res = await client.get('/api/admin/users')
  users.value = res.data
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

async function fetchInvitations() {
  const res = await client.get('/api/admin/invitations')
  invitations.value = res.data
}

async function generateInvite() {
  inviteError.value = ''
  inviteSent.value = ''
  generatingInvite.value = true
  try {
    await client.post('/api/admin/invitations', { email: inviteEmail.value || null })
    inviteSent.value = inviteEmail.value
      ? `Invitation envoyée à ${inviteEmail.value}`
      : 'Lien généré — copiez-le dans la liste ci-dessous'
    inviteEmail.value = ''
    await fetchInvitations()
  } catch (e) {
    inviteError.value = e.response?.data?.detail || "Erreur lors de l'envoi"
  } finally {
    generatingInvite.value = false
  }
}

async function revokeInvite(inv) {
  revoking.value = inv.token
  try {
    await client.delete(`/api/admin/invitations/${inv.token}`)
    await fetchInvitations()
  } finally {
    revoking.value = null
  }
}

function copyInviteLink(token) {
  const url = `${window.location.origin}/invite/${token}`
  navigator.clipboard.writeText(url)
  copiedToken.value = true
  setTimeout(() => (copiedToken.value = false), 2000)
}

function isExpired(inv) {
  if (!inv.expires_at) return false
  return new Date(inv.expires_at) < new Date()
}

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('fr-FR', { day: 'numeric', month: 'short', year: 'numeric' })
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

.form-error {
  font-size: 11px;
  color: var(--rust);
}

/* Invitations */
.invite-form {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 24px;
}

.invite-input-row {
  display: flex;
  gap: 10px;
}

.invite-input-row input {
  flex: 1;
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
.invite-input-row input:focus { border-color: var(--green-mid); }

.invite-sent {
  font-size: 11px;
  color: var(--green-mid);
}

.empty-invites {
  font-size: 12px;
  color: var(--green-light);
  padding: 20px 0;
}

.invites-list {
  display: flex;
  flex-direction: column;
  border: 1px solid var(--green-light);
}

.invite-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 20px;
  border-bottom: 1px solid var(--green-pale);
  gap: 12px;
}
.invite-row:last-child { border-bottom: none; }

.invite-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.invite-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.badge-active {
  font-size: 9px;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  padding: 3px 8px;
  border: 1px solid var(--green-mid);
  color: var(--green-mid);
  border-radius: 100px;
}

.badge-used {
  font-size: 9px;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  padding: 3px 8px;
  border: 1px solid var(--green-light);
  color: var(--green-light);
  border-radius: 100px;
}

.badge-expired {
  font-size: 9px;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  padding: 3px 8px;
  border: 1px solid var(--rust);
  color: var(--rust);
  border-radius: 100px;
}

.invite-target {
  font-size: 12px;
  color: var(--dark);
  font-family: 'DM Mono', monospace;
}

.invite-date {
  font-size: 11px;
  color: var(--green-mid);
}

.copy-confirm {
  font-size: 11px;
  color: var(--green-mid);
  margin-top: 12px;
}

@media (max-width: 720px) {
  .site-header { padding: 48px 32px 32px; }
  .admin-body { padding: 40px 24px; }
  .form-row { grid-template-columns: 1fr; }
}
</style>
