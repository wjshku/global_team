// Base API configuration - common API setup and utilities
const API_BASE = import.meta.env.VITE_API_BASE

// Common API utilities
export const apiRequest = async (endpoint, options = {}) => {
  const url = `${API_BASE}${endpoint}`
  
  const defaultOptions = {
    headers: {
      'Content-Type': 'application/json',
      // Inject bearer token if available
      ...(typeof localStorage !== 'undefined' && localStorage.getItem('token')
        ? { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        : {}),
    },
  }
  
  const config = {
    ...defaultOptions,
    ...options,
    headers: {
      ...defaultOptions.headers,
      ...options.headers,
    },
  }
  
  try {
    const response = await fetch(url, config)
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const contentType = response.headers.get('content-type')
    if (contentType && contentType.includes('application/json')) {
      return await response.json()
    }
    
    return await response.text()
  } catch (error) {
    console.error('API request failed:', error)
    throw error
  }
}

// Export API base URL for other modules
export { API_BASE }
