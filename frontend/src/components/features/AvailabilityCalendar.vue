<template>
  <div class="availability-calendar" ref="rootRef">
    <div class="calendar-toolbar">
      <div class="timezone-picker" v-if="showTimezoneSelector">
        <label class="tz-label">Timezone</label>
        <select class="tz-select" :value="selectedTz" @change="onTimezoneChange($event.target.value)">
          <option v-for="tz in timezones" :key="tz.tz" :value="tz.tz">
            {{ formatTzLabel(tz.tz) }}
          </option>
        </select>
      </div>

      <div class="day-actions" v-if="showSelectAll && !isHeatmap">
        <button class="btn" @click="selectAll()">Select all</button>
        <button class="btn btn--secondary" @click="clearAll()">Clear all</button>
      </div>
    </div>

    <div class="calendar-grid">
      <div class="grid-header">
        <div class="cell cell--time">Time</div>
        <div class="cell cell--day" v-for="(dayLabel, d) in dayLabels" :key="d">
          <div class="day-head">
            <span class="day-name">{{ dayLabel }}</span>
            <div class="day-inline-actions" v-if="showSelectAll && !isHeatmap">
              <button class="link" @click="selectDay(d)">all</button>
              <span>·</span>
              <button class="link" @click="clearDay(d)">none</button>
            </div>
          </div>
        </div>
      </div>

      <div class="grid-body" @mouseleave="onEndDrag; hideTooltip()">
        <div class="row" v-for="slot in displaySlots" :key="slot.index">
          <div class="cell cell--time">
            {{ slot.label }}
          </div>
          <div
            v-for="d in 7"
            :key="`d${d-1}-s${slot.displaySlotIndex}`"
            class="cell time-slot"
            :class="slotClasses(d-1, slot.displaySlotIndex)"
          :title="!isHeatmap ? slotTitle(d-1, slot.displaySlotIndex) : null"
            @mousedown.prevent="onBeginDrag(d-1, slot.displaySlotIndex, $event)"
            @mouseenter="onHoverCell(d-1, slot.displaySlotIndex, $event); onDragOver(d-1, slot.displaySlotIndex)"
            @mousemove="onHoverMove($event)"
            @mouseup.stop="onEndDrag"
          />
        </div>
      </div>
    </div>

    <div class="legend" v-if="showLegend">
      <template v-if="isHeatmap">
        <div class="legend-item"><span class="legend-swatch heat-0"></span> 0</div>
        <div class="legend-item"><span class="legend-swatch heat-25"></span> 25%</div>
        <div class="legend-item"><span class="legend-swatch heat-50"></span> 50%</div>
        <div class="legend-item"><span class="legend-swatch heat-75"></span> 75%</div>
        <div class="legend-item"><span class="legend-swatch heat-100"></span> 100%</div>
      </template>
      <template v-else>
        <div class="legend-item"><span class="legend-swatch on"></span> Available</div>
        <div class="legend-item"><span class="legend-swatch off"></span> Unavailable</div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { computed, toRefs, ref, onMounted, onBeforeUnmount } from 'vue'
import { useMembersStore } from '@/store/modules/members'
import { getUnifiedTimezones, formatTimezoneCurrentLabel, timezoneMapping, timezoneOffset } from '@/utils/timezone'

// Props
const props = defineProps({
  modelValue: { type: Object, default: () => ({}) },
  startHour: { type: Number, default: 0 },
  endHour: { type: Number, default: 24 },
  slotInterval: { type: Number, default: 60 },
  showTimezoneSelector: { type: Boolean, default: true },
  showSelectAll: { type: Boolean, default: true },
  showLegend: { type: Boolean, default: true },
  timezone: { type: String, default: null },
  baseTimezone: { type: String, default: 'UTC' },
  memberId: { type: [String, Number], default: null },
  heatmapData: { type: Object, default: null },
  heatmapMax: { type: Number, default: 0 },
  slotMembersInfo: { type: Object, default: null },
  debug: { type: Boolean, default: false },
})

const emit = defineEmits(['update:modelValue', 'change', 'update:timezone', 'hover-info'])

