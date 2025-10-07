import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type {
  SystemStatus,
  Position,
  CameraSettings,
  Image,
  Job,
  SavedPosition,
  LogEntry
} from '@/types'

export const useMicroscopeStore = defineStore('microscope', () => {
  // State
  const systemStatus = ref<SystemStatus>({
    camera: 'disconnected',
    stage: 'disconnected',
    database: 'disconnected',
    queue: 'stopped'
  })

  const position = ref<Position>({
    x: 0,
    y: 0,
    z: 0,
    is_moving: false
  })

  const cameraSettings = ref<CameraSettings>({
    exposure: 100,
    gain: 1.0,
    resolution: {
      width: 1920,
      height: 1080
    }
  })

  const images = ref<Image[]>([])
  const jobs = ref<Job[]>([])
  const savedPositions = ref<SavedPosition[]>([])
  const logs = ref<LogEntry[]>([])

  // Computed
  const isSystemHealthy = computed(() =>
    systemStatus.value.camera === 'connected' &&
    systemStatus.value.stage === 'connected' &&
    systemStatus.value.database === 'connected'
  )

  const activeJobs = computed(() =>
    jobs.value.filter(job => job.status === 'running' || job.status === 'pending')
  )

  const recentImages = computed(() =>
    images.value.slice(0, 20)
  )

  // Actions
  function updateSystemStatus(status: Partial<SystemStatus>) {
    systemStatus.value = { ...systemStatus.value, ...status }
  }

  function updatePosition(pos: Position) {
    position.value = pos
  }

  function updateCameraSettings(settings: Partial<CameraSettings>) {
    cameraSettings.value = { ...cameraSettings.value, ...settings }
  }

  function addImage(image: Image) {
    images.value.unshift(image)
  }

  function setImages(imageList: Image[]) {
    images.value = imageList
  }

  function addJob(job: Job) {
    jobs.value.unshift(job)
  }

  function updateJob(jobId: number, updates: Partial<Job>) {
    const index = jobs.value.findIndex(j => j.id === jobId)
    if (index !== -1) {
      jobs.value[index] = { ...jobs.value[index], ...updates }
    }
  }

  function setJobs(jobList: Job[]) {
    jobs.value = jobList
  }

  function setSavedPositions(positions: SavedPosition[]) {
    savedPositions.value = positions
  }

  function addSavedPosition(position: SavedPosition) {
    savedPositions.value.push(position)
  }

  function removeSavedPosition(positionId: number) {
    savedPositions.value = savedPositions.value.filter(p => p.id !== positionId)
  }

  function addLog(message: string, type: LogEntry['type'] = 'info') {
    logs.value.push({
      timestamp: new Date(),
      message,
      type
    })

    // Keep only last 100 logs
    if (logs.value.length > 100) {
      logs.value = logs.value.slice(-100)
    }
  }

  function clearLogs() {
    logs.value = []
  }

  return {
    // State
    systemStatus,
    position,
    cameraSettings,
    images,
    jobs,
    savedPositions,
    logs,

    // Computed
    isSystemHealthy,
    activeJobs,
    recentImages,

    // Actions
    updateSystemStatus,
    updatePosition,
    updateCameraSettings,
    addImage,
    setImages,
    addJob,
    updateJob,
    setJobs,
    setSavedPositions,
    addSavedPosition,
    removeSavedPosition,
    addLog,
    clearLogs
  }
})
