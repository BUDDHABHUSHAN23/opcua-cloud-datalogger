import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 5173,
    proxy: {
      '/api': 'http://backend:8000',
      '/ws': {
        target: 'ws://backend:8000',
        ws: true,
      },
    },
    fs: {
      strict: false,
    },
  },
  // ✅ This handles 404s on route refresh in dev mode
  build: {
    rollupOptions: {
      input: '/index.html',
    },
  },
  resolve: {
    alias: {
      '@': '/src',
    },
  },
})
