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
  gap: 10px;
  max-height: 400px;
  overflow-y: auto;
}

.image-item {
  aspect-ratio: 1;
  background: #f0f0f0;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  color: #666;
  cursor: pointer;
  transition: background 0.2s;
}

.image-item:hover:not(.empty) {
  background: #e0e0e0;
}

.image-item.empty {
  cursor: default;
}
</style>
