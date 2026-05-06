<template>
  <div class="home">

    <!-- Header -->
    <header class="site-header">
      <div class="header-left">
        <p class="eyebrow">Herbier personnel · {{ currentYear }}</p>
        <h1 class="headline">
          Mes <span class="accent">plantes</span>
        </h1>
        <p class="subline">
          {{ plants.length }} espèce{{ plants.length !== 1 ? 's' : '' }} · besoins normalisés sur 5 niveaux
        </p>
      </div>

      <div class="header-right">
        <!-- Toggle grille / liste -->
        <div class="view-toggle">
          <button
            v-for="[v, ic, lbl] in viewOptions"
            :key="v"
            class="toggle-btn"
            :class="{ active: theme.view === v }"
            @click="theme.view = v"
          >
            <Icon :name="ic" :size="12" />
            {{ lbl }}
          </button>
        </div>

        <!-- Actions -->
        <div class="header-actions">
          <button class="btn btn-primary" @click="openAdd">
            <Icon name="plus" :size="14" />
            Ajouter
          </button>
          <!-- Toggle thème jour/nuit -->
          <button class="btn btn-ghost" :title="theme.theme === 'dark' ? 'Passer en mode jour' : 'Passer en mode nuit'" @click="theme.theme = theme.theme === 'dark' ? 'light' : 'dark'">
            <Icon :name="theme.theme === 'dark' ? 'sun' : 'moon'" :size="14" />
          </button>
          <RouterLink v-if="auth.isAdmin" to="/admin" class="btn btn-ghost" title="Administration">
            <Icon name="user" :size="14" />
          </RouterLink>
          <button class="btn btn-ghost" title="Se déconnecter" @click="logout">
            <Icon name="logout" :size="14" />
          </button>
        </div>
      </div>
    </header>

    <!-- États loading / vide -->
    <div v-if="store.loading" class="loading-state">
      <AiLoader />
    </div>

    <div v-else-if="plants.length === 0" class="empty-state">
      <p class="empty-icon">🌱</p>
      <p class="empty-text">Votre herbier est vide</p>
      <button class="btn btn-primary" @click="openAdd">Ajouter ma première plante</button>
    </div>

    <template v-else>
      <!-- Vue grille -->
      <div v-if="theme.view === 'grid'" class="plants-grid" :style="gridStyle">
        <PlantCard
          v-for="(plant, index) in plants"
          :key="plant.id"
          :plant="plant"
          :index="index"
          :care-style="theme.careStyle"
          :condition-tags="theme.conditionTags"
          @select="selectedPlant = $event"
          @edit="openEdit(plant)"
          @delete="confirmDelete(plant)"
        />
      </div>

      <!-- Vue liste -->
      <div v-else class="plants-list">
        <!-- En-tête colonnes -->
        <div class="list-header">
          <div v-for="(h, i) in listHeaders" :key="i" class="list-header-cell" :class="{ right: i === 4 }">
            {{ h }}
          </div>
        </div>

        <PlantRow
          v-for="(plant, index) in plants"
          :key="plant.id"
          :plant="plant"
          :index="index"
          :care-style="theme.careStyle"
          :condition-tags="theme.conditionTags"
          @select="selectedPlant = $event"
          @edit="openEdit(plant)"
          @delete="confirmDelete(plant)"
        />
      </div>
    </template>

    <!-- Footer -->
    <footer v-if="plants.length > 0" class="site-footer">
      <div>
        <span class="footer-count">{{ plants.length }}</span>
        <p class="footer-label">PLANTES RECENSÉES</p>
      </div>
      <p class="footer-label">HERBIER · {{ currentYear }}</p>
    </footer>

    <!-- Panel détail plante -->
    <DetailPanel
      v-if="selectedPlant"
      :plant="selectedPlant"
      :care-style="theme.careStyle"
      @close="selectedPlant = null"
      @edit="openEdit(selectedPlant); selectedPlant = null"
      @delete="confirmDelete(selectedPlant); selectedPlant = null"
    />

    <!-- Modal ajout/édition -->
    <PlantForm v-model="showForm" :plant="editingPlant" @saved="store.fetchAll()" />

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
import { useAuthStore }   from '@/stores/auth'
import { usePlantsStore } from '@/stores/plants'
import { useThemeStore }  from '@/stores/theme'
import PlantCard      from '@/components/PlantCard.vue'
import PlantRow       from '@/components/PlantRow.vue'
import PlantForm      from '@/components/PlantForm.vue'
import ConfirmDialog  from '@/components/ConfirmDialog.vue'
import DetailPanel    from '@/components/DetailPanel.vue'
import AiLoader       from '@/components/AiLoader.vue'
import Icon           from '@/components/Icon.vue'

const router = useRouter()
const auth   = useAuthStore()
const store  = usePlantsStore()
const theme  = useThemeStore()

