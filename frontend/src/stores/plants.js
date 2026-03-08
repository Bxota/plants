import { defineStore } from 'pinia'
import { ref } from 'vue'
import client from '@/api/client'

export const usePlantsStore = defineStore('plants', () => {
  const plants = ref([])
  const loading = ref(false)

  async function fetchAll() {
    loading.value = true
    try {
      const res = await client.get('/api/plants')
      plants.value = res.data
    } finally {
      loading.value = false
    }
  }

  async function create(data) {
    const res = await client.post('/api/plants', data)
    plants.value.push(res.data)
    return res.data
  }

  async function update(id, data) {
    const res = await client.put(`/api/plants/${id}`, data)
    const idx = plants.value.findIndex((p) => p.id === id)
    if (idx !== -1) plants.value[idx] = res.data
    return res.data
  }

  async function remove(id) {
    // Optimistic remove
    const backup = [...plants.value]
    plants.value = plants.value.filter((p) => p.id !== id)
    try {
      await client.delete(`/api/plants/${id}`)
    } catch (e) {
      plants.value = backup
      throw e
    }
  }

  async function uploadPhoto(id, file) {
    const form = new FormData()
    form.append('photo', file)
    const res = await client.post(`/api/plants/${id}/photo`, form, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    const idx = plants.value.findIndex((p) => p.id === id)
    if (idx !== -1) plants.value[idx].photo_url = res.data.photo_url
    return res.data.photo_url
  }

  async function identify(file) {
    const form = new FormData()
    form.append('photo', file)
    const res = await client.post('/api/identify', form, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return res.data
  }

  return { plants, loading, fetchAll, create, update, remove, uploadPhoto, identify }
})
