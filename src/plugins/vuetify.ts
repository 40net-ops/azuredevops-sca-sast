import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

export default createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          primary: '#1976D2',
          secondary: '#00BCD4',
          success: '#4CAF50',
          error: '#F44336',
        },
      },
      dark: {
        colors: {
          primary: '#1976D2',
          secondary: '#00BCD4',
          success: '#4CAF50',
          error: '#F44336',
        },
      },
    },
  },
})
