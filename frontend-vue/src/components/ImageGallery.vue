<template>
  <div class="card">
    <h2>🖼️ Recent Images</h2>

    <div class="image-gallery">
      <div
        v-for="image in store.recentImages"
        :key="image.id"
        class="image-item"
        :title="image.filename"
      >
        <span>{{ image.id }}</span>
      </div>
      <div v-if="store.images.length === 0" class="image-item empty">
        No images
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useMicroscopeStore } from '@/stores/microscope'
import { imageAPI } from '@/api/client'

const store = useMicroscopeStore()

onMounted(async () => {
  try {
    const result = await imageAPI.listImages({ limit: 20 })
    store.setImages(result.images)
  } catch (error: any) {
    store.addLog(`Failed to load images: ${error.message}`, 'error')
  }
})
</script>

<style scoped>
.image-gallery {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  @apply gap-2.5 max-h-96 overflow-y-auto;
}

.image-item {
  @apply aspect-square bg-gray-200 rounded flex items-center justify-center text-sm text-gray-600 cursor-pointer transition-colors;
}

.image-item:hover:not(.empty) {
  @apply bg-gray-300;
}

.image-item.empty {
  @apply cursor-default;
}
</style>
