import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  const isDark = ref<boolean>(false)

  // Initialize theme from localStorage or system preference
  function initTheme() {
    const savedTheme = localStorage.getItem('theme')
    if (savedTheme) {
      isDark.value = savedTheme === 'dark'
    } else {
      // Check system preference
      isDark.value = window.matchMedia('(prefers-color-scheme: dark)').matches
    }
  }

  function toggleTheme() {
    isDark.value = !isDark.value
    localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
  }

  function setTheme(dark: boolean) {
    isDark.value = dark
    localStorage.setItem('theme', dark ? 'dark' : 'light')
  }

  return {
    isDark,
    initTheme,
    toggleTheme,
    setTheme,
  }
})