const { modelValue, startHour, endHour, slotInterval, timezone, baseTimezone } = toRefs(props)

// Stores
const membersStore = useMembersStore()

// Timezones
const timezones = computed(() => getUnifiedTimezones())
const selectedTz = computed(() => timezone?.value || Intl.DateTimeFormat().resolvedOptions().timeZone)

function onTimezoneChange(tz) {
  emit('update:timezone', tz)
}

function formatTzLabel(tz) {
  return formatTimezoneCurrentLabel(tz)
}

// Calendar derived values
const totalMinutes = computed(() => Math.max(0, (endHour.value - startHour.value) * 60))
const totalSlotsPerDay = computed(() => Math.max(1, Math.round(totalMinutes.value / slotInterval.value)))

// Sort rows by (baseMinutes + tzOffset) % 1440 to show local-time order
const tzMinuteOffset = computed(() => timezoneOffset('UTC', selectedTz.value))

const displaySlots = computed(() => {
  const slots = []
  for (let i = 0; i < totalSlotsPerDay.value; i += 1) {
    const baseMinutes = startHour.value * 60 + i * slotInterval.value
    const localMinutes = (baseMinutes + (tzMinuteOffset.value || 0) + 1440) % 1440
    const hours = Math.floor(localMinutes / 60)
    const minutes = localMinutes % 60
    const hh = String(hours).padStart(2, '0')
    const mm = String(minutes).padStart(2, '0')
    slots.push({
      index: i,
      baseMinutes,
      localMinutes,
      label: `${hh}:${mm}`,
    })
  }
  // Stable sort by localMinutes but keep mapping to an index for rendering
  const sorted = [...slots].sort((a, b) => a.localMinutes - b.localMinutes)
  return sorted.map((s, displayIndex) => ({ ...s, displaySlotIndex: displayIndex }))
})

// Mapping helpers
const mappingUtcToDisplay = computed(() => timezoneMapping('UTC', selectedTz.value))

function displayKey(dIndex, sIndex) {
  return `day_${dIndex}_slot_${sIndex}`
}

function baseKeyFromDisplay(dIndex, sIndex) {
  // Our display grid uses day_d_slot_s indices in the DISPLAY timezone rows order.
  // Need to map display slot index back to base slot index using slot offset.
  const slotOffset = mappingUtcToDisplay.value.slotOffset(slotInterval.value)
  // In display, rows are rotated by +slotOffset; reverse that to base index.
  let baseSlot = sIndex - slotOffset
  while (baseSlot < 0) baseSlot += totalSlotsPerDay.value
  while (baseSlot >= totalSlotsPerDay.value) baseSlot -= totalSlotsPerDay.value
  // Map day across boundaries using provided helper
  const key = mappingUtcToDisplay.value.displayKeyToBaseKey(`day_${dIndex}`, `slot_${sIndex}`, {
    slotInterval: slotInterval.value,
    totalSlotsPerDay: totalSlotsPerDay.value,
    days: 7,
  })
  return key || `day_${dIndex}_slot_${baseSlot}`
}

// Active state for a cell
function isActive(dIndex, sIndex) {
  if (!modelValue?.value) return false
  const baseKey = baseKeyFromDisplay(dIndex, sIndex)
  return !!modelValue.value[baseKey]
}

// Heat intensity [0,1]
function heatRatio(dIndex, sIndex) {
  const data = props.heatmapData
  const max = props.heatmapMax || 0
  if (!data || max <= 0) return 0
  const baseKey = baseKeyFromDisplay(dIndex, sIndex)
  const count = data[baseKey] || 0
  return Math.max(0, Math.min(1, count / max))
}

const isHeatmap = computed(() => !!props.heatmapData && (props.heatmapMax || 0) > 0)

function slotClasses(dIndex, sIndex) {
  if (isHeatmap.value) {
    const r = heatRatio(dIndex, sIndex)
    return {
      'slot--heatmap': true,
      'heat-0': r === 0,
      'heat-25': r > 0 && r <= 0.25,
      'heat-50': r > 0.25 && r <= 0.5,
      'heat-75': r > 0.5 && r <= 0.75,
      'heat-100': r > 0.75,
    }
  }
  return { 'slot--interactive': true, 'on': isActive(dIndex, sIndex), 'off': !isActive(dIndex, sIndex) }
}

