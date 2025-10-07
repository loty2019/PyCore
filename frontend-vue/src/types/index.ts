export * from './api'

export interface LogEntry {
  timestamp: Date
  message: string
  type: 'info' | 'success' | 'error' | 'warning'
}

export interface WebSocketState {
  isConnected: boolean
  reconnectAttempts: number
  maxReconnectAttempts: number
}
