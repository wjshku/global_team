// Timezone utilities and unified timezone catalog
const Z = (n) => (n < 10 ? `0${n}` : `${n}`)
function labelFor(tz, city, offsetMinutes) {
  const sign = offsetMinutes >= 0 ? '+' : '-'
  const abs = Math.abs(offsetMinutes)
  const hh = Math.floor(abs / 60)
  const mm = abs % 60
  return `${city} (UTC${sign}${Z(hh)}:${Z(mm)})`
}

export const UNIFIED_TIMEZONES = [
  { tz: 'Pacific/Niue', city: 'Niue', offset: -660 },
  { tz: 'Pacific/Honolulu', city: 'Honolulu', offset: -600 },
  { tz: 'America/Anchorage', city: 'Anchorage', offset: -540 },
  { tz: 'America/Los_Angeles', city: 'Los Angeles', offset: -480 },
  { tz: 'America/Denver', city: 'Denver', offset: -420 },
  { tz: 'America/Chicago', city: 'Chicago', offset: -360 },
  { tz: 'America/New_York', city: 'New York', offset: -300 },
  { tz: 'America/Halifax', city: 'Halifax', offset: -240 },
  { tz: 'America/Argentina/Buenos_Aires', city: 'Buenos Aires', offset: -180 },
  { tz: 'Atlantic/South_Georgia', city: 'South Georgia', offset: -120 },
  { tz: 'Atlantic/Azores', city: 'Azores', offset: -60 },
  { tz: 'UTC', city: 'UTC', offset: 0 },
  { tz: 'Europe/London', city: 'London', offset: 0 },
  { tz: 'Europe/Berlin', city: 'Berlin', offset: 60 },
  { tz: 'Europe/Athens', city: 'Athens', offset: 120 },
  { tz: 'Europe/Moscow', city: 'Moscow', offset: 180 },
  { tz: 'Asia/Dubai', city: 'Dubai', offset: 240 },
  { tz: 'Asia/Karachi', city: 'Karachi', offset: 300 },
  { tz: 'Asia/Kolkata', city: 'India (Kolkata)', offset: 330 },
  { tz: 'Asia/Dhaka', city: 'Dhaka', offset: 360 },
  { tz: 'Asia/Bangkok', city: 'Bangkok', offset: 420 },
  { tz: 'Asia/Singapore', city: 'Singapore', offset: 480 },
  { tz: 'Asia/Tokyo', city: 'Tokyo', offset: 540 },
  { tz: 'Australia/Adelaide', city: 'Adelaide', offset: 570 },
  { tz: 'Australia/Sydney', city: 'Sydney', offset: 600 },
  { tz: 'Pacific/Noumea', city: 'Noumea', offset: 660 },
  { tz: 'Pacific/Auckland', city: 'Auckland', offset: 720 },
  { tz: 'Pacific/Chatham', city: 'Chatham Islands', offset: 765 }
]

export function getUnifiedTimezones() {
  return UNIFIED_TIMEZONES
}

/**
 * Format a single timezone label with its current offset (DST-aware)
 * Falls back to a best-effort city name if tz not in the unified list
 */
export function formatTimezoneCurrentLabel(tz) {
  if (!tz) return ''
  const entry = UNIFIED_TIMEZONES.find(t => t.tz === tz)
  const city = entry?.city || String(tz).split('/').pop()?.replace(/_/g, ' ') || String(tz)
  const offset = timezoneOffset('UTC', tz)
  return labelFor(tz, city, offset)
}

export function isUnifiedTimezone(tz) {
  return UNIFIED_TIMEZONES.some(t => t.tz === tz)
}

/**
 * Get user's current timezone
 * @returns {string} User's timezone
 */
export function getUserTimezone() {
  return Intl.DateTimeFormat().resolvedOptions().timeZone
}


/**
 * Get current time in specific timezone
 * @param {string} timezone - Target timezone
 * @returns {Date} Current time in timezone
 */
export function getCurrentTimeInTimezone(timezone) {
  const now = new Date()
  // Represent "now" displayed in the requested timezone
  return new Date(now.getTime())
}

/**
 * Compute minute offset from one timezone to another at current moment.
 * Positive result means target timezone is ahead of source.
 * @param {string} fromTz
 * @param {string} toTz
 * @returns {number} minutes offset
 */
export function timezoneOffset(fromTz, toTz) {
  try {
    const now = new Date()
    const fmt = (tz) => new Intl.DateTimeFormat('en-US', { timeZone: tz, hour12: false, hour: '2-digit', minute: '2-digit' }).format(now)
    const [fromH, fromM] = fmt(fromTz).split(':').map(v => parseInt(v, 10))
    const [toH, toM] = fmt(toTz).split(':').map(v => parseInt(v, 10))
    const fromTotal = fromH * 60 + fromM
    const toTotal = toH * 60 + toM
    let diff = toTotal - fromTotal
    if (diff > 720) diff -= 1440
    if (diff < -720) diff += 1440
    return diff
  } catch (e) {
    return 0
  }
}

