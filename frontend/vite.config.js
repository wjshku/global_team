import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
      '@constants': resolve(__dirname, 'src/constants')
    }
  },
  define: {
    __API_BASE__: JSON.stringify(process.env.VITE_API_BASE || ''),
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets'
  }
})