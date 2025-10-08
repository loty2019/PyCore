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
      <button @click="move(0, 100, 0)" :disabled="stage.isMoving.value" class="btn">↑ Y+</button>
      <div></div>

      <button @click="move(-100, 0, 0)" :disabled="stage.isMoving.value" class="btn">← X-</button>
      <button @click="stage.home()" class="center btn" :disabled="stage.isMoving.value">⌂ Home</button>
      <button @click="move(100, 0, 0)" :disabled="stage.isMoving.value" class="btn">X+ →</button>

      <div></div>
      <button @click="move(0, -100, 0)" :disabled="stage.isMoving.value" class="btn">↓ Y-</button>
      <div></div>
    </div>

    <div class="button-group">
      <button @click="move(0, 0, 10)" :disabled="stage.isMoving.value" class="btn">Z+ ↑</button>
      <button @click="move(0, 0, -10)" :disabled="stage.isMoving.value" class="btn">Z- ↓</button>
      <button @click="stage.stop()" class="btn btn-danger">⛔ STOP</button>
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
  @apply bg-gray-100 p-4 rounded mb-4 font-mono;
}

.position-display div {
  @apply mb-1;
}

.stage-control {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  @apply gap-2.5 mb-4;
}

.stage-control button {
  @apply p-4;
}

.stage-control .center {
  @apply bg-orange-600;
}

.stage-control .center:hover:not(:disabled) {
  @apply bg-orange-700;
}
</style>
