<template>
  <div class="status-bar">
    <div class="status-item">
      <div :class="['status-indicator', store.systemStatus.camera]"></div>
      <span>Camera</span>
    </div>
    <div class="status-item">
      <div :class="['status-indicator', store.systemStatus.stage]"></div>
      <span>Stage</span>
    </div>
    <div class="status-item">
      <div :class="['status-indicator', store.systemStatus.database]"></div>
      <span>Database</span>
    </div>
    <div class="status-item">
      <div :class="['status-indicator', wsStore.state.isConnected ? 'connected' : 'disconnected']"></div>
      <span>WebSocket</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useMicroscopeStore } from '@/stores/microscope'
import { useWebSocketStore } from '@/stores/websocket'

const store = useMicroscopeStore()
const wsStore = useWebSocketStore()
</script>

<style scoped>
.status-bar {
  @apply flex gap-5 items-center;
}

.status-item {
  @apply flex items-center gap-2 text-sm;
}

.status-indicator {
  @apply w-3 h-3 rounded-full bg-gray-400 transition-colors;
}

.status-indicator.connected,
.status-indicator.running {
  @apply bg-green-500;
}

.status-indicator.disconnected {
  @apply bg-red-500;
}

.status-indicator.stopped {
  @apply bg-orange-500;
}
</style>
