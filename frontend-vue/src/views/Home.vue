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
  @apply max-w-screen-xl mx-auto p-5;
}

header {
  @apply bg-white p-5 rounded-lg mb-5 shadow-md;
}

header h1 {
  @apply text-gray-800 mb-2.5 text-3xl;
}

header p {
  @apply text-gray-600 mb-4;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  @apply gap-5 mb-5;
}
</style>
