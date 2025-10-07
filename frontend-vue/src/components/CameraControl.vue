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
      class="success"
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
.card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.card h2 {
  color: #333;
  margin-bottom: 15px;
  font-size: 18px;
  border-bottom: 2px solid #2196F3;
  padding-bottom: 8px;
}

.control-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  color: #666;
  font-size: 14px;
}

input[type="number"] {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

button {
  background: #2196F3;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.3s;
  width: 100%;
}

button:hover:not(:disabled) {
  background: #1976D2;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

button.success {
  background: #4CAF50;
}

button.success:hover:not(:disabled) {
  background: #45a049;
}
</style>
