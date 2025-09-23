// Data formatting utility functions - format dates, numbers, text

/**
 * Format a date string or Date object into a readable format
 * @param {string|Date} date - The date to format
 * @param {string} format - The format type ('short', 'long', 'relative')
 * @returns {string} Formatted date string
 */
export function formatDate(date, format = 'short') {
  if (!date) return 'N/A'
  
  const dateObj = typeof date === 'string' ? new Date(date) : date
  
  // Check if date is valid
  if (isNaN(dateObj.getTime())) {
    return 'Invalid Date'
  }
  
  const now = new Date()
  const diffInMs = now - dateObj
  const diffInDays = Math.floor(diffInMs / (1000 * 60 * 60 * 24))
  
  switch (format) {
    case 'relative':
      if (diffInDays === 0) return 'Today'
      if (diffInDays === 1) return 'Yesterday'
      if (diffInDays < 7) return `${diffInDays} days ago`
      if (diffInDays < 30) return `${Math.floor(diffInDays / 7)} weeks ago`
      if (diffInDays < 365) return `${Math.floor(diffInDays / 30)} months ago`
      return `${Math.floor(diffInDays / 365)} years ago`
    
    case 'long':
      return dateObj.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    
    case 'short':
    default:
      return dateObj.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
  }
}

// formatNumber removed - no usage identified in components

/**
 * Format a time string from a Date object
 * @param {string|Date} date - The date to format
 * @param {boolean} includeSeconds - Whether to include seconds
 * @returns {string} Formatted time string
 */
export function formatTime(date, includeSeconds = false) {
  if (!date) return 'N/A'
  
  const dateObj = typeof date === 'string' ? new Date(date) : date
  
  if (isNaN(dateObj.getTime())) {
    return 'Invalid Time'
  }
  
  return dateObj.toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    second: includeSeconds ? '2-digit' : undefined,
    hour12: true
  })
}

/**
 * Format a duration in milliseconds to a readable string
 * @param {number} ms - Duration in milliseconds
 * @returns {string} Formatted duration string
 */
export function formatDuration(ms) {
  if (typeof ms !== 'number' || isNaN(ms) || ms < 0) return '0s'
  
  const seconds = Math.floor(ms / 1000)
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)
  const days = Math.floor(hours / 24)
  
  if (days > 0) return `${days}d ${hours % 24}h`
  if (hours > 0) return `${hours}h ${minutes % 60}m`
  if (minutes > 0) return `${minutes}m ${seconds % 60}s`
  return `${seconds}s`
}

/**
 * Format date and time together
 * @param {string|Date} date - The date to format
 * @param {object} options - Formatting options
 * @returns {string} Formatted date and time string
 */
export function formatDateTime(date, options = {}) {
  if (!date) return 'N/A'
  
  const dateObj = typeof date === 'string' ? new Date(date) : date
  
  if (isNaN(dateObj.getTime())) {
    return 'Invalid Date'
  }
  
  const defaultOptions = {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: true,
    timeZoneName: 'short'
  }
  
  const formatOptions = { ...defaultOptions, ...options }
  
  return dateObj.toLocaleString('en-US', formatOptions)
}

/**
 * Truncate text to a specified length with ellipsis
 * @param {string} text - The text to truncate
 * @param {number} maxLength - Maximum length before truncation
 * @returns {string} Truncated text
 */
export function truncateText(text, maxLength = 50) {
  if (typeof text !== 'string') return ''
  if (text.length <= maxLength) return text
  return text.substring(0, maxLength - 3) + '...'
}
