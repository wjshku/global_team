// Authentication API calls - login, logout, user management
import { apiRequest } from './index.js'

// Mock toggle
const USE_MOCK_API = import.meta.env.VITE_USE_MOCKS === 'true'

// Moved mock accounts from store to API layer
const MOCK_ACCOUNTS = {
  'john@example.com': {
    id: '1',
    name: 'John Doe',
    email: 'john@example.com',
    password: 'password123',
    timezone: 'America/New_York',
    role: 'admin',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=John',
    createdAt: '2024-01-15T10:00:00Z'
  },
  'jane@example.com': {
    id: '2',
    name: 'Jane Smith',
    email: 'jane@example.com',
    password: 'password123',
    timezone: 'Asia/Singapore',
    role: 'member',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Jane',
    createdAt: '2024-01-16T14:30:00Z'
  },
  'mike@example.com': {
    id: '3',
    name: 'Mike Johnson',
    email: 'mike@example.com',
    password: 'password123',
    timezone: 'Asia/Singapore',
    role: 'member',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Mike',
    createdAt: '2024-01-17T09:15:00Z'
  },
  'sarah@example.com': {
    id: '4',
    name: 'Sarah Wilson',
    email: 'sarah@example.com',
    password: 'password123',
    timezone: 'Asia/Singapore',
    role: 'member',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Sarah',
    createdAt: '2024-01-18T16:45:00Z'
  }
}

// Helpers for mock behavior
const generateToken = (id) => `mock-jwt-token-${id}`
const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms))

// Authentication API functions
export const authAPI = {
  // Login user
  async login(credentials) {
    try {
      if (USE_MOCK_API) {
        const { email, password } = credentials || {}
        await delay(500)
        const account = MOCK_ACCOUNTS[email]
        if (!account) {
          throw new Error('User not found')
        }
        if (account.password !== password) {
          throw new Error('Invalid password')
        }
        return {
          ...account,
          token: generateToken(account.id),
          lastLogin: new Date().toISOString()
        }
      }

      const response = await apiRequest('/auth/login', {
        method: 'POST',
        body: JSON.stringify(credentials),
      })
      return response
    } catch (error) {
      console.error('Login failed:', error)
      throw error
    }
  },

  // Register new user
  async register(userData) {
    try {
      if (USE_MOCK_API) {
        const { email, password, name, timezone } = userData || {}
        await delay(500)
        if (MOCK_ACCOUNTS[email]) {
          throw new Error('User already exists')
        }
        const id = (Object.keys(MOCK_ACCOUNTS).length + 1).toString()
        const newUser = {
          id,
          name,
          email,
          password,
          timezone,
          role: 'member',
          avatar: `https://api.dicebear.com/7.x/avataaars/svg?seed=${(name || '').replace(' ', '')}`,
          createdAt: new Date().toISOString()
        }
        MOCK_ACCOUNTS[email] = newUser
        return {
          ...newUser,
          token: generateToken(id),
          lastLogin: new Date().toISOString()
        }
      }

      const response = await apiRequest('/auth/register', {
        method: 'POST',
        body: JSON.stringify(userData),
      })
      return response
    } catch (error) {
      console.error('Registration failed:', error)
      throw error
    }
  },

  // Logout user
  async logout() {
    try {
      await apiRequest('/auth/logout', {
        method: 'POST',
      })
    } catch (error) {
      console.error('Logout failed:', error)
      throw error
    }
  },

  // Get current user profile
  async getProfile() {
    try {
      if (USE_MOCK_API) {
        await delay(300)
        // In a real app we would decode token; here, pick the first user
        const first = Object.values(MOCK_ACCOUNTS)[0]
        if (!first) throw new Error('No profile')
        return {
          ...first,
          token: generateToken(first.id)
        }
      }

      const response = await apiRequest('/auth/profile')
      return response
    } catch (error) {
      console.error('Get profile failed:', error)
      throw error
    }
  },

  // Update user profile
  async updateProfile(profileData) {
    try {
      const response = await apiRequest('/auth/profile', {
        method: 'PUT',
        body: JSON.stringify(profileData),
      })
      return response
    } catch (error) {
      console.error('Update profile failed:', error)
      throw error
    }
  },

  // Verify token validity
  async verifyToken(token) {
    try {
      if (USE_MOCK_API) {
        await delay(200)
        const isValid = typeof token === 'string' && token.startsWith('mock-jwt-token-')
        return { valid: isValid }
      }

      const response = await apiRequest('/auth/verify', {
        method: 'POST',
        body: JSON.stringify({ token }),
      })
      return response
    } catch (error) {
      console.error('Token verification failed:', error)
      throw error
    }
  }
}

export default authAPI
