<template>
  <div class="home">
    <header>
      <h1>🔬 Microscope Control System</h1>
      <p>Proof of Concept Interface</p>
      <StatusBar />
    </header>

    <div class="grid">
      <CameraControl />
      <StageControl />
      <JobManager />
    </div>

    <ImageGallery />

    <ConsoleLog />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useMicroscopeStore } from '@/stores/microscope'
import { controlAPI } from '@/api/client'
import { useWebSocket } from '@/composables/useWebSocket'
import StatusBar from '@/components/StatusBar.vue'
import CameraControl from '@/components/CameraControl.vue'
import StageControl from '@/components/StageControl.vue'
import JobManager from '@/components/JobManager.vue'
import ImageGallery from '@/components/ImageGallery.vue'
import ConsoleLog from '@/components/ConsoleLog.vue'

const store = useMicroscopeStore()

// Initialize WebSocket
useWebSocket()

onMounted(async () => {
  // Load initial status
  try {
    const status = await controlAPI.getStatus()
    store.updateSystemStatus(status)
  } catch (error: any) {
    store.addLog(`Failed to load system status: ${error.message}`, 'error')
  }
})
</script>

<style scoped>
.home {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

header {
  background: white;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

header h1 {
  color: #333;
  margin-bottom: 10px;
  font-size: 28px;
}

header p {
  color: #666;
  margin-bottom: 15px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}
</style>