function slotTitle(dIndex, sIndex) {
  if (isHeatmap.value) {
    const baseKey = baseKeyFromDisplay(dIndex, sIndex)
    const info = props.slotMembersInfo?.[baseKey]
    if (!info) return `Available: 0 / ${props.heatmapMax || 0}`
    const availNames = (info.available || []).map(p => p.name).join(', ')
    const unavailNames = (info.unavailable || []).map(p => p.name).join(', ')
    return `Available (${info.available.length}): ${availNames}\nUnavailable (${info.unavailable.length}): ${unavailNames}`
  }
  return isActive(dIndex, sIndex) ? 'Click to mark unavailable' : 'Click to mark available'
}

// Drag selection state
const isDragging = ref(false)
const dragSetTo = ref(true) // true = set available, false = clear
const dragSnapshot = ref(null)
const rootRef = ref(null)

function applySet(baseKey, setTo, working) {
  if (setTo) working[baseKey] = true
  else if (working[baseKey] !== undefined) delete working[baseKey]
}

function onBeginDrag(dIndex, sIndex, evt) {
  if (isHeatmap.value) return
  isDragging.value = true
  dragSnapshot.value = { ...(modelValue.value || {}) }
  const baseKey = baseKeyFromDisplay(dIndex, sIndex)
  const wasActive = !!dragSnapshot.value[baseKey]
  dragSetTo.value = !wasActive
  const next = { ...dragSnapshot.value }
  applySet(baseKey, dragSetTo.value, next)
  emit('update:modelValue', next)
}

function onDragOver(dIndex, sIndex) {
  if (!isDragging.value || isHeatmap.value) return
  const baseKey = baseKeyFromDisplay(dIndex, sIndex)
  const next = { ...(modelValue.value || {}) }
  applySet(baseKey, dragSetTo.value, next)
  emit('update:modelValue', next)
}

function onEndDrag() {
  if (!isDragging.value) return
  isDragging.value = false
  const finalMap = { ...(modelValue.value || {}) }
  emit('change', finalMap)
  if (props.memberId != null && membersStore?.updateAvailability) {
    const memberId = props.memberId
    const snapshot = dragSnapshot.value || {}
    Promise.resolve(membersStore.updateAvailability(memberId, finalMap)).catch((e) => {
      console.error('[AvailabilityCalendar] Persist failed; reverting', e)
      emit('update:modelValue', snapshot)
      emit('change', snapshot)
    })
  }
}

function onGlobalMouseUp() { onEndDrag() }

// Day-level actions
function selectDay(dayIndex) {
  if (isHeatmap.value) return
  const next = { ...(modelValue.value || {}) }
  for (let s = 0; s < totalSlotsPerDay.value; s += 1) {
    const key = baseKeyFromDisplay(dayIndex, s)
    next[key] = true
  }
  emit('update:modelValue', next)
  emit('change', next)
}

function clearDay(dayIndex) {
  if (isHeatmap.value) return
  const next = { ...(modelValue.value || {}) }
  for (let s = 0; s < totalSlotsPerDay.value; s += 1) {
    const key = baseKeyFromDisplay(dayIndex, s)
    if (next[key] !== undefined) delete next[key]
  }
  emit('update:modelValue', next)
  emit('change', next)
}

function selectAll() {
  if (isHeatmap.value) return
  const next = { ...(modelValue.value || {}) }
  for (let d = 0; d < 7; d += 1) {
    for (let s = 0; s < totalSlotsPerDay.value; s += 1) {
      const key = baseKeyFromDisplay(d, s)
      next[key] = true
    }
  }
  emit('update:modelValue', next)
  emit('change', next)
}

function clearAll() {
  if (isHeatmap.value) return
  const next = { ...(modelValue.value || {}) }
  for (let d = 0; d < 7; d += 1) {
    for (let s = 0; s < totalSlotsPerDay.value; s += 1) {
      const key = baseKeyFromDisplay(d, s)
      if (next[key] !== undefined) delete next[key]
    }
  }
  emit('update:modelValue', next)
  emit('change', next)
}

