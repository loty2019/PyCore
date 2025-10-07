import { ref } from 'vue'
import { controlAPI } from '@/api/client'
import { useMicroscopeStore } from '@/stores/microscope'

export function useStage() {
  const store = useMicroscopeStore()
  const isMoving = ref(false)

  async function move(x?: number, y?: number, z?: number, relative = false) {
    isMoving.value = true
    try {
      const result = await controlAPI.moveStage({ x, y, z, relative })

      const pos = result.target_position
      store.addLog(
        `Moving to X:${pos.x.toFixed(1)} Y:${pos.y.toFixed(1)} Z:${pos.z.toFixed(1)}`,
        'info'
      )

      return result
    } catch (error: any) {
      store.addLog(`Move failed: ${error.message}`, 'error')
      throw error
    } finally {
      isMoving.value = false
    }
  }

  async function home() {
    isMoving.value = true
    try {
      await controlAPI.homeStage()
      store.addLog('Homing all axes...', 'info')
    } catch (error: any) {
      store.addLog(`Home failed: ${error.message}`, 'error')
      throw error
    } finally {
      isMoving.value = false
    }
  }

  async function stop() {
    try {
      await controlAPI.emergencyStop()
      store.addLog('Emergency stop activated!', 'warning')
    } catch (error: any) {
      store.addLog(`Stop failed: ${error.message}`, 'error')
      throw error
    }
  }

  async function updatePosition() {
    try {
      const position = await controlAPI.getPosition()
      store.updatePosition(position)
    } catch (error: any) {
      console.error('Failed to update position:', error)
    }
  }

  return {
    isMoving,
    move,
    home,
    stop,
    updatePosition
  }
}
