import { ref, onMounted, onUnmounted } from 'vue'
import { useMicroscopeStore } from '@/stores/microscope'
import { useWebSocketStore } from '@/stores/websocket'
import type { WSMessage } from '@/types'

export function useWebSocket() {
  const microscopeStore = useMicroscopeStore()
  const wsStore = useWebSocketStore()

  const ws = ref<WebSocket | null>(null)
  const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws'

  function connect() {
    if (ws.value?.readyState === WebSocket.OPEN) {
      return
    }

    try {
      ws.value = new WebSocket(WS_URL)

      ws.value.onopen = () => {
        wsStore.setConnected(true)
        wsStore.resetReconnectAttempts()
        microscopeStore.addLog('WebSocket connected', 'success')
      }

      ws.value.onmessage = (event) => {
        const message: WSMessage = JSON.parse(event.data)
        handleMessage(message)
      }

      ws.value.onclose = () => {
        wsStore.setConnected(false)
        microscopeStore.addLog('WebSocket disconnected', 'error')

        // Attempt to reconnect
        if (wsStore.canReconnect()) {
          wsStore.incrementReconnectAttempts()
          setTimeout(connect, 5000)
        }
      }

      ws.value.onerror = (error) => {
        console.error('WebSocket error:', error)
        microscopeStore.addLog('WebSocket error occurred', 'error')
      }
    } catch (error) {
      console.error('Failed to connect WebSocket:', error)
      microscopeStore.addLog('Failed to connect WebSocket', 'error')
    }
  }

  function disconnect() {
    if (ws.value) {
      ws.value.close()
      ws.value = null
    }
  }

  function send(data: any) {
    if (ws.value?.readyState === WebSocket.OPEN) {
      ws.value.send(JSON.stringify(data))
    }
  }

  function handleMessage(message: WSMessage) {
    switch (message.type) {
      case 'position':
        microscopeStore.updatePosition(message.data)
        break

      case 'job_progress':
        microscopeStore.updateJob(message.data.job_id, {
          progress: message.data.progress,
          total_steps: message.data.total_steps,
          status: message.data.status as any
        })
        microscopeStore.addLog(
          `Job ${message.data.job_id}: ${message.data.progress}/${message.data.total_steps}`,
          'info'
        )
        break

      case 'image_captured':
        microscopeStore.addLog(
          `Image captured: ${message.data.filename}`,
          'success'
        )
        // Optionally refresh image list
        break

      case 'status':
        microscopeStore.updateSystemStatus({
          camera: message.data.camera,
          stage: message.data.stage
        })
        break

      case 'error':
        microscopeStore.addLog(
          `${message.data.component}: ${message.data.message}`,
          'error'
        )
        break

      case 'echo':
        // Echo response - can be used for testing
        break
    }
  }

  onMounted(() => {
    connect()
  })

  onUnmounted(() => {
    disconnect()
  })

  return {
    isConnected: () => wsStore.state.isConnected,
    connect,
    disconnect,
    send
  }
}
