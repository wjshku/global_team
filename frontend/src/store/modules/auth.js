import { defineStore } from 'pinia'
import { authAPI } from '@/api/auth'

const USE_MOCKS = import.meta.env.VITE_USE_MOCKS === 'true'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    isAuthenticated: false,
    token: null
  }),

  getters: {
    currentUser: (state) => state.user,
    isLoggedIn: (state) => state.isAuthenticated
  },

  actions: {
    // Backward-compatible mock login wrapper -> delegates to API (mock or real)
    async mockLogin(email, password) {
      const result = await authAPI.login({ email, password })
      // In mock mode, login returns a full user + token
      if (USE_MOCKS) {
        this.user = result
        this.isAuthenticated = true
        this.token = result.token || null
        localStorage.setItem('user', JSON.stringify(this.user))
        if (this.token) localStorage.setItem('token', this.token)
        return this.user
      }
      // Real backend: login returns access token only
      const token = result?.accessToken || result?.token?.accessToken || null
      if (!token) throw new Error('Login did not return access token')
      this.token = token
      this.isAuthenticated = true
      localStorage.setItem('token', token)
      // Fetch the authenticated profile
      const profile = await authAPI.getProfile()
      this.user = profile
      localStorage.setItem('user', JSON.stringify(profile))
      return profile
    },

    // Backward-compatible mock signup wrapper -> delegates to API (mock or real)
    async mockSignup(userData) {
      const created = await authAPI.register(userData)
      if (USE_MOCKS) {
        this.user = created
        this.isAuthenticated = true
        this.token = created.token || null
        localStorage.setItem('user', JSON.stringify(this.user))
        if (this.token) localStorage.setItem('token', this.token)
        return created
      }
      const token = created?.accessToken || created?.token?.accessToken || null
      if (!token) throw new Error('Register did not return access token')
      this.token = token
      this.isAuthenticated = true
      localStorage.setItem('token', token)
      const profile = await authAPI.getProfile()
      this.user = profile
      localStorage.setItem('user', JSON.stringify(profile))
      return profile
    },

    login(userData) {
      // Retain for backward compatibility with places that may call login() directly
      // If given a token-shaped object, only store token and fetch profile separately via initializeAuth
      const token = userData?.accessToken || userData?.token?.accessToken || userData?.token || null
      const hasProfileShape = userData && typeof userData === 'object' && !!userData.id
      if (token && !hasProfileShape) {
        this.user = null
        this.isAuthenticated = true
        this.token = token
        localStorage.setItem('token', token)
        localStorage.removeItem('user')
        return
      }
      this.user = userData
      this.isAuthenticated = true
      this.token = userData?.token || this.token
      localStorage.setItem('user', JSON.stringify(this.user))
      if (this.token) localStorage.setItem('token', this.token)
      console.log('AuthStore: User logged in', userData)
    },

    logout() {
      console.log('AuthStore: User logged out')
      this.user = null
      this.isAuthenticated = false
      this.token = null
      
      // Clear localStorage
      localStorage.removeItem('user')
      localStorage.removeItem('token')
    },

    async initializeAuth() {
      // Check for stored auth data on app start
      const storedUser = localStorage.getItem('user')
      const storedToken = localStorage.getItem('token')
      
      if (storedUser) {
        try {
          const parsed = JSON.parse(storedUser)
          // Detect token-shaped object mistakenly stored as user
          const isTokenObject = parsed && typeof parsed === 'object' && !parsed.id && (parsed.accessToken || parsed.tokenType)
          if (isTokenObject) {
            const token = parsed.accessToken || storedToken
            if (token) {
              this.token = token
              this.isAuthenticated = true
              localStorage.setItem('token', token)
              try {
                const profile = await authAPI.getProfile()
                this.user = profile
                localStorage.setItem('user', JSON.stringify(profile))
                console.log('AuthStore: Fixed token-object in user; profile fetched')
              } catch (e) {
                console.error('AuthStore: Failed to fetch profile from token-object user', e)
                this.logout()
              }
              return
            }
          }
          // Normal user object
          this.user = parsed
          this.isAuthenticated = true
          this.token = storedToken
          console.log('AuthStore: User restored from localStorage', this.user)
        } catch (error) {
          console.error('Error parsing stored user data:', error)
          this.logout()
        }
      } else if (storedToken) {
        // No user but we have a token -> fetch profile
        try {
          this.token = storedToken
          this.isAuthenticated = true
          const profile = await authAPI.getProfile()
          this.user = profile
          localStorage.setItem('user', JSON.stringify(profile))
          console.log('AuthStore: Profile fetched from token')
        } catch (error) {
          console.error('Failed to fetch profile with stored token:', error)
          this.logout()
        }
      }
    }
  }
})