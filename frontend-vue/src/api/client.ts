import axios from 'axios'
import type {
  SystemStatus,
  HealthCheck,
  Position,
  CameraSettings,
  CaptureRequest,
  CaptureResponse,
  MoveRequest,
  MoveResponse,
  ImageListResponse,
  Image,
  JobCreate,
  Job,
  JobListResponse,
  PositionCreate,
  SavedPosition,
  PositionListResponse
} from '@/types'

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Control endpoints
export const controlAPI = {
  async getStatus(): Promise<SystemStatus> {
    const { data } = await apiClient.get<SystemStatus>('/control/status')
    return data
  },

  async getHealth(): Promise<HealthCheck> {
    const { data } = await apiClient.get<HealthCheck>('/control/health')
    return data
  },

  async captureImage(request: CaptureRequest): Promise<CaptureResponse> {
    const { data } = await apiClient.post<CaptureResponse>('/control/capture', request)
    return data
  },

  async moveStage(request: MoveRequest): Promise<MoveResponse> {
    const { data } = await apiClient.post<MoveResponse>('/control/move', request)
    return data
  },

  async getPosition(): Promise<Position> {
    const { data } = await apiClient.get<Position>('/control/position')
    return data
  },

  async homeStage(): Promise<{ status: string; message: string }> {
    const { data } = await apiClient.post('/control/home')
    return data
  },

  async emergencyStop(): Promise<{ status: string; message: string }> {
    const { data } = await apiClient.post('/control/stop')
    return data
  },

  async getCameraSettings(): Promise<CameraSettings> {
    const { data } = await apiClient.get<CameraSettings>('/control/camera/settings')
    return data
  },

  async updateCameraSettings(settings: Partial<CameraSettings>): Promise<void> {
    await apiClient.put('/control/camera/settings', settings)
  }
}

// Image endpoints
export const imageAPI = {
  async listImages(params?: {
    skip?: number
    limit?: number
    job_id?: number
    start_date?: string
    end_date?: string
  }): Promise<ImageListResponse> {
    const { data } = await apiClient.get<ImageListResponse>('/images', { params })
    return data
  },

  async getImage(imageId: number): Promise<Image> {
    const { data } = await apiClient.get<Image>(`/images/${imageId}`)
    return data
  },

  async deleteImage(imageId: number): Promise<void> {
    await apiClient.delete(`/images/${imageId}`)
  }
}

// Job endpoints
export const jobAPI = {
  async listJobs(params?: {
    skip?: number
    limit?: number
    status?: string
    job_type?: string
  }): Promise<JobListResponse> {
    const { data } = await apiClient.get<JobListResponse>('/jobs', { params })
    return data
  },

  async createJob(job: JobCreate): Promise<Job> {
    const { data } = await apiClient.post<Job>('/jobs', job)
    return data
  },

  async getJob(jobId: number): Promise<Job> {
    const { data } = await apiClient.get<Job>(`/jobs/${jobId}`)
    return data
  },

  async updateJob(jobId: number, updates: { status?: string }): Promise<Job> {
    const { data } = await apiClient.patch<Job>(`/jobs/${jobId}`, updates)
    return data
  },

  async deleteJob(jobId: number): Promise<void> {
    await apiClient.delete(`/jobs/${jobId}`)
  }
}

// Position endpoints
export const positionAPI = {
  async listPositions(): Promise<PositionListResponse> {
    const { data } = await apiClient.get<PositionListResponse>('/positions')
    return data
  },

  async createPosition(position: PositionCreate): Promise<SavedPosition> {
    const { data } = await apiClient.post<SavedPosition>('/positions', position)
    return data
  },

  async getPosition(positionId: number): Promise<SavedPosition> {
    const { data } = await apiClient.get<SavedPosition>(`/positions/${positionId}`)
    return data
  },

  async gotoPosition(positionId: number): Promise<void> {
    await apiClient.post(`/positions/${positionId}/goto`)
  },

  async deletePosition(positionId: number): Promise<void> {
    await apiClient.delete(`/positions/${positionId}`)
  }
}

export default apiClient
