// App-wide constants - configuration values, enums, magic numbers
export const APP_NAME = 'MeeTime'

/**
 * API Configuration
 */
export const API_CONFIG = {
  BASE_URL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:3000/api',
  TIMEOUT: 10000, // 10 seconds
  RETRY_ATTEMPTS: 3
}

/**
 * Application Routes
 */
export const ROUTES = {
  HOME: '/',
  SIGNUP: '/signup',
  LOGIN: '/login',
  PERSONAL: '/personal',
  TEAM: '/team/:id',
  MEETING: '/meeting/:id',
  NOT_FOUND: '/404'
}

/**
 * User Roles
 */
export const USER_ROLES = {
  ADMIN: 'admin',
  MEMBER: 'member',
  GUEST: 'guest'
}

/**
 * Team Status
 */
export const TEAM_STATUS = {
  ACTIVE: 'active',
  INACTIVE: 'inactive',
  ARCHIVED: 'archived'
}

/**
 * Meeting Status
 */
export const MEETING_STATUS = {
  SCHEDULED: 'scheduled',
  IN_PROGRESS: 'in_progress',
  COMPLETED: 'completed',
  CANCELLED: 'cancelled'
}

/**
 * UI Constants
 */
export const UI_CONSTANTS = {
  MAX_TEAM_NAME_LENGTH: 50,
  MAX_DESCRIPTION_LENGTH: 500,
  MAX_MEMBERS_PREVIEW: 4,
  DEBOUNCE_DELAY: 300, // milliseconds
  ANIMATION_DURATION: 200 // milliseconds
}

/**
 * Date/Time Formats
 */
export const DATE_FORMATS = {
  SHORT: 'short',
  LONG: 'long',
  RELATIVE: 'relative',
  TIME_ONLY: 'time_only',
  DATE_TIME: 'date_time'
}

/**
 * Validation Rules
 */
export const VALIDATION_RULES = {
  PASSWORD: {
    MIN_LENGTH: 8,
    MAX_LENGTH: 128,
    REQUIRE_UPPERCASE: true,
    REQUIRE_LOWERCASE: true,
    REQUIRE_NUMBER: true,
    REQUIRE_SPECIAL: false
  },
  EMAIL: {
    MAX_LENGTH: 254
  },
  TEAM_NAME: {
    MIN_LENGTH: 2,
    MAX_LENGTH: 50
  },
  DESCRIPTION: {
    MAX_LENGTH: 500
  }
}

/**
 * Error Messages
 */
export const ERROR_MESSAGES = {
  NETWORK_ERROR: 'Network error. Please check your connection.',
  SERVER_ERROR: 'Server error. Please try again later.',
  VALIDATION_ERROR: 'Please check your input and try again.',
  UNAUTHORIZED: 'You are not authorized to perform this action.',
  NOT_FOUND: 'The requested resource was not found.',
  GENERIC: 'Something went wrong. Please try again.'
}

/**
 * Success Messages
 */
export const SUCCESS_MESSAGES = {
  TEAM_CREATED: 'Team created successfully!',
  TEAM_UPDATED: 'Team updated successfully!',
  TEAM_DELETED: 'Team deleted successfully!',
  MEMBER_ADDED: 'Member added successfully!',
  MEMBER_REMOVED: 'Member removed successfully!',
  MEETING_SCHEDULED: 'Meeting scheduled successfully!',
  PROFILE_UPDATED: 'Profile updated successfully!'
}

/**
 * Local Storage Keys
 */
export const STORAGE_KEYS = {
  AUTH_TOKEN: 'auth_token',
  USER_DATA: 'user_data',
  SELECTED_TEAM: 'selected_team',
  THEME: 'theme',
  LANGUAGE: 'language'
}

/**
 * Theme Options
 */
export const THEMES = {
  LIGHT: 'light',
  DARK: 'dark',
  AUTO: 'auto'
}

/**
 * Language Options
 */
export const LANGUAGES = {
  EN: 'en',
  ES: 'es',
  FR: 'fr',
  DE: 'de',
  JA: 'ja'
}