const plants      = computed(() => store.plants)
const currentYear = new Date().getFullYear()

const selectedPlant = ref(null)
const showForm      = ref(false)
const editingPlant  = ref(null)
const showConfirm   = ref(false)
const deletingPlant = ref(null)

onMounted(() => store.fetchAll())

const viewOptions  = [['grid', 'grid', 'Grille'], ['list', 'list', 'Liste']]
const listHeaders  = ['№', 'Nom', 'Eau · Lumière · Temp · Humidité · Fert.', 'Conditions', '']

const gridCols = computed(() => ({
  compact: 'repeat(auto-fill, minmax(280px, 1fr))',
  normal:  'repeat(auto-fill, minmax(320px, 1fr))',
  airy:    'repeat(auto-fill, minmax(380px, 1fr))',
}[theme.density] ?? 'repeat(auto-fill, minmax(320px, 1fr))'))

const gridStyle = computed(() => ({ gridTemplateColumns: gridCols.value }))

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
/* ── Header ── */
.site-header {
  padding: 60px 60px 36px;
  border-bottom: 1px solid var(--color-border);
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 40px;
  flex-wrap: wrap;
  animation: fadeUp 0.6s ease both;
}

.eyebrow {
  font-family: var(--font-label);
  font-size: 10px;
  letter-spacing: 0.3em;
  text-transform: uppercase;
  color: var(--color-accent);
  opacity: 0.7;
  margin-bottom: 14px;
}

.headline {
  font-family: var(--font-display);
  font-size: clamp(48px, 7vw, 88px);
  font-weight: 800;
  color: var(--color-text);
  line-height: 0.95;
  letter-spacing: -0.04em;
  margin-bottom: 14px;
}

.accent {
  color: var(--color-accent);
}

.subline {
  font-family: var(--font-label);
  font-size: 12px;
  color: var(--color-text-muted);
  line-height: 1.6;
  max-width: 420px;
}

.header-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 16px;
}

/* View toggle */
.view-toggle {
  display: inline-flex;
  border: 1px solid var(--color-border);
  border-radius: 3px;
  padding: 3px;
  gap: 2px;
}

.toggle-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 7px 12px;
  border-radius: 2px;
  border: none;
  font-family: var(--font-label);
  font-size: 10px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  cursor: pointer;
  background: transparent;
  color: var(--color-text-muted);
  font-weight: 400;
  transition: background 0.2s, color 0.2s;
}

.toggle-btn.active {
  background: var(--color-accent);
  color: var(--color-bg);
  font-weight: 600;
}

.header-actions {
  display: flex;
  gap: 8px;
  align-items: center;
}

/* ── Grid ── */
.plants-grid {
  display: grid;
  gap: 16px;
  padding: 32px 60px;
  animation: fadeUp 0.5s ease both;
}

/* ── List ── */
.plants-list {
  animation: fadeUp 0.4s ease both;
}

.list-header {
  display: grid;
  grid-template-columns: 60px minmax(180px, 1.6fr) minmax(280px, 2fr) minmax(180px, 1.4fr) 80px;
  gap: 24px;
  padding: 16px 32px;
  border-bottom: 1px solid var(--color-border);
  background: var(--color-surface);
}

.list-header-cell {
  font-family: var(--font-label);
  font-size: 9px;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--color-text-muted);
}
.list-header-cell.right {
  text-align: right;
}

/* ── États ── */
.loading-state {
  padding: 80px 0;
}

.empty-state {
  text-align: center;
  padding: 120px 40px;
  animation: fadeUp 0.6s ease both;
}

.empty-icon {
  font-size: 56px;
  margin-bottom: 20px;
}

.empty-text {
  font-family: var(--font-display);
  font-size: 24px;
  font-weight: 600;
  color: var(--color-text);
  margin-bottom: 32px;
}

/* ── Footer ── */
.site-footer {
  padding: 32px 60px;
  border-top: 1px solid var(--color-border);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
}

.footer-count {
  font-family: var(--font-display);
  font-size: 36px;
  font-weight: 700;
  color: var(--color-accent);
  letter-spacing: -0.02em;
  display: block;
}

.footer-label {
  font-family: var(--font-label);
  font-size: 10px;
  letter-spacing: 0.2em;
  color: var(--color-text-dim);
  margin-top: 2px;
}

@media (max-width: 720px) {
  .site-header   { padding: 48px 24px 28px; }
  .header-right  { width: 100%; align-items: stretch; }
  .view-toggle   { width: 100%; justify-content: space-between; }
  .header-actions { width: 100%; flex-wrap: wrap; }
  .header-actions .btn,
  .header-actions .btn-ghost { flex: 1 1 auto; justify-content: center; }
  .plants-grid   { padding: 20px 16px; }
  .site-footer   { padding: 24px; }
  .list-header   { display: none; }
}
</style>
