// src/store/modules/members.js
import { defineStore } from 'pinia';
import { fetchMembers, updateMember as updateMemberApi, updateAvailability as updateAvailabilityApi } from '@/api/members';

export const useMembersStore = defineStore('members', {
  state: () => ({
    members: [],
    currentMember: null,
    availability: {},
    loading: false,
    error: null
  }),

  getters: {
    allMembers: (state) => state.members,
    getMemberById: (state) => (id) => state.members.find(member => member.id === id),
    getAvailability: (state) => state.availability,
    isLoading: (state) => state.loading,
    hasError: (state) => !!state.error
  },

  actions: {
    async fetchMembers() {
      this.loading = true; this.error = null;
      try {
        const members = await fetchMembers();
        this.members = members;
      } catch (error) {
        this.error = error.message;
        console.error('Error fetching members:', error);
      } finally {
        this.loading = false;
      }
    },

    async updateAvailability(memberId, availability) {
      this.loading = true; this.error = null;
      try {
        const updated = await updateAvailabilityApi(memberId, availability);
        const idx = this.members.findIndex(m => m.id === memberId);
        if (idx !== -1) this.members[idx] = updated;
        this.availability[memberId] = availability;
      } catch (error) {
        this.error = error.message;
        console.error('Error updating availability:', error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async updateMember(memberId, updates) {
      this.loading = true; this.error = null;
      try {
        const updated = await updateMemberApi(memberId, updates);
        const idx = this.members.findIndex(m => m.id === memberId);
        if (idx !== -1) this.members[idx] = updated;
      } catch (error) {
        this.error = error.message;
        console.error('Error updating member:', error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    setCurrentMember(member) { this.currentMember = member; },
    setAvailability(availability) { this.availability = availability; },
    clearError() { this.error = null; }
  }
});