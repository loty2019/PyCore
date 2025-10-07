import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { WebSocketState } from '@/types'

export const useWebSocketStore = defineStore('websocket', () => {
  // State
  const state = ref<WebSocketState>({
    isConnected: false,
    reconnectAttempts: 0,
    maxReconnectAttempts: 5
  })

  // Actions
  function setConnected(connected: boolean) {
    state.value.isConnected = connected
  }

  function incrementReconnectAttempts() {
    state.value.reconnectAttempts++
  }

  function resetReconnectAttempts() {
    state.value.reconnectAttempts = 0
  }

  function canReconnect() {
    return state.value.reconnectAttempts < state.value.maxReconnectAttempts
  }

  return {
    state,
    setConnected,
    incrementReconnectAttempts,
    resetReconnectAttempts,
    canReconnect
  }
})
