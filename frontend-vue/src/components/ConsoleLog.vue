<template>
  <div class="card">
    <h2>📋 Console</h2>

    <div class="websocket-status" :class="{ connected: wsStore.state.isConnected }">
      WebSocket: {{ wsStore.state.isConnected ? 'Connected' : 'Disconnected' }}
    </div>

    <div class="log-container" ref="logContainer">
      <div
        v-for="(log, index) in store.logs"
        :key="index"
        :class="['log-entry', log.type]"
      >
        [{{ formatTime(log.timestamp) }}] {{ log.message }}
      </div>
    </div>

    <button @click="store.clearLogs()" class="btn clear-btn">Clear Logs</button>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'
import { useMicroscopeStore } from '@/stores/microscope'
import { useWebSocketStore } from '@/stores/websocket'

const store = useMicroscopeStore()
const wsStore = useWebSocketStore()
const logContainer = ref<HTMLElement | null>(null)

function formatTime(date: Date): string {
  return date.toLocaleTimeString()
}

// Auto-scroll to bottom when new logs arrive
watch(() => store.logs.length, async () => {
  await nextTick()
  if (logContainer.value) {
    logContainer.value.scrollTop = logContainer.value.scrollHeight
  }
})
</script>

<style scoped>
.websocket-status {
  @apply px-3 py-2 rounded text-xs bg-red-50 text-red-800 mb-4;
}

.websocket-status.connected {
  @apply bg-green-50 text-green-800;
}

.log-container {
  @apply bg-gray-900 text-gray-300 p-4 rounded font-mono text-xs max-h-[300px] overflow-y-auto mb-2.5;
}

.log-entry {
  @apply mb-1;
}

.log-entry.error {
  @apply text-red-500;
}

.log-entry.success {
  @apply text-green-500;
}

.log-entry.info {
  @apply text-blue-500;
}

.log-entry.warning {
  @apply text-orange-500;
}

.clear-btn {
  @apply w-full py-2 text-xs bg-gray-600;
}

.clear-btn:hover {
  @apply bg-gray-700;
}
</style>
