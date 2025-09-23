import { defineStore } from 'pinia'
import { THEMES, STORAGE_KEYS } from '@/utils/constants'

export const useUIStore = defineStore('ui', {
  state: () => ({
    notifications: [],
    loading: false,
    error: null,
    theme: THEMES.AUTO
  }),

  getters: {
    allNotifications: (state) => state.notifications,
    isLoading: (state) => state.loading,
    hasError: (state) => !!state.error,
    isDark: (state) => {
      if (state.theme === THEMES.DARK) return true
      if (state.theme === THEMES.LIGHT) return false
      return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
    },
    currentTheme: (state) => state.theme
  },

  actions: {
    showNotification(notification) {
      const id = Date.now().toString()
      const newNotification = {
        id,
        type: notification.type || 'info',
        message: notification.message,
        duration: notification.duration || 5000,
        timestamp: new Date().toISOString()
      }
      
      this.notifications.push(newNotification)
      
      // Auto-remove notification after duration
      if (newNotification.duration > 0) {
        setTimeout(() => {
          this.removeNotification(id)
        }, newNotification.duration)
      }
      
      return id
    },

    removeNotification(notificationId) {
      this.notifications = this.notifications.filter(n => n.id !== notificationId)
    },

    clearAllNotifications() {
      this.notifications = []
    },

    setLoading(loading) {
      this.loading = loading
    },

    setError(error) {
      this.error = error
    },

    clearError() {
      this.error = null
    },

    initializeTheme() {
      try {
        const saved = localStorage.getItem(STORAGE_KEYS.THEME)
        if (saved === THEMES.DARK || saved === THEMES.LIGHT || saved === THEMES.AUTO) {
          this.theme = saved
        } else {
          this.theme = THEMES.AUTO
        }
      } catch {}
      this.applyTheme()
      if (window.matchMedia) {
        const mq = window.matchMedia('(prefers-color-scheme: dark)')
        mq.addEventListener?.('change', () => {
          if (this.theme === THEMES.AUTO) this.applyTheme()
        })
      }
    },

    setTheme(theme) {
      if (![THEMES.LIGHT, THEMES.DARK, THEMES.AUTO].includes(theme)) return
      this.theme = theme
      try {
        localStorage.setItem(STORAGE_KEYS.THEME, theme)
      } catch {}
      this.applyTheme()
    },

    toggleTheme() {
      const next = this.isDark ? THEMES.LIGHT : THEMES.DARK
      this.setTheme(next)
    },

    applyTheme() {
      const root = document.documentElement
      if (this.theme === THEMES.AUTO) {
        root.removeAttribute('data-theme')
      } else {
        root.setAttribute('data-theme', this.theme)
      }
    }
  }
})
