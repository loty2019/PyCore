<template>
  <div class="card">
    <h2>📷 Camera Control</h2>

    <div class="control-group">
      <label>Exposure (ms)</label>
      <input
        type="number"
        v-model.number="exposure"
        min="1"
        max="1000"
        @change="updateSettings"
      />
    </div>

    <div class="control-group">
      <label>Gain</label>
      <input
        type="number"
        v-model.number="gain"
        min="0.1"
        max="10"
        step="0.1"
        @change="updateSettings"
      />
    </div>

    <button
      @click="capture"
      :disabled="camera.isCapturing.value"
      class="btn btn-success w-full"
    >
      {{ camera.isCapturing.value ? 'Capturing...' : 'Capture Image' }}
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useMicroscopeStore } from '@/stores/microscope'
import { useCamera } from '@/composables/useCamera'

const store = useMicroscopeStore()
const camera = useCamera()

const exposure = ref(100)
const gain = ref(1.0)

onMounted(async () => {
  await camera.loadSettings()
  exposure.value = store.cameraSettings.exposure
  gain.value = store.cameraSettings.gain
})

async function updateSettings() {
  await camera.updateSettings({
    exposure: exposure.value,
    gain: gain.value
  })
}

async function capture() {
  await camera.captureImage({
    exposure: exposure.value,
    gain: gain.value
  })
}
</script>

<style scoped>
/* Component-specific styles are now handled by Tailwind classes */
</style>
