<template>
  <div>
    <div v-if="!results || results.length === 0" class="empty-state">
      <p class="empty-message">No votes yet.</p>
    </div>
    <div v-else class="results-content">
      <div class="results-summary">
        <div class="summary-item">
          <span class="summary-label">Total Votes:</span>
          <span class="summary-value">{{ totalVotes }}</span>
        </div>
      </div>
      <div class="results-chart">
        <div
          v-for="result in sortedResults"
          :key="result.option"
          class="result-item"
        >
          <div class="result-option">
            <span class="result-option-text">{{ result.option }}</span>
          </div>
          <div class="result-bar">
            <div 
              class="result-fill" 
              :style="{ width: `${result.percentage}%` }"
            ></div>
          </div>
          <div class="result-count">{{ result.count }} votes</div>
          <div class="result-select" v-if="canSelectWinner">
            <input
              class="winner-checkbox"
              type="checkbox"
              :value="resolveRawId(result)"
              :checked="modelValue === resolveRawId(result)"
              @change="onCheckboxChange($event, result)"
              aria-label="Select this option as winner"
            />
          </div>
        </div>
      </div>
      <div v-if="canSelectWinner" class="results-actions">
        <BaseButton
          variant="primary"
          size="small"
          :disabled="!modelValue"
          @click="$emit('end')"
        >
          End Voting
        </BaseButton>
      </div>
    </div>
  </div>
  
</template>

<script>
import BaseButton from '@/components/common/BaseButton.vue'

export default {
  name: 'VoteResultsPanel',
  components: { BaseButton },
  props: {
    results: { type: Array, default: () => [] },
    totalVotes: { type: Number, default: 0 },
    canSelectWinner: { type: Boolean, default: false },
    rawIdByFormatted: { type: Object, default: () => ({}) },
    modelValue: { type: String, default: '' }
  },
  emits: ['update:modelValue', 'end'],
  computed: {
    // Keep options consistently ordered by their raw UTC time ascending
    sortedResults() {
      const safe = Array.isArray(this.results) ? [...this.results] : []
      try {
        return safe.sort((a, b) => {
          const ra = this.resolveRawId(a)
          const rb = this.resolveRawId(b)
          const ta = ra ? Date.parse(ra) : 0
          const tb = rb ? Date.parse(rb) : 0
          return ta - tb
        })
      } catch (e) {
        return safe
      }
    }
  },
  mounted() {
    // Debug: initial prop snapshot
    console.log('[VoteResultsPanel] mounted', {
      canSelectWinner: this.canSelectWinner,
      totalVotes: this.totalVotes,
      modelValue: this.modelValue,
      results: this.results,
      rawIdByFormatted: this.rawIdByFormatted
    })
  },
  watch: {
    canSelectWinner(newVal, oldVal) {
      console.log('[VoteResultsPanel] canSelectWinner changed', { oldVal, newVal })
    },
    modelValue(newVal, oldVal) {
      console.log('[VoteResultsPanel] modelValue changed', { oldVal, newVal })
    },
    results: {
      handler(newVal) {
        console.log('[VoteResultsPanel] results updated', newVal)
      },
      deep: true
    }
  },
  methods: {
    resolveRawId(result) {
      // Expect mapping of formatted text -> raw UTC id
      const mapped = this.rawIdByFormatted?.[result?.option]
      if (!mapped) {
        console.warn('[VoteResultsPanel] resolveRawId: mapping missing for', result?.option, this.rawIdByFormatted)
      }
      return mapped || ''
    },
    onCheckboxChange(evt, result) {
      const rawId = this.resolveRawId(result)
      const checked = !!evt?.target?.checked
      const next = checked ? rawId : ''
      console.log('[VoteResultsPanel] onCheckboxChange ->', { checked, rawId, next })
      this.$emit('update:modelValue', next)
    }
  }
}
</script>

<style scoped>
.results-content {
  padding: 1rem 0;
}

.results-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
  padding: 1rem;
  background-color: var(--color-background-secondary);
  border-radius: 8px;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.summary-label {
  font-weight: 600;
  color: var(--color-text-secondary);
}

.summary-value {
  color: var(--color-text-primary);
  font-weight: 600;
}

.results-chart {
  display: grid;
  gap: 1rem;
}

.result-item {
  display: grid;
  grid-template-columns: 1fr 1.5fr 100px 40px;
  gap: 1rem;
  align-items: center;
}

.result-option-text {
  font-weight: 600;
  color: var(--color-text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.result-bar {
  height: 20px;
  background-color: var(--color-border);
  border-radius: 10px;
  overflow: hidden;
}

.result-fill {
  height: 100%;
  background-color: var(--color-primary);
  transition: width 0.3s ease;
}

.result-count {
  text-align: right;
  font-size: 0.9rem;
  color: var(--color-text-secondary);
}

.circle-select {
  position: relative;
  display: inline-flex;
  align-items: center;
  cursor: pointer;
}

.circle-select input {
  position: absolute;
  opacity: 0;
}

.circle-select .circle {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  border: 2px solid #000; /* ensure visible outline when not selected */
  background-color: #fff;
  display: inline-block;
}

.circle-select input:checked + .circle {
  border-color: var(--color-primary);
  box-shadow: inset 0 0 0 4px var(--color-primary);
}

/* Accessibility: show focus outline when keyboard navigating */
.circle-select input:focus + .circle {
  box-shadow: 0 0 0 2px rgba(0,0,0,0.5);
}

.results-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 1rem;
}

.empty-state {
  text-align: center;
  padding: 2rem;
  color: var(--color-text-secondary);
}

.empty-message {
  font-size: 1.1rem;
}

@media (max-width: 768px) {
  .result-item {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }
  .result-count { text-align: left; }
  .result-option-text {
    white-space: normal;
    overflow: visible;
    text-overflow: unset;
  }
}
</style>