// Static labels
const dayLabels = computed(() => ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])

function onHoverCell(dIndex, sIndex, evt) {
  if (!isHeatmap.value) return
  const baseKey = baseKeyFromDisplay(dIndex, sIndex)
  const info = props.slotMembersInfo?.[baseKey] || { available: [], unavailable: [] }
  const slot = displaySlots.value.find(s => s.displaySlotIndex === sIndex)
  emit('hover-info', { baseKey, dayIndex: dIndex, slotIndex: sIndex, timeLabel: slot?.label || '', available: info.available || [], unavailable: info.unavailable || [] })
}

function onHoverMove(evt) {
  // No-op: visual tooltip removed; keeping handler to avoid template change
}

function hideTooltip() { emit('hover-info', null) }

onMounted(() => {
  window.addEventListener('mouseup', onGlobalMouseUp)
})

onBeforeUnmount(() => {
  window.removeEventListener('mouseup', onGlobalMouseUp)
})
</script>

<style scoped>
.availability-calendar {
  display: flex;
  flex-direction: column;
  gap: 12px;
  position: relative;
}

.calendar-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.timezone-picker { display: flex; align-items: center; gap: 8px; }
.tz-label { font-weight: 600; }
.tz-select { padding: 6px 8px; border: 1px solid var(--border-primary, #e5e7eb); border-radius: 6px; }

.day-actions { display: flex; gap: 8px; }
.btn { padding: 6px 10px; border-radius: 6px; border: none; cursor: pointer; background: var(--color-primary, #3b82f6); color: #fff; }
.btn--secondary { background: #64748b; }
.link { background: none; border: none; color: var(--color-primary, #3b82f6); cursor: pointer; padding: 0; }

.calendar-grid { border: 1px solid var(--border-primary, #e5e7eb); border-radius: 8px; overflow: hidden; }
.grid-header, .row { display: grid; grid-template-columns: 90px repeat(7, 1fr); }
.grid-header { background: #f8fafc; border-bottom: 1px solid var(--border-primary, #e5e7eb); }
.grid-body .row:nth-child(odd) { background: #fcfdff; }
.cell { padding: 8px; border-right: 1px solid var(--border-primary, #e5e7eb); }
.cell:last-child { border-right: none; }
.cell--time { font-weight: 600; font-size: 12px; color: #475569; }
.cell--day { text-align: center; font-weight: 600; font-size: 12px; color: #334155; }
.day-head { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
.day-inline-actions { display: flex; align-items: center; gap: 6px; font-size: 11px; }

.time-slot { cursor: pointer; min-height: 28px; }
.slot--interactive.on { background: #dbeafe; }
.slot--interactive.off { background: #ffffff; }
.slot--heatmap { background: #f1f5f9; cursor: default; }
.heat-0 { background: #f1f5f9; }
.heat-25 { background: #c7d2fe; }
.heat-50 { background: #93c5fd; }
.heat-75 { background: #60a5fa; }
.heat-100 { background: #3b82f6; }

.legend { display: flex; gap: 12px; align-items: center; font-size: 12px; color: #475569; }
.legend-item { display: flex; gap: 6px; align-items: center; }
.legend-swatch { width: 14px; height: 14px; border-radius: 3px; display: inline-block; }
.legend-swatch.on { background: #3b82f6; }
.legend-swatch.off { background: #e2e8f0; }
.legend-swatch.heat-0 { background: #f1f5f9; }
.legend-swatch.heat-25 { background: #c7d2fe; }
.legend-swatch.heat-50 { background: #93c5fd; }
.legend-swatch.heat-75 { background: #60a5fa; }
.legend-swatch.heat-100 { background: #3b82f6; }

.heatmap-tooltip {
  position: absolute;
  z-index: 10;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 8px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
  width: 260px;
  pointer-events: none;
}
.tooltip-section { display: flex; flex-direction: column; gap: 4px; }
.tooltip-title { font-weight: 700; font-size: 12px; color: #334155; }
.tooltip-names { font-size: 12px; color: #475569; word-break: break-word; }
</style>


