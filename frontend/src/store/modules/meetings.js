import { defineStore } from 'pinia'
import { meetingsAPI } from '../../api/meetings.js'

export const useMeetingsStore = defineStore('meetings', {
  state: () => ({
    meetings: [],
    currentMeeting: null,
    meetingMembers: [],
    meetingVotes: [],
    voteResults: {},
    userMeetings: [],
    loading: false,
    error: null
  }),

  getters: {
    // Main data getters
    allMeetings: (state) => state.meetings,
    
    // Computed getters
    userVote: (state) => state.meetingVotes.find(vote => vote.userId === 'current-user'), // TODO: Replace with actual user ID
    isVotingOpen: (state) => {
      if (!state.currentMeeting) return false
      const now = new Date()
      const start = new Date(state.currentMeeting.votingStart)
      const end = new Date(state.currentMeeting.votingEnd)
      return now >= start && now <= end
    },
    meetingCount: (state) => state.meetings.length,
    isLoading: (state) => state.loading,
    hasError: (state) => !!state.error
  },

  actions: {
    async fetchMeetings() {
      this.loading = true
      this.error = null
      
      try {
        const meetings = await meetingsAPI.getAllMeetings()
        this.meetings = Array.isArray(meetings) ? meetings : []
      } catch (error) {
        this.error = error.message
        console.error('Error fetching meetings:', error)
      } finally {
        this.loading = false
      }
    },

    async fetchMeeting(meetingId) {
      this.loading = true
      this.error = null
      
      try {
        const meeting = await meetingsAPI.getMeetingById(meetingId)
        if (meeting) this.currentMeeting = meeting
      } catch (error) {
        this.error = error.message
        console.error('Error fetching meeting:', error)
      } finally {
        this.loading = false
      }
    },

    async fetchMeetingMembers(meetingId) {
      this.loading = true
      this.error = null
      
      try {
        const members = await meetingsAPI.getMeetingMembers(meetingId)
        this.meetingMembers = Array.isArray(members) ? members : []
      } catch (error) {
        this.error = error.message
        console.error('Error fetching meeting members:', error)
      } finally {
        this.loading = false
      }
    },

    async fetchMeetingVotes(meetingId) {
      this.loading = true
      this.error = null
      
      try {
        const votes = await meetingsAPI.getMeetingVotes(meetingId)
        this.meetingVotes = Array.isArray(votes) ? votes : []
      } catch (error) {
        this.error = error.message
        console.error('Error fetching meeting votes:', error)
      } finally {
        this.loading = false
      }
    },

    async fetchVoteResults(meetingId) {
      this.loading = true
      this.error = null
      
      try {
        const results = await meetingsAPI.getVoteResults(meetingId)
        this.voteResults = results || {}
      } catch (error) {
        this.error = error.message
        console.error('Error fetching vote results:', error)
      } finally {
        this.loading = false
      }
    },

    async fetchUserMeetings() {
      this.loading = true
      this.error = null
      
      try {
        // Placeholder: derive from all meetings; in real app, use user teams
        const meetings = await meetingsAPI.getAllMeetings()
        this.userMeetings = Array.isArray(meetings) ? meetings.filter(m => m.teamId === '1') : []
      } catch (error) {
        this.error = error.message
        console.error('Error fetching user meetings:', error)
      } finally {
        this.loading = false
      }
    },

    async submitVote(meetingId, voteData) {
      this.loading = true
      this.error = null
      
      try {
        const newVote = await meetingsAPI.submitVote(meetingId, voteData)
        this.meetingVotes = (this.meetingVotes || []).filter(vote => !(vote.meetingId === meetingId && vote.userId === newVote.userId))
        this.meetingVotes.push(newVote)
        return newVote
      } catch (error) {
        this.error = error.message
        console.error('Error submitting vote:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    setCurrentMeeting(meeting) {
      this.currentMeeting = meeting
    },

    clearError() {
      this.error = null
    }
  }
})
