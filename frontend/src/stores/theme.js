import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

function load(key, def) {
  return localStorage.getItem(key) ?? def
}

export const useThemeStore = defineStore('theme', () => {
  const theme       = ref(load('theme', 'dark'))
  const density     = ref(load('density', 'normal'))
  const view        = ref(load('view', 'grid'))
  const careStyle   = ref(load('careStyle', 'bars'))
  const conditionTags = ref(load('conditionTags', 'on'))

  watch(theme, val => {
    localStorage.setItem('theme', val)
    document.documentElement.classList.toggle('theme-light', val === 'light')
  }, { immediate: true })

  watch(density,      val => localStorage.setItem('density', val))
  watch(view,         val => localStorage.setItem('view', val))
  watch(careStyle,    val => localStorage.setItem('careStyle', val))
  watch(conditionTags, val => localStorage.setItem('conditionTags', val))

  return { theme, density, view, careStyle, conditionTags }
})
