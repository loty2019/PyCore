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
  display: flex;
  gap: 20px;
  align-items: center;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
}

.status-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #ccc;
  transition: background 0.3s;
}

.status-indicator.connected {
  background: #4CAF50;
}

.status-indicator.disconnected {
  background: #f44336;
}

.status-indicator.running {
  background: #4CAF50;
}

.status-indicator.stopped {
  background: #FF9800;
}
</style>
