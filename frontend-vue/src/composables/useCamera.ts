import { ref } from 'vue'
import { controlAPI } from '@/api/client'
import { useMicroscopeStore } from '@/stores/microscope'
import type { CaptureRequest } from '@/types'

export function useCamera() {
  const store = useMicroscopeStore()
  const isCapturing = ref(false)

  async function captureImage(params?: CaptureRequest) {
    isCapturing.value = true
    try {
      const result = await controlAPI.captureImage({
        exposure: params?.exposure ?? store.cameraSettings.exposure,
        gain: params?.gain ?? store.cameraSettings.gain
      })

      store.addLog(`Image captured: ${result.filename}`, 'success')
      return result
    } catch (error: any) {
      store.addLog(`Capture failed: ${error.message}`, 'error')
      throw error
    } finally {
      isCapturing.value = false
    }
  }

  async function updateSettings(settings: { exposure?: number; gain?: number }) {
    try {
      await controlAPI.updateCameraSettings(settings)
      store.updateCameraSettings(settings)
      store.addLog('Camera settings updated', 'success')
    } catch (error: any) {
      store.addLog(`Failed to update settings: ${error.message}`, 'error')
      throw error
    }
  }

  async function loadSettings() {
    try {
      const settings = await controlAPI.getCameraSettings()
      store.updateCameraSettings(settings)
    } catch (error: any) {
      store.addLog(`Failed to load settings: ${error.message}`, 'error')
    }
  }

  return {
    isCapturing,
    captureImage,
    updateSettings,
    loadSettings
  }
}
