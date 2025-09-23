// Validation utility functions - form validation, data validation

/**
 * Validate email format
 * @param {string} email - Email to validate
 * @returns {boolean} True if valid email format
 */
export function isValidEmail(email) {
  if (typeof email !== 'string') return false
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email.trim())
}

/**
 * Validate password strength
 * @param {string} password - Password to validate
 * @returns {object} Validation result with isValid and message
 */
export function validatePassword(password) {
  if (typeof password !== 'string') {
    return { isValid: false, message: 'Password must be a string' }
  }
  
  if (password.length < 8) {
    return { isValid: false, message: 'Password must be at least 8 characters long' }
  }
  
  if (!/[A-Z]/.test(password)) {
    return { isValid: false, message: 'Password must contain at least one uppercase letter' }
  }
  
  if (!/[a-z]/.test(password)) {
    return { isValid: false, message: 'Password must contain at least one lowercase letter' }
  }
  
  if (!/\d/.test(password)) {
    return { isValid: false, message: 'Password must contain at least one number' }
  }
  
  return { isValid: true, message: 'Password is valid' }
}

/**
 * Validate required fields
 * @param {object} data - Object to validate
 * @param {array} requiredFields - Array of required field names
 * @returns {object} Validation result with isValid and missing fields
 */
export function validateRequired(data, requiredFields) {
  if (typeof data !== 'object' || data === null) {
    return { isValid: false, missingFields: requiredFields }
  }
  
  const missingFields = requiredFields.filter(field => {
    const value = data[field]
    return value === undefined || value === null || value === ''
  })
  
  return {
    isValid: missingFields.length === 0,
    missingFields
  }
}

/**
 * Validate team name
 * @param {string} name - Team name to validate
 * @returns {object} Validation result
 */
export function validateTeamName(name) {
  if (typeof name !== 'string') {
    return { isValid: false, message: 'Team name must be a string' }
  }
  
  const trimmed = name.trim()
  
  if (trimmed.length === 0) {
    return { isValid: false, message: 'Team name is required' }
  }
  
  if (trimmed.length < 2) {
    return { isValid: false, message: 'Team name must be at least 2 characters long' }
  }
  
  if (trimmed.length > 50) {
    return { isValid: false, message: 'Team name must be less than 50 characters' }
  }
  
  return { isValid: true, message: 'Team name is valid' }
}

// isValidTimezone moved to timezone.js to avoid duplication

// sanitizeString removed - no usage identified in components
