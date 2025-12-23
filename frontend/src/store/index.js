import { create } from 'zustand';

const getInitialUserId = () => {
  if (typeof window !== 'undefined' && window.localStorage) {
    return localStorage.getItem('userId') || `user-${Date.now()}`;
  }
  return `user-${Date.now()}`;
};

export const useChatStore = create((set) => ({
  userId: getInitialUserId(),
  messages: [],
  isLoading: false,
  error: null,

  setUserId: (userId) => {
    if (typeof window !== 'undefined' && window.localStorage) {
      localStorage.setItem('userId', userId);
    }
    set({ userId });
  },

  addMessage: (message) => {
    set((state) => ({
      messages: [...state.messages, message],
    }));
  },

  setMessages: (messages) => {
    set({ messages });
  },

  setLoading: (isLoading) => {
    set({ isLoading });
  },

  setError: (error) => {
    set({ error });
  },

  clearMessages: () => {
    set({ messages: [] });
  },
}));

export const useResourceStore = create((set) => ({
  resources: [],
  selectedResource: null,
  isLoading: false,
  error: null,

  setResources: (resources) => {
    set({ resources });
  },

  setSelectedResource: (resource) => {
    set({ selectedResource: resource });
  },

  setLoading: (isLoading) => {
    set({ isLoading });
  },

  setError: (error) => {
    set({ error });
  },

  clearResources: () => {
    set({ resources: [], selectedResource: null });
  },
}));

export const useUserStore = create((set) => ({
  location: null,
  latitude: null,
  longitude: null,
  needs: [],
  eligibilityInfo: null,
  accessibilityNeeds: [],

  setLocation: (location) => {
    set({ location });
  },

  setLatitude: (latitude) => {
    set({ latitude });
  },

  setLongitude: (longitude) => {
    set({ longitude });
  },

  setNeeds: (needs) => {
    set({ needs });
  },

  setEligibilityInfo: (info) => {
    set({ eligibilityInfo: info });
  },

  setAccessibilityNeeds: (needs) => {
    set({ accessibilityNeeds: needs });
  },

  updateContext: (context) => {
    set((state) => ({
      location: context.location || state.location,
      latitude: context.latitude || state.latitude,
      longitude: context.longitude || state.longitude,
      needs: context.needs || state.needs,
      eligibilityInfo: context.eligibility_info || state.eligibilityInfo,
      accessibilityNeeds: context.accessibility_needs || state.accessibilityNeeds,
    }));
  },
}));
