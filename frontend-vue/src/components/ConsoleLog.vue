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

    <button @click="store.clearLogs()" class="clear-btn">Clear Logs</button>
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
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 12px;
  background: #FFEBEE;
  color: #C62828;
  margin-bottom: 15px;
}

.websocket-status.connected {
  background: #E8F5E9;
  color: #2E7D32;
}

.log-container {
  background: #1e1e1e;
  color: #d4d4d4;
  padding: 15px;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  font-size: 12px;
  max-height: 300px;
  overflow-y: auto;
  margin-bottom: 10px;
}

.log-entry {
  margin-bottom: 5px;
}

.log-entry.error {
  color: #f44336;
}

.log-entry.success {
  color: #4CAF50;
}

.log-entry.info {
  color: #2196F3;
}

.log-entry.warning {
  color: #FF9800;
}

.clear-btn {
  width: 100%;
  padding: 8px;
  font-size: 12px;
  background: #666;
}

.clear-btn:hover {
  background: #555;
}
</style>
