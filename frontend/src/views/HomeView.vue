<template>
  <div>
    <!-- Header -->
    <header class="site-header">
      <div class="header-left">
        <p class="label">Herbier personnel</p>
        <h1>Mes<br /><em>Plantes</em></h1>
      </div>
      <div class="header-right">
        <div class="header-meta">
          <p>{{ plants.length }} espèce{{ plants.length !== 1 ? 's' : '' }} recensée{{ plants.length !== 1 ? 's' : '' }}</p>
          <p>Mise à jour · {{ currentYear }}</p>
        </div>
        <div class="header-actions">
          <button class="btn btn-primary" @click="openAdd">+ Ajouter</button>
          <RouterLink v-if="auth.isAdmin" to="/admin" class="btn btn-ghost" title="Administration">⚙</RouterLink>
          <button class="btn btn-ghost btn-logout" @click="logout" title="Se déconnecter">⏻</button>
        </div>
      </div>
    </header>

    <!-- Grille -->
    <div v-if="store.loading" class="loading-state">
      <AiLoader />
    </div>

    <div v-else-if="plants.length === 0" class="empty-state">
      <p class="empty-icon">🌱</p>
      <p class="empty-text">Votre herbier est vide</p>
      <button class="btn btn-primary" @click="openAdd">Ajouter ma première plante</button>
    </div>

    <div v-else class="plants-grid">
      <PlantCard
        v-for="(plant, index) in plants"
        :key="plant.id"
        :plant="plant"
        :index="index"
        @edit="openEdit(plant)"
        @delete="confirmDelete(plant)"
      />
    </div>

    <!-- Footer -->
    <footer v-if="plants.length > 0" class="site-footer">
      <div>
        <span class="footer-count">{{ plants.length }}</span>
        <p style="margin-top:4px">plante{{ plants.length !== 1 ? 's' : '' }} recensée{{ plants.length !== 1 ? 's' : '' }}</p>
      </div>
      <p>Herbier · Mis à jour en {{ currentYear }}</p>
    </footer>

    <!-- Modal ajout/édition -->
    <PlantForm
      v-model="showForm"
      :plant="editingPlant"
      @saved="store.fetchAll()"
    />

    <!-- Dialog suppression -->
    <ConfirmDialog
      v-model="showConfirm"
      title="Supprimer la plante"
      :message="`Supprimer « ${deletingPlant?.common_name} » ? Cette action est irréversible.`"
      @confirm="doDelete"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { usePlantsStore } from '@/stores/plants'
import PlantCard from '@/components/PlantCard.vue'
import PlantForm from '@/components/PlantForm.vue'
import ConfirmDialog from '@/components/ConfirmDialog.vue'
import AiLoader from '@/components/AiLoader.vue'

const router = useRouter()
const auth = useAuthStore()
const store = usePlantsStore()

const plants = computed(() => store.plants)
const currentYear = new Date().getFullYear()

const showForm = ref(false)
const editingPlant = ref(null)
const showConfirm = ref(false)
const deletingPlant = ref(null)

onMounted(() => store.fetchAll())

function openAdd() {
  editingPlant.value = null
  showForm.value = true
}

function openEdit(plant) {
  editingPlant.value = plant
  showForm.value = true
}

function confirmDelete(plant) {
  deletingPlant.value = plant
  showConfirm.value = true
}

async function doDelete() {
  if (!deletingPlant.value) return
  await store.remove(deletingPlant.value.id)
  deletingPlant.value = null
}

function logout() {
  auth.logout()
  router.push('/login')
}
</script>

<style scoped>
/* Header */
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
  font-size: clamp(48px, 7vw, 96px);
  line-height: 0.9;
  color: var(--green-deep);
  font-weight: 400;
}

h1 em {
  font-style: italic;
  color: var(--ochre);
}

.header-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 16px;
}

.header-meta {
  text-align: right;
  font-size: 11px;
  color: var(--green-mid);
  line-height: 2;
}

.header-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.btn-logout {
  font-size: 16px;
  padding: 12px 14px;
}

/* Grid */
.plants-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
  gap: 0;
}

/* States */
.loading-state {
  padding: 80px 0;
}

.empty-state {
  text-align: center;
  padding: 120px 40px;
  animation: fadeUp 0.6s ease;
}

.empty-icon {
  font-size: 56px;
  margin-bottom: 20px;
}

.empty-text {
  font-family: 'Playfair Display', serif;
  font-size: 24px;
  color: var(--green-deep);
  font-style: italic;
  margin-bottom: 32px;
}

/* Footer */
.site-footer {
  padding: 40px 60px;
  border-top: 1px solid var(--green-light);
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 10px;
  color: var(--green-light);
  letter-spacing: 0.15em;
  flex-wrap: wrap;
  gap: 16px;
  animation: fadeUp 0.8s 0.6s ease both;
}

.footer-count {
  font-family: 'Playfair Display', serif;
  font-size: 36px;
  color: var(--green-deep);
  font-style: italic;
  display: block;
}

@media (max-width: 720px) {
  .site-header { padding: 48px 32px 32px; }
  .site-footer { padding: 32px; }
}
</style>
