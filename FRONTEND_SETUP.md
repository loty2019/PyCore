# Vue 3 TypeScript Frontend Setup Guide

Complete guide for setting up and running the modern Vue 3 frontend.

## 🎯 Overview

The new frontend is a complete rewrite using:
- **Vue 3** with Composition API
- **TypeScript** for type safety
- **Vite** for fast development
- **Pinia** for state management
- **Reusable components** for better maintainability

## 📋 Prerequisites

- Node.js 18+
- npm or yarn
- Backend server running on `http://localhost:8000`

## 🚀 Quick Start

### 1. Navigate to frontend directory

```bash
cd C:\Users\loren\Desktop\Link\PyCore\frontend-vue
```

### 2. Install dependencies

```bash
npm install
```

This will install:
- Vue 3
- TypeScript
- Vite
- Pinia (state management)
- Vue Router
- Axios (HTTP client)
- @vueuse/core (utilities)

### 3. Start development server

```bash
npm run dev
```

The application will be available at `http://localhost:5173`

### 4. Open in browser

Navigate to `http://localhost:5173` and you should see the microscope control interface.

## 🔧 Configuration

### Environment Variables

Create a `.env` file in `frontend-vue/` (optional):

```env
VITE_API_URL=/api
VITE_WS_URL=ws://localhost:8000/ws
```

The default configuration uses Vite's proxy, so this is optional for development.

## 📁 Project Structure

```
frontend-vue/
├── src/
│   ├── api/                    # API client (Axios)
│   ├── assets/                 # Styles & static files
│   ├── components/             # Reusable Vue components
│   │   ├── CameraControl.vue
│   │   ├── StageControl.vue
│   │   ├── JobManager.vue
│   │   ├── ImageGallery.vue
│   │   ├── ConsoleLog.vue
│   │   └── StatusBar.vue
│   ├── composables/            # Reusable composition functions
│   │   ├── useWebSocket.ts
│   │   ├── useCamera.ts
│   │   └── useStage.ts
│   ├── stores/                 # Pinia stores
│   │   ├── microscope.ts
│   │   └── websocket.ts
│   ├── types/                  # TypeScript type definitions
│   ├── views/                  # Page components
│   ├── router/                 # Vue Router configuration
│   ├── App.vue                 # Root component
│   └── main.ts                 # Entry point
├── package.json
├── tsconfig.json
├── vite.config.ts
└── README.md
```

## 🎨 Key Features

### 1. Type-Safe API Client

All API calls are fully typed:

```typescript
import { controlAPI } from '@/api/client'

// TypeScript knows the response type
const result = await controlAPI.captureImage({
  exposure: 100,
  gain: 1.5
})
```

### 2. Reusable Composables

```typescript
import { useCamera, useStage } from '@/composables'

const camera = useCamera()
const stage = useStage()

await camera.captureImage()
await stage.move(100, 50, 0, true)
```

### 3. Centralized State Management

```typescript
import { useMicroscopeStore } from '@/stores/microscope'

const store = useMicroscopeStore()

// Reactive state
console.log(store.position)
console.log(store.cameraSettings)
console.log(store.images)
```

### 4. Automatic WebSocket Connection

WebSocket connection is managed automatically:

```typescript
// In your component
const { isConnected } = useWebSocket()

// Messages are automatically routed to the store
```

## 🛠️ Development

### Available Commands

```bash
# Start dev server with hot reload
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Type check
npm run type-check
```

### Adding New Components

1. Create component in `src/components/`
2. Import and use in views
3. TypeScript will provide full intellisense

Example:

```vue
<template>
  <div class="my-component">
    <h2>{{ title }}</h2>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title: string
}>()
</script>

<style scoped>
.my-component {
  padding: 20px;
}
</style>
```

### Adding API Endpoints

1. Define types in `src/types/api.ts`
2. Add API method in `src/api/client.ts`
3. Use in components or composables

```typescript
// src/types/api.ts
export interface MyData {
  id: number
  name: string
}

// src/api/client.ts
export const myAPI = {
  async getData(): Promise<MyData> {
    const { data } = await apiClient.get<MyData>('/my-endpoint')
    return data
  }
}
```

## 📦 Production Build

### 1. Build the application

```bash
npm run build
```

This creates an optimized production build in the `dist/` folder.

### 2. Copy to backend (Option A)

```bash
# Copy dist folder to backend static directory
xcopy /E /I /Y dist ..\backend\static
```

### 3. Deploy separately (Option B)

Deploy the `dist/` folder to:
- Netlify
- Vercel
- AWS S3 + CloudFront
- Any static hosting service

Update the API URLs to point to your backend server.

## 🔗 Integration with Backend

### Development (Automatic Proxy)

Vite automatically proxies API requests:

```typescript
// vite.config.ts
server: {
  proxy: {
    '/api': 'http://localhost:8000',
    '/ws': {
      target: 'ws://localhost:8000',
      ws: true
    }
  }
}
```

No additional configuration needed!

### Production

Update environment variables to point to your backend:

```env
VITE_API_URL=https://your-backend.com/api
VITE_WS_URL=wss://your-backend.com/ws
```

## 🐛 Troubleshooting

### Port already in use

```bash
# Kill process on port 5173
npx kill-port 5173

# Or use a different port
npm run dev -- --port 3000
```

### TypeScript errors

```bash
# Run type check
npm run type-check

# Fix common issues
npm install
```

### API requests fail

1. Ensure backend is running on `http://localhost:8000`
2. Check browser console for CORS errors
3. Verify proxy configuration in `vite.config.ts`

### WebSocket won't connect

1. Check backend WebSocket endpoint is running
2. Verify WS URL in browser console
3. Check for connection errors in Network tab

### Dependencies won't install

```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

## 🔄 Migration from Old Frontend

The old `frontend/index.html` is still available but the new Vue frontend provides:

✅ **Better organization** - Separate files for components
✅ **Type safety** - Full TypeScript support
✅ **Reusability** - Composable functions and components
✅ **Better dev experience** - Hot reload, debugging
✅ **Production ready** - Optimized builds

To switch:
1. Keep old frontend as backup
2. Run new Vue frontend on port 5173
3. Test all features
4. Deploy when ready

## 📚 Learn More

- [Vue 3 Docs](https://vuejs.org/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Vite Guide](https://vitejs.dev/guide/)
- [Pinia Docs](https://pinia.vuejs.org/)

## 🎯 Next Steps

1. **Test all features** with backend running
2. **Customize styling** in `src/assets/main.css`
3. **Add more views** for advanced features
4. **Implement tests** with Vitest
5. **Add error boundaries** for better UX

## 📝 Notes

- The Vue app runs on port **5173** by default
- Backend should run on port **8000**
- WebSocket connects automatically on mount
- All state is managed through Pinia stores
- Components are fully typed with TypeScript

---

**Need help?** Check the README.md in `frontend-vue/` folder or the main project documentation.
