import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  define: {
    __API_BASE__: JSON.stringify(process.env.VITE_API_BASE || ''),
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets'
  }
})