export function timezoneMapping(fromTz, toTz) {
  const parseIndex = (key, prefix) => {
    const m = String(key).match(new RegExp(`^${prefix}_(\\d+)$`))
    return m ? parseInt(m[1], 10) || 0 : 0
  }

  function displayKeyToBaseKey(dayKey, slotKey, { slotInterval, totalSlotsPerDay, days = 7 }) {
    const dayIdx = parseIndex(dayKey, 'day')
    const slotIdx = parseIndex(slotKey, 'slot')
    const minuteOffset = timezoneOffset(fromTz, toTz)
    const slotOffset = Math.round(minuteOffset / (slotInterval || 60))
    let newSlot = slotIdx - slotOffset
    let newDay = dayIdx
    while (newSlot < 0) { newSlot += totalSlotsPerDay; newDay -= 1 }
    while (newSlot >= totalSlotsPerDay) { newSlot -= totalSlotsPerDay; newDay += 1 }
    if (days && days > 0) {
      newDay = ((newDay % days) + days) % days
    } else {
      newDay = Math.max(0, newDay)
    }
    return `day_${newDay}_slot_${newSlot}`
  }

  function translateAvailability(availability, { slotInterval = 60, totalSlotsPerDay = 24, days = 7 } = {}) {
    if (!availability || typeof availability !== 'object') return {}
    const result = {}
    const minuteOffset = timezoneOffset(fromTz, toTz)
    const slotOffset = Math.round(minuteOffset / (slotInterval || 60))
    for (const [key, value] of Object.entries(availability)) {
      if (!value) continue
      let dayIdx
      let slotIdx
      if (/^day_\d+_slot_\d+$/.test(String(key))) {
        const m = String(key).match(/^day_(\d+)_slot_(\d+)$/)
        dayIdx = parseInt(m[1], 10) || 0
        slotIdx = parseInt(m[2], 10) || 0
      } else {
        const parts = String(key).split('_')
        if (parts.length === 4 && parts[0] === 'day' && parts[2] === 'slot') {
          dayIdx = parseInt(parts[1], 10) || 0
          slotIdx = parseInt(parts[3], 10) || 0
        } else if (parts.length === 2 && parts[0].startsWith('day') && parts[1].startsWith('slot')) {
          dayIdx = parseIndex(parts[0], 'day')
          slotIdx = parseIndex(parts[1], 'slot')
        } else {
          continue
        }
      }
      let newSlot = slotIdx + slotOffset
      let newDay = dayIdx
      while (newSlot < 0) { newSlot += totalSlotsPerDay; newDay -= 1 }
      while (newSlot >= totalSlotsPerDay) { newSlot -= totalSlotsPerDay; newDay += 1 }
      if (days && days > 0) {
        newDay = ((newDay % days) + days) % days
      } else {
        newDay = Math.max(0, newDay)
      }
      const newKey = `day_${newDay}_slot_${newSlot}`
      result[newKey] = true
    }
    return result
  }

  function offsetMinutes() {
    return timezoneOffset(fromTz, toTz)
  }

  function slotOffset(slotInterval) {
    return Math.round(offsetMinutes() / (slotInterval || 60))
  }

  return { displayKeyToBaseKey, translateAvailability, offsetMinutes, slotOffset }
}

/**
 * Format a date/time in a specific timezone with a consistent style and TZ label.
 * @param {string|Date|number} date - ISO string or Date or timestamp
 * @param {string} targetTimezone - IANA timezone to display in
 * @param {object} options - Optional Intl options to override defaults
 * @returns {string}
 */
export function formatDateTimeInTimezone(date, targetTimezone, options = {}) {
  if (!date) return 'N/A'
  const d = typeof date === 'string' || typeof date === 'number' ? new Date(date) : date
  if (isNaN(d?.getTime?.())) return 'Invalid Date'
  const defaults = {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: true,
    timeZone: targetTimezone || getUserTimezone(),
    timeZoneName: 'short'
  }
  const fmt = { ...defaults, ...options }
  return d.toLocaleString('en-US', fmt)
}

/**
 * Convert and format a meeting datetime from its stored timezone (or UTC) to user's timezone.
 * Note: If the input is a proper ISO string with timezone (or UTC), no conversion is needed; we
 * simply render using the user's timezone via Intl options.
 * @param {string|Date|number} datetime - meeting datetime (prefer ISO with timezone/UTC)
 * @param {string} meetingTz - source meeting timezone (optional; reserved for naive strings)
 * @param {string} userTz - target user timezone
 * @param {object} options - Intl override options
 * @returns {string}
 */
export function convertToUserTimezone(datetime, meetingTz, userTz, options = {}) {
  // For ISO-with-TZ inputs, a Date represents an absolute instant. We format in userTz.
  return formatDateTimeInTimezone(datetime, userTz, options)
}