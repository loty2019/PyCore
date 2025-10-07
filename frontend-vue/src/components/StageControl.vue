<template>
  <div class="card">
    <h2>🎯 Stage Control</h2>

    <div class="position-display">
      <div>X: <span>{{ store.position.x.toFixed(1) }}</span></div>
      <div>Y: <span>{{ store.position.y.toFixed(1) }}</span></div>
      <div>Z: <span>{{ store.position.z.toFixed(1) }}</span></div>
    </div>

    <div class="stage-control">
      <div></div>
      <button @click="move(0, 100, 0)" :disabled="stage.isMoving.value">↑ Y+</button>
      <div></div>

      <button @click="move(-100, 0, 0)" :disabled="stage.isMoving.value">← X-</button>
      <button @click="stage.home()" class="center" :disabled="stage.isMoving.value">⌂ Home</button>
      <button @click="move(100, 0, 0)" :disabled="stage.isMoving.value">X+ →</button>

      <div></div>
      <button @click="move(0, -100, 0)" :disabled="stage.isMoving.value">↓ Y-</button>
      <div></div>
    </div>

    <div class="button-group">
      <button @click="move(0, 0, 10)" :disabled="stage.isMoving.value">Z+ ↑</button>
      <button @click="move(0, 0, -10)" :disabled="stage.isMoving.value">Z- ↓</button>
      <button @click="stage.stop()" class="danger">⛔ STOP</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'
import { useMicroscopeStore } from '@/stores/microscope'
import { useStage } from '@/composables/useStage'

const store = useMicroscopeStore()
const stage = useStage()

let intervalId: number | null = null

onMounted(() => {
  // Poll position every 2 seconds
  intervalId = window.setInterval(stage.updatePosition, 2000)
  stage.updatePosition()
})

onUnmounted(() => {
  if (intervalId) {
    clearInterval(intervalId)
  }
})

async function move(x: number, y: number, z: number) {
  await stage.move(x, y, z, true)
  setTimeout(stage.updatePosition, 500)
}
</script>

<style scoped>
.position-display {
  background: #f5f5f5;
  padding: 15px;
  border-radius: 4px;
  margin-bottom: 15px;
  font-family: monospace;
}

.position-display div {
  margin-bottom: 5px;
}

.stage-control {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  margin-bottom: 15px;
}

.stage-control button {
  padding: 15px;
}

.stage-control .center {
  background: #FF5722;
}

.stage-control .center:hover:not(:disabled) {
  background: #E64A19;
}

.button-group {
  display: flex;
  gap: 10px;
}

.button-group button {
  flex: 1;
}

button.danger {
  background: #f44336;
}

button.danger:hover {
  background: #d32f2f;
}
</style>
