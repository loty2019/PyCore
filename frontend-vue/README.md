# Microscope Control System - Vue 3 Frontend

Modern, TypeScript-based frontend for the Microscope Control System built with Vue 3, Vite, and Pinia.

## 🚀 Features

- **Vue 3 Composition API** with TypeScript
- **Pinia** for state management
- **Reusable Components** for camera, stage, jobs, and images
- **Real-time Updates** via WebSocket
- **Type-Safe API** with full TypeScript support
- **Responsive Design** with modern CSS

## 📦 Tech Stack

- **Framework**: Vue 3
- **Language**: TypeScript
- **Build Tool**: Vite
- **State Management**: Pinia
- **HTTP Client**: Axios
- **Utilities**: @vueuse/core
- **Router**: Vue Router

## 🏗️ Project Structure

```
frontend-vue/
├── src/
│   ├── api/                    # API client
│   │   └── client.ts           # Axios-based API client
│   ├── assets/                 # Static assets
│   │   └── main.css            # Global styles
│   ├── components/             # Reusable Vue components
│   │   ├── CameraControl.vue   # Camera control panel
│   │   ├── StageControl.vue    # Stage joystick control
│   │   ├── JobManager.vue      # Job creation & monitoring
│   │   ├── ImageGallery.vue    # Image list display
│   │   ├── ConsoleLog.vue      # Log viewer
│   │   └── StatusBar.vue       # System status indicators
│   ├── composables/            # Vue composables
│   │   ├── useWebSocket.ts     # WebSocket connection
│   │   ├── useCamera.ts        # Camera operations
│   │   └── useStage.ts         # Stage operations
│   ├── router/                 # Vue Router
│   │   └── index.ts            # Route configuration
│   ├── stores/                 # Pinia stores
│   │   ├── microscope.ts       # Main application state
│   │   └── websocket.ts        # WebSocket state
│   ├── types/                  # TypeScript types
│   │   ├── api.ts              # API response types
│   │   └── index.ts            # Common types
│   ├── views/                  # Page components
│   │   └── Home.vue            # Main dashboard
│   ├── App.vue                 # Root component
│   └── main.ts                 # Application entry point
├── index.html                  # HTML template
├── package.json                # Dependencies
├── tsconfig.json               # TypeScript config
├── vite.config.ts              # Vite configuration
└── README.md                   # This file
```

## 🛠️ Installation

1. **Install dependencies:**
```bash
npm install
```

2. **Configure environment (optional):**
```bash
cp .env.example .env
```

3. **Run development server:**
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## 📝 Available Scripts

- **`npm run dev`** - Start development server with hot reload
- **`npm run build`** - Build for production
- **`npm run preview`** - Preview production build
- **`npm run type-check`** - Run TypeScript type checking

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```env
VITE_API_URL=/api
VITE_WS_URL=ws://localhost:8000/ws
```

### Vite Proxy

The Vite dev server is configured to proxy API requests to the backend:

```typescript
// vite.config.ts
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true
    },
    '/ws': {
      target: 'ws://localhost:8000',
      ws: true
    }
  }
}
```

## 🎨 Components

### CameraControl
- Exposure and gain controls
- Image capture button
- Real-time settings updates

### StageControl
- Joystick-style movement controls
- Position display (X/Y/Z)
- Home and emergency stop buttons

### JobManager
- Create timelapse, grid scan, or z-stack jobs
- Monitor job progress
- Pause/resume/cancel controls

### ImageGallery
- Display recent images
- Clickable thumbnails
- Auto-refresh on new captures

### ConsoleLog
- Real-time log display
- Color-coded message types
- WebSocket status indicator

## 🔌 API Integration

### Using the API Client

```typescript
import { controlAPI, imageAPI, jobAPI } from '@/api/client'

// Capture an image
const result = await controlAPI.captureImage({
  exposure: 100,
  gain: 1.5
})

// Move stage
await controlAPI.moveStage({
  x: 100,
  y: 50,
  z: 0,
  relative: true
})

// Create a job
const job = await jobAPI.createJob({
  name: 'My Timelapse',
  job_type: 'timelapse',
  parameters: {
    interval: 60,
    duration: 3600
  }
})
```

### Using Composables

```typescript
import { useCamera, useStage } from '@/composables'

const camera = useCamera()
const stage = useStage()

// Capture image
await camera.captureImage()

// Move stage
await stage.move(100, 50, 0, true)
```

## 🔄 State Management

### Microscope Store

```typescript
import { useMicroscopeStore } from '@/stores/microscope'

const store = useMicroscopeStore()

// Access state
console.log(store.position)
console.log(store.cameraSettings)
console.log(store.images)

// Update state
store.updatePosition({ x: 100, y: 50, z: 0 })
store.addLog('Image captured', 'success')
```

### WebSocket Store

```typescript
import { useWebSocketStore } from '@/stores/websocket'

const wsStore = useWebSocketStore()

// Check connection
if (wsStore.state.isConnected) {
  console.log('WebSocket connected')
}
```

## 📡 WebSocket Integration

WebSocket connection is automatically managed by the `useWebSocket` composable:

```typescript
// Automatically connects on mount
const { isConnected, send } = useWebSocket()

// Send message
send({ type: 'ping' })
```

Incoming messages are automatically routed to the appropriate handlers:
- **position** → Updates position in store
- **job_progress** → Updates job progress
- **image_captured** → Adds log entry
- **status** → Updates system status
- **error** → Logs error message

## 🎯 Type Safety

All API responses and components are fully typed:

```typescript
import type { Position, Image, Job } from '@/types'

const position: Position = {
  x: 0,
  y: 0,
  z: 0,
  is_moving: false
}
```

## 🚀 Production Build

1. **Build the application:**
```bash
npm run build
```

2. **Preview the build:**
```bash
npm run preview
```

3. **Deploy the `dist` folder** to your web server or copy it to the backend's static folder

## 🔍 Troubleshooting

### API requests fail
- Ensure backend is running on `http://localhost:8000`
- Check Vite proxy configuration
- Verify CORS settings on backend

### WebSocket won't connect
- Check WebSocket URL in `.env`
- Ensure backend WebSocket endpoint is accessible
- Check browser console for errors

### TypeScript errors
- Run `npm run type-check`
- Ensure all types are properly imported
- Check `tsconfig.json` settings

## 📚 Learn More

- [Vue 3 Documentation](https://vuejs.org/)
- [Vite Documentation](https://vitejs.dev/)
- [Pinia Documentation](https://pinia.vuejs.org/)
- [TypeScript Documentation](https://www.typescriptlang.org/)
- [VueUse Documentation](https://vueuse.org/)

## 🤝 Contributing

This is a proof of concept. For production improvements:
- Add comprehensive error handling
- Implement unit tests (Vitest)
- Add E2E tests (Playwright/Cypress)
- Improve accessibility (ARIA labels)
- Add internationalization (i18n)

## 📄 License

MIT
