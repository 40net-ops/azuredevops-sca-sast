<template>
  <v-app>
    <v-app-bar elevation="2" color="primary">
      <v-app-bar-title class="text-h6">
        <v-icon icon="mdi-calculator" class="mr-2" />
        Computer Unit Converter
      </v-app-bar-title>

      <v-spacer />

      <v-btn
        icon
        @click="themeStore.toggleTheme"
        class="mr-2"
      >
        <v-icon>{{ themeStore.isDark ? 'mdi-weather-sunny' : 'mdi-weather-night' }}</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main>
      <ConverterMain />
    </v-main>

    <v-footer app class="text-center d-flex flex-column">
      <div class="text-caption mb-2">
        Built with Vue 3, TypeScript, and Vuetify 3
      </div>
      <div class="text-caption text-medium-emphasis">
        Computer Unit Converter v1.0.0 - MVP
      </div>
    </v-footer>
  </v-app>
</template>

<script setup lang="ts">
import { onMounted, watch } from 'vue'
import { useTheme } from 'vuetify'
import ConverterMain from './components/ConverterMain.vue'
import { useThemeStore } from './stores/themeStore'

const themeStore = useThemeStore()
const vuetifyTheme = useTheme()

// Initialize theme on mount
onMounted(() => {
  themeStore.initTheme()
  vuetifyTheme.global.name.value = themeStore.isDark ? 'dark' : 'light'
})

// Watch theme changes
watch(
  () => themeStore.isDark,
  (isDark) => {
    vuetifyTheme.global.name.value = isDark ? 'dark' : 'light'
  }
)
</script>

<style>
html, body {
  overflow-x: hidden;
}
</style>
