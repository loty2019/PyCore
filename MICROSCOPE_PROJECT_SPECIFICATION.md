# Microscope Control System - Complete Project Specification

## Project Overview

Build a web-based microscope control system that allows remote control of a microscope camera, motorized stage (X/Y/Z axes), and automated job execution. The system must support real-time monitoring, image capture, and job scheduling accessible from any web browser.

---

## Technology Stack

### Backend
- **Language:** Python 3.11+
- **Web Framework:** FastAPI
- **Database:** PostgreSQL 16
- **ORM:** SQLAlchemy 2.0
- **Migrations:** Alembic
- **Camera Control:** OpenCV (or manufacturer SDK)
- **Image Processing:** Pillow, NumPy
- **API Documentation:** Swagger/OpenAPI (automatic with FastAPI)

### Frontend
- **Framework:** Vue 3 with Composition API
- **Language:** TypeScript
- **Build Tool:** Vite
- **State Management:** Pinia
- **Utilities:** VueUse (for WebSocket and hardware control)
- **Styling:** CSS with scoped styles
- **HTTP Client:** Axios or Fetch API

### Hardware Communication
- **Windows PC:** FastAPI backend controls camera directly
- **Raspberry Pi 5:** Python Flask service for motor control (GPIO)
- **Communication:** HTTP REST API between Windows PC and RPi

### DevOps
- **Version Control:** Git + GitHub
- **CI/CD:** GitHub Actions
- **Testing:** Pytest (backend), Vitest (frontend)
- **Code Quality:** Black, Flake8, ESLint, Prettier

---

## System Architecture

```
┌─────────────────────────────────────────┐
│  Web Browser (Any Device)              │
│  - Vue 3 TypeScript Frontend            │
│  - Image viewer, controls, job manager │
└──────────────┬──────────────────────────┘
               │ HTTPS/WebSocket
               ▼
┌─────────────────────────────────────────┐
│  Windows PC - FastAPI Backend           │
│  - Camera control (OpenCV)              │
│  - PostgreSQL database                  │
│  - Image storage & processing           │
│  - Job queue management                 │
│  - Serves frontend static files         │
└──────────────┬──────────────────────────┘
               │ HTTP REST API
               ▼
┌─────────────────────────────────────────┐
│  Raspberry Pi 5 - Motor Controller      │
│  - Python Flask service                 │
│  - GPIO control (stepper motors)        │
│  - Sensor reading                       │
│  - Position tracking                    │
└─────────────────────────────────────────┘
```

---

## Project Structure

```
microscope-project/
├── .env                          # Environment variables (SECRET - not in git)
├── .gitignore                    # Git ignore rules
├── .pre-commit-config.yaml       # Pre-commit hooks configuration
├── README.md                     # Project documentation
├── requirements.txt              # Python dependencies (production)
│
├── .github/
│   └── workflows/
│       ├── backend-ci.yml        # Backend CI pipeline
│       ├── frontend-ci.yml       # Frontend CI pipeline
│       └── deploy.yml            # Deployment pipeline
│
├── backend/
│   ├── __init__.py
│   ├── main.py                   # FastAPI application entry point
│   ├── config.py                 # Configuration management (Pydantic Settings)
│   ├── requirements.txt          # Backend production dependencies
│   ├── requirements-dev.txt      # Backend dev dependencies (pytest, etc.)
│   │
│   ├── alembic/                  # Database migrations
│   │   ├── versions/             # Migration files
│   │   ├── env.py                # Alembic environment
│   │   └── alembic.ini           # Alembic configuration
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── base.py               # SQLAlchemy base
│   │   ├── session.py            # Database session management
│   │   └── models.py             # Database models (Image, Job, Position, etc.)
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py               # Dependency injection (get_db, etc.)
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── images.py         # Image CRUD endpoints
│   │       ├── jobs.py           # Job management endpoints
│   │       ├── control.py        # Camera & stage control endpoints
│   │       ├── positions.py      # Saved positions endpoints
│   │       └── websocket.py      # WebSocket for real-time updates
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── image.py              # Pydantic schemas for images
│   │   ├── job.py                # Pydantic schemas for jobs
│   │   ├── control.py            # Pydantic schemas for control commands
│   │   └── position.py           # Pydantic schemas for positions
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── camera.py             # Camera control service
│   │   ├── stage.py              # Raspberry Pi communication service
│   │   ├── job_queue.py          # Job execution engine
│   │   ├── image_service.py      # Image saving, thumbnail generation
│   │   └── websocket_manager.py  # WebSocket connection manager
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── security.py           # Authentication (future)
│   │   ├── watchdog.py           # Safety monitoring & timeouts
│   │   └── logging.py            # Logging configuration
│   │
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py           # Pytest fixtures
│   │   ├── test_api_images.py
│   │   ├── test_api_jobs.py
│   │   ├── test_api_control.py
│   │   ├── test_camera.py
│   │   └── test_stage.py
│   │
│   └── static/                   # Served frontend files (after build)
│       ├── index.html
│       ├── assets/
│       └── ...
│
├── frontend/
│   ├── package.json              # Node.js dependencies
│   ├── package-lock.json
│   ├── tsconfig.json             # TypeScript configuration
│   ├── vite.config.ts            # Vite build configuration
│   ├── .eslintrc.cjs             # ESLint configuration
│   ├── .prettierrc.json          # Prettier configuration
│   │
│   ├── public/                   # Static assets
│   │   └── favicon.ico
│   │
│   ├── src/
│   │   ├── main.ts               # Application entry point
│   │   ├── App.vue               # Root component
│   │   │
│   │   ├── api/
│   │   │   └── client.ts         # API client (Axios/Fetch wrapper)
│   │   │
│   │   ├── stores/
│   │   │   ├── microscope.ts     # Main application state (Pinia)
│   │   │   └── websocket.ts      # WebSocket state
│   │   │
│   │   ├── components/
│   │   │   ├── ImageViewer.vue   # Image display with zoom/pan
│   │   │   ├── ImageGallery.vue  # Image list/grid
│   │   │   ├── StageControl.vue  # Joystick-like stage control
│   │   │   ├── CameraSettings.vue # Camera exposure, gain controls
│   │   │   ├── JobManager.vue    # Job creation & monitoring
│   │   │   ├── JobProgress.vue   # Progress bar for running jobs
│   │   │   ├── PositionList.vue  # Saved positions
│   │   │   └── StatusIndicator.vue # Connection status
│   │   │
│   │   ├── views/
│   │   │   ├── Home.vue          # Main dashboard
│   │   │   ├── Images.vue        # Image management view
│   │   │   ├── Jobs.vue          # Job management view
│   │   │   └── Settings.vue      # System settings
│   │   │
│   │   ├── composables/
│   │   │   ├── useWebSocket.ts   # WebSocket composable
│   │   │   └── useCamera.ts      # Camera control composable
│   │   │
│   │   ├── types/
│   │   │   ├── api.ts            # TypeScript types (can be auto-generated)
│   │   │   └── index.ts          # Common types
│   │   │
│   │   ├── router/
│   │   │   └── index.ts          # Vue Router configuration
│   │   │
│   │   └── assets/
│   │       └── styles/
│   │           └── main.css      # Global styles
│   │
│   ├── tests/
│   │   ├── unit/
│   │   │   ├── ImageViewer.spec.ts
│   │   │   ├── StageControl.spec.ts
│   │   │   └── JobManager.spec.ts
│   │   └── e2e/
│   │       └── basic.spec.ts
│   │
│   └── dist/                     # Build output (created by npm run build)
│
├── raspberry_pi/
│   ├── motor_controller.py       # Flask service for GPIO control
│   ├── config.py                 # RPi configuration
│   ├── requirements.txt          # RPi Python dependencies
│   └── systemd/
│       └── motor-controller.service # Systemd service file
│
├── deploy/
│   ├── deploy.ps1                # PowerShell deployment script (Windows)
│   ├── rollback.ps1              # Rollback script
│   └── health-check.py           # Post-deployment health check
│
├── scripts/
│   ├── setup-database.sql        # Initial database setup
│   ├── init-project.sh           # Project initialization script
│   └── generate-types.sh         # Generate TypeScript types from OpenAPI
│
├── images/                       # Captured images (auto-created)
├── thumbnails/                   # Image thumbnails (auto-created)
└── logs/                         # Application logs (auto-created)
```

---

## Database Schema (PostgreSQL)

### Table: `images`
Stores metadata about captured images.

```sql
CREATE TABLE images (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL UNIQUE,
    thumbnail_path VARCHAR(255),
    captured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Position when captured
    x_position FLOAT,
    y_position FLOAT,
    z_position FLOAT,
    
    -- Camera settings
    exposure_time INTEGER,  -- milliseconds
    gain FLOAT,
    
    -- File information
    file_size INTEGER,  -- bytes
    width INTEGER,      -- pixels
    height INTEGER,     -- pixels
    
    -- Relationship to job
    job_id INTEGER REFERENCES jobs(id) ON DELETE SET NULL,
    
    -- Additional metadata (JSON)
    metadata JSONB DEFAULT '{}',
    
    CONSTRAINT valid_position CHECK (
        x_position >= 0 AND y_position >= 0 AND z_position >= 0
    )
);

CREATE INDEX idx_images_captured_at ON images(captured_at DESC);
CREATE INDEX idx_images_job_id ON images(job_id);
```

### Table: `jobs`
Automated job tracking (timelapse, grid scans, z-stacks).

```sql
CREATE TABLE jobs (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    
    -- Job type: 'timelapse', 'grid', 'zstack', 'manual'
    job_type VARCHAR(50) NOT NULL,
    
    -- Status: 'pending', 'running', 'paused', 'completed', 'failed', 'cancelled'
    status VARCHAR(50) DEFAULT 'pending',
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    
    -- Progress tracking
    progress INTEGER DEFAULT 0,
    total_steps INTEGER,
    
    -- Job-specific parameters (JSON)
    -- Example: {"start_x": 0, "end_x": 1000, "step_x": 100, "interval": 60}
    parameters JSONB DEFAULT '{}',
    
    -- Error handling
    error_message TEXT,
    retry_count INTEGER DEFAULT 0
);

CREATE INDEX idx_jobs_status ON jobs(status);
CREATE INDEX idx_jobs_created_at ON jobs(created_at DESC);
CREATE INDEX idx_jobs_type ON jobs(job_type);
```

### Table: `positions`
Saved positions for quick navigation.

```sql
CREATE TABLE positions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    
    -- 3D coordinates
    x_position FLOAT NOT NULL,
    y_position FLOAT NOT NULL,
    z_position FLOAT NOT NULL,
    
    -- Optional: camera settings at this position
    camera_settings JSONB DEFAULT '{}',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT valid_position CHECK (
        x_position >= 0 AND y_position >= 0 AND z_position >= 0
    )
);

CREATE INDEX idx_positions_name ON positions(name);
```

### Table: `system_logs`
System event logging for debugging and audit trail.

```sql
CREATE TABLE system_logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Level: 'debug', 'info', 'warning', 'error', 'critical'
    level VARCHAR(20) NOT NULL,
    
    -- Component: 'camera', 'stage', 'web', 'job', 'watchdog'
    component VARCHAR(50) NOT NULL,
    
    message TEXT NOT NULL,
    
    -- Additional structured data
    details JSONB DEFAULT '{}'
);

CREATE INDEX idx_logs_timestamp ON system_logs(timestamp DESC);
CREATE INDEX idx_logs_level ON system_logs(level);
CREATE INDEX idx_logs_component ON system_logs(component);
```

### Table: `settings`
Persistent application settings.

```sql
CREATE TABLE settings (
    key VARCHAR(100) PRIMARY KEY,
    value JSONB NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT
);

-- Trigger to update updated_at automatically
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_settings_updated_at
    BEFORE UPDATE ON settings
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

---

## API Endpoints Specification

### Base URL: `http://localhost:8000`

### Health & Status

#### `GET /api/status`
Get system status.

**Response:**
```json
{
  "camera": "connected",
  "stage": "connected",
  "database": "connected",
  "queue": "running"
}
```

#### `GET /api/health`
Detailed health check for monitoring.

**Response:**
```json
{
  "status": "healthy",
  "checks": {
    "database": true,
    "raspberry_pi": true,
    "camera": true
  },
  "version": "1.0.0",
  "timestamp": "2025-10-06T10:30:00Z"
}
```

---

### Camera Control

#### `POST /api/control/capture`
Capture an image.

**Request:**
```json
{
  "exposure": 100,
  "gain": 1.5
}
```

**Response:**
```json
{
  "status": "success",
  "image_id": 123,
  "filename": "/images/image_123.jpg",
  "thumbnail_path": "/thumbnails/thumb_123.jpg",
  "timestamp": "2025-10-06T10:30:00Z"
}
```

#### `GET /api/control/camera/settings`
Get current camera settings.

**Response:**
```json
{
  "exposure": 100,
  "gain": 1.5,
  "resolution": {"width": 1920, "height": 1080},
  "available_resolutions": [
    {"width": 1920, "height": 1080},
    {"width": 1280, "height": 720}
  ]
}
```

#### `PUT /api/control/camera/settings`
Update camera settings.

**Request:**
```json
{
  "exposure": 150,
  "gain": 2.0
}
```

---

### Stage Control

#### `POST /api/control/move`
Move the stage.

**Request:**
```json
{
  "x": 1000,
  "y": 500,
  "z": 100,
  "relative": false
}
```

**Parameters:**
- `x`, `y`, `z`: Position in steps (optional, at least one required)
- `relative`: If true, move relative to current position

**Response:**
```json
{
  "status": "moving",
  "target_position": {
    "x": 1000,
    "y": 500,
    "z": 100
  }
}
```

#### `GET /api/control/position`
Get current stage position.

**Response:**
```json
{
  "x": 1000,
  "y": 500,
  "z": 100,
  "is_moving": false
}
```

#### `POST /api/control/home`
Home all axes.

**Response:**
```json
{
  "status": "homing",
  "message": "Homing in progress"
}
```

#### `POST /api/control/stop`
Emergency stop - halt all movement immediately.

**Response:**
```json
{
  "status": "stopped",
  "message": "All movement stopped"
}
```

---

### Images

#### `GET /api/images`
List images with pagination.

**Query Parameters:**
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum records to return (default: 50)
- `job_id`: Filter by job ID (optional)
- `start_date`: Filter by start date (ISO format, optional)
- `end_date`: Filter by end date (ISO format, optional)

**Response:**
```json
{
  "total": 100,
  "skip": 0,
  "limit": 50,
  "images": [
    {
      "id": 1,
      "filename": "/images/image_001.jpg",
      "thumbnail_path": "/thumbnails/thumb_001.jpg",
      "captured_at": "2025-10-06T10:30:00Z",
      "x_position": 1000,
      "y_position": 500,
      "z_position": 100,
      "exposure_time": 100,
      "gain": 1.5,
      "job_id": null,
      "file_size": 1048576,
      "width": 1920,
      "height": 1080
    }
  ]
}
```

#### `GET /api/images/{image_id}`
Get specific image details.

**Response:**
```json
{
  "id": 1,
  "filename": "/images/image_001.jpg",
  "thumbnail_path": "/thumbnails/thumb_001.jpg",
  "captured_at": "2025-10-06T10:30:00Z",
  "x_position": 1000,
  "y_position": 500,
  "z_position": 100,
  "exposure_time": 100,
  "gain": 1.5,
  "job_id": null,
  "metadata": {},
  "file_size": 1048576,
  "width": 1920,
  "height": 1080
}
```

#### `DELETE /api/images/{image_id}`
Delete an image.

**Response:**
```json
{
  "status": "deleted",
  "message": "Image deleted successfully"
}
```

---

### Jobs

#### `GET /api/jobs`
List all jobs.

**Query Parameters:**
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum records to return (default: 50)
- `status`: Filter by status (optional)
- `job_type`: Filter by type (optional)

**Response:**
```json
{
  "total": 10,
  "jobs": [
    {
      "id": 1,
      "name": "Evening Timelapse",
      "description": "24-hour timelapse",
      "job_type": "timelapse",
      "status": "running",
      "created_at": "2025-10-06T08:00:00Z",
      "started_at": "2025-10-06T08:05:00Z",
      "progress": 120,
      "total_steps": 1440,
      "parameters": {
        "interval": 60,
        "duration": 86400
      }
    }
  ]
}
```

#### `POST /api/jobs`
Create a new job.

**Request (Timelapse):**
```json
{
  "name": "Morning Timelapse",
  "job_type": "timelapse",
  "parameters": {
    "interval": 60,
    "duration": 3600,
    "exposure": 100,
    "gain": 1.5
  }
}
```

**Request (Grid Scan):**
```json
{
  "name": "Sample Grid Scan",
  "job_type": "grid",
  "parameters": {
    "start_x": 0,
    "end_x": 5000,
    "step_x": 500,
    "start_y": 0,
    "end_y": 5000,
    "step_y": 500,
    "z_position": 100,
    "exposure": 100,
    "gain": 1.5
  }
}
```

**Request (Z-Stack):**
```json
{
  "name": "Z-Stack Capture",
  "job_type": "zstack",
  "parameters": {
    "x_position": 1000,
    "y_position": 500,
    "start_z": 0,
    "end_z": 1000,
    "step_z": 50,
    "exposure": 100,
    "gain": 1.5
  }
}
```

**Response:**
```json
{
  "id": 2,
  "name": "Morning Timelapse",
  "job_type": "timelapse",
  "status": "pending",
  "created_at": "2025-10-06T10:30:00Z",
  "parameters": {...}
}
```

#### `GET /api/jobs/{job_id}`
Get job details.

**Response:**
```json
{
  "id": 1,
  "name": "Evening Timelapse",
  "description": "24-hour timelapse",
  "job_type": "timelapse",
  "status": "running",
  "created_at": "2025-10-06T08:00:00Z",
  "started_at": "2025-10-06T08:05:00Z",
  "progress": 120,
  "total_steps": 1440,
  "parameters": {...},
  "images": [
    {"id": 1, "filename": "image_001.jpg"},
    {"id": 2, "filename": "image_002.jpg"}
  ]
}
```

#### `PATCH /api/jobs/{job_id}`
Update job status (pause/resume/cancel).

**Request:**
```json
{
  "status": "paused"
}
```

**Valid statuses:** `running`, `paused`, `cancelled`

#### `DELETE /api/jobs/{job_id}`
Delete a job and its associated images.

---

### Positions

#### `GET /api/positions`
List all saved positions.

**Response:**
```json
{
  "positions": [
    {
      "id": 1,
      "name": "Sample Center",
      "description": "Center of sample",
      "x_position": 1000,
      "y_position": 500,
      "z_position": 100,
      "camera_settings": {"exposure": 100, "gain": 1.5},
      "created_at": "2025-10-06T09:00:00Z"
    }
  ]
}
```

#### `POST /api/positions`
Save current position.

**Request:**
```json
{
  "name": "Sample Edge",
  "description": "Left edge of sample",
  "x_position": 2000,
  "y_position": 1000,
  "z_position": 150,
  "camera_settings": {"exposure": 120, "gain": 1.8}
}
```

#### `POST /api/positions/{position_id}/goto`
Move to saved position.

**Response:**
```json
{
  "status": "moving",
  "target_position": {
    "x": 2000,
    "y": 1000,
    "z": 150
  }
}
```

#### `DELETE /api/positions/{position_id}`
Delete saved position.

---

### WebSocket

#### `WS /ws`
Real-time updates via WebSocket.

**Connection:**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');
```

**Message Types (Server → Client):**

**Position Update:**
```json
{
  "type": "position",
  "data": {
    "x": 1000,
    "y": 500,
    "z": 100,
    "is_moving": true
  }
}
```

**Job Progress:**
```json
{
  "type": "job_progress",
  "data": {
    "job_id": 1,
    "progress": 120,
    "total_steps": 1440,
    "status": "running"
  }
}
```

**Image Captured:**
```json
{
  "type": "image_captured",
  "data": {
    "image_id": 123,
    "filename": "/images/image_123.jpg",
    "thumbnail_path": "/thumbnails/thumb_123.jpg"
  }
}
```

**Status Update:**
```json
{
  "type": "status",
  "data": {
    "camera": "connected",
    "stage": "connected"
  }
}
```

**Error:**
```json
{
  "type": "error",
  "data": {
    "component": "camera",
    "message": "Camera connection lost",
    "severity": "critical"
  }
}
```

---

## Raspberry Pi Motor Controller API

The Raspberry Pi runs a separate Flask service for GPIO control.

### Base URL: `http://raspberrypi.local:5000`

#### `POST /move`
Move motors.

**Request:**
```json
{
  "x": 1000,
  "y": 500,
  "z": 100,
  "relative": false
}
```

**Response:**
```json
{
  "status": "success",
  "position": {
    "x": 1000,
    "y": 500,
    "z": 100
  }
}
```

#### `GET /position`
Get current position.

**Response:**
```json
{
  "x": 1000,
  "y": 500,
  "z": 100
}
```

#### `POST /home`
Home all axes.

**Response:**
```json
{
  "status": "homed",
  "position": {"x": 0, "y": 0, "z": 0}
}
```

#### `GET /sensors`
Read all sensors.

**Response:**
```json
{
  "temperature": 25.5,
  "limit_switches": {
    "x_min": false,
    "x_max": false,
    "y_min": false,
    "y_max": false,
    "z_min": false,
    "z_max": false
  }
}
```

#### `POST /stop`
Emergency stop.

**Response:**
```json
{
  "status": "stopped"
}
```

---

## Configuration

### Environment Variables (.env)

**CRITICAL: Never commit .env to git!**

```bash
# Database
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/microscope_db

# Raspberry Pi
RPI_URL=http://raspberrypi.local:5000
RPI_TIMEOUT=10

# Storage
IMAGES_PATH=./images
THUMBNAILS_PATH=./thumbnails
THUMBNAIL_SIZE=400

# Camera
CAMERA_INDEX=0

# Server
HOST=0.0.0.0
PORT=8000

# Safety Limits (steps)
MAX_X_POSITION=10000
MAX_Y_POSITION=10000
MAX_Z_POSITION=5000
MIN_X_POSITION=0
MIN_Y_POSITION=0
MIN_Z_POSITION=0

# Watchdog
WATCHDOG_TIMEOUT=30

# CORS (for development)
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:8000
```

---

## Key Features Implementation

### 1. Position Validation

**Requirement:** Validate positions before movement to prevent hardware damage.

**Implementation in `backend/core/watchdog.py`:**

```python
from backend.config import get_settings

settings = get_settings()

class PositionValidator:
    """Validates stage positions before movement"""
    
    @staticmethod
    def validate_position(x: float = None, y: float = None, z: float = None) -> tuple[bool, str]:
        """
        Validate position against safety limits.
        
        Returns:
            (is_valid, error_message)
        """
        if x is not None:
            if x < settings.MIN_X_POSITION or x > settings.MAX_X_POSITION:
                return False, f"X position {x} out of range [{settings.MIN_X_POSITION}, {settings.MAX_X_POSITION}]"
        
        if y is not None:
            if y < settings.MIN_Y_POSITION or y > settings.MAX_Y_POSITION:
                return False, f"Y position {y} out of range [{settings.MIN_Y_POSITION}, {settings.MAX_Y_POSITION}]"
        
        if z is not None:
            if z < settings.MIN_Z_POSITION or z > settings.MAX_Z_POSITION:
                return False, f"Z position {z} out of range [{settings.MIN_Z_POSITION}, {settings.MAX_Z_POSITION}]"
        
        return True, ""
    
    @staticmethod
    def validate_relative_move(current_x: float, current_y: float, current_z: float,
                               dx: float = 0, dy: float = 0, dz: float = 0) -> tuple[bool, str]:
        """Validate relative movement"""
        target_x = current_x + dx
        target_y = current_y + dy
        target_z = current_z + dz
        
        return PositionValidator.validate_position(target_x, target_y, target_z)
```

**Usage in API:**

```python
from backend.core.watchdog import PositionValidator

@router.post("/move")
async def move_stage(request: MoveRequest):
    # Validate before moving
    is_valid, error_msg = PositionValidator.validate_position(
        request.x, request.y, request.z
    )
    
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_msg)
    
    # Proceed with movement
    await stage.move(...)
```

---

### 2. Watchdog Timers

**Requirement:** Timeout protection for hardware communication.

**Implementation in `backend/core/watchdog.py`:**

```python
import asyncio
from typing import Callable, Any

class Watchdog:
    """Timeout protection for hardware operations"""
    
    @staticmethod
    async def execute_with_timeout(
        coro: Callable,
        timeout: float,
        operation_name: str
    ) -> Any:
        """
        Execute async operation with timeout.
        
        Args:
            coro: Async function to execute
            timeout: Timeout in seconds
            operation_name: Name for error messages
            
        Returns:
            Result of the operation
            
        Raises:
            TimeoutError: If operation exceeds timeout
        """
        try:
            return await asyncio.wait_for(coro, timeout=timeout)
        except asyncio.TimeoutError:
            raise TimeoutError(
                f"{operation_name} timed out after {timeout} seconds. "
                "Check hardware connection."
            )
```

**Usage:**

```python
from backend.core.watchdog import Watchdog
from backend.config import get_settings

settings = get_settings()

async def move_stage_safe(x, y, z):
    """Move stage with timeout protection"""
    try:
        result = await Watchdog.execute_with_timeout(
            stage.move(x, y, z),
            timeout=settings.WATCHDOG_TIMEOUT,
            operation_name="Stage movement"
        )
        return result
    except TimeoutError as e:
        # Log error, notify user
        await log_error("stage", str(e))
        raise HTTPException(status_code=504, detail=str(e))
```

---

### 3. Swagger API Documentation

**Requirement:** Interactive API documentation.

**Implementation:** FastAPI provides this automatically, but here's how to enhance it:

```python
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

app = FastAPI(
    title="Microscope Control API",
    description="""
    ## Microscope Control System API
    
    Control microscope camera, motorized stage, and automated jobs.
    
    ### Features
    * **Camera Control**: Capture images with custom exposure and gain
    * **Stage Control**: Move X/Y/Z axes with position validation
    * **Job Automation**: Timelapse, grid scans, z-stacks
    * **Real-time Updates**: WebSocket for live position and status
    * **Image Management**: Store, retrieve, and delete images
    
    ### Safety Features
    * Position validation before movement
    * Watchdog timers for hardware operations
    * Emergency stop functionality
    """,
    version="1.0.0",
    contact={
        "name": "Microscope Lab",
        "email": "lab@example.com",
    },
    license_info={
        "name": "MIT",
    },
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Microscope Control API",
        version="1.0.0",
        description=app.description,
        routes=app.routes,
    )
    
    # Add tags metadata
    openapi_schema["tags"] = [
        {
            "name": "Camera Control",
            "description": "Operations for controlling the microscope camera"
        },
        {
            "name": "Stage Control",
            "description": "Operations for controlling the motorized stage"
        },
        {
            "name": "Images",
            "description": "Image management operations"
        },
        {
            "name": "Jobs",
            "description": "Automated job management"
        },
        {
            "name": "Positions",
            "description": "Saved position management"
        },
        {
            "name": "System",
            "description": "System status and health checks"
        }
    ]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
```

**Access Swagger UI:** `http://localhost:8000/docs`

---

## Development Workflow

### 1. Initial Setup

```bash
# Clone repository
git clone <repository-url>
cd microscope-project

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Create .env file (copy from .env.example)
cp .env.example .env
# Edit .env with your settings

# Setup database
createdb microscope_db
alembic upgrade head

# Frontend setup
cd ../frontend
npm install

# Install pre-commit hooks
cd ..
pip install pre-commit
pre-commit install
```

---

### 2. Running Development Servers

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
python main.py
# Or use uvicorn with hot reload:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
# Runs on http://localhost:5173
```

**Terminal 3 - Raspberry Pi (on RPi):**
```bash
cd raspberry_pi
python motor_controller.py
# Runs on http://raspberrypi.local:5000
```

---

### 3. Git Workflow

```bash
# Create feature branch
git checkout -b feature/image-viewer

# Make changes, add files
git add .

# Pre-commit hooks run automatically on commit
git commit -m "Add image viewer component"

# Push to remote
git push origin feature/image-viewer

# Create Pull Request on GitHub
# CI/CD pipeline runs automatically

# After PR approved and merged to develop
git checkout develop
git pull

# When ready for production
git checkout main
git merge develop
git push origin main
# Deployment pipeline runs automatically
```

---

### 4. Testing

**Backend tests:**
```bash
cd backend
pytest
pytest --cov=. --cov-report=html  # With coverage report
pytest tests/test_api_control.py -v  # Specific test file
```

**Frontend tests:**
```bash
cd frontend
npm run test:unit
npm run test:e2e
```

---

### 5. Database Migrations

**Create new migration:**
```bash
cd backend
alembic revision --autogenerate -m "Add user authentication"
```

**Apply migrations:**
```bash
alembic upgrade head
```

**Rollback migration:**
```bash
alembic downgrade -1
```

---

## CI/CD Pipeline

### GitHub Actions Workflow

**Backend CI (`.github/workflows/backend-ci.yml`):**
- Runs on every push/PR to `main` or `develop`
- Lints code with flake8 and black
- Type checks with mypy
- Runs pytest with coverage
- Uploads coverage to Codecov

**Frontend CI (`.github/workflows/frontend-ci.yml`):**
- Runs on every push/PR to `main` or `develop`
- Lints code with ESLint
- Format checks with Prettier
- Type checks with vue-tsc
- Runs unit tests
- Builds production bundle

**Deployment (`.github/workflows/deploy.yml`):**
- Triggered on push to `main` branch
- Builds frontend
- Deploys to Windows PC via SSH/SCP
- Runs database migrations
- Restarts application service
- Performs health check
- Sends notifications

---

## Security Considerations

### 1. Authentication (Future Implementation)

For production, implement JWT-based authentication:

```python
# backend/core/security.py
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = "your-secret-key-here"  # Store in .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

### 2. CORS Configuration

Configure CORS properly for production:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3. Rate Limiting

Implement rate limiting for API endpoints:

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/capture")
@limiter.limit("10/minute")
async def capture_image(request: Request):
    # Limit to 10 captures per minute
    pass
```

---

## Production Deployment

### Windows PC Setup

**1. Install Dependencies:**
- Python 3.11+
- PostgreSQL 16
- Git

**2. Create Windows Service:**

Create `microscope-api.xml` for NSSM:

```xml
<service>
  <id>MicroscopeAPI</id>
  <name>Microscope Control API</name>
  <description>Microscope control system backend</description>
  <executable>C:\Python311\python.exe</executable>
  <arguments>-m uvicorn main:app --host 0.0.0.0 --port 8000</arguments>
  <workingdirectory>C:\microscope-app\backend</workingdirectory>
  <logpath>C:\microscope-app\logs</logpath>
  <log mode="roll-by-size">
    <sizeThreshold>10240</sizeThreshold>
    <keepFiles>8</keepFiles>
  </log>
</service>
```

**Install service:**
```powershell
# Download NSSM (Non-Sucking Service Manager)
# https://nssm.cc/download

nssm install MicroscopeAPI C:\Python311\python.exe "-m uvicorn main:app --host 0.0.0.0 --port 8000"
nssm set MicroscopeAPI AppDirectory C:\microscope-app\backend
nssm start MicroscopeAPI
```

---

### Raspberry Pi Setup

**1. Install Raspberry Pi OS Lite (64-bit)**

**2. Install Python and dependencies:**
```bash
sudo apt update
sudo apt install python3-pip python3-venv git
```

**3. Setup motor controller:**
```bash
cd /home/pi
git clone <repository-url>
cd microscope-project/raspberry_pi
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**4. Create systemd service:**

Create `/etc/systemd/system/motor-controller.service`:

```ini
[Unit]
Description=Microscope Motor Controller
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/microscope-project/raspberry_pi
ExecStart=/home/pi/microscope-project/raspberry_pi/venv/bin/python motor_controller.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable and start:**
```bash
sudo systemctl enable motor-controller
sudo systemctl start motor-controller
sudo systemctl status motor-controller
```

---

## Monitoring & Logging

### Application Logging

**Backend logging (`backend/core/logging.py`):**

```python
import logging
from logging.handlers import RotatingFileHandler
import sys

def setup_logging():
    """Configure application logging"""
    
    # Create logs directory
    import os
    os.makedirs("logs", exist_ok=True)
    
    # Create logger
    logger = logging.getLogger("microscope")
    logger.setLevel(logging.DEBUG)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    
    # File handler (rotating)
    file_handler = RotatingFileHandler(
        "logs/microscope.log",
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

logger = setup_logging()
```

**Usage:**
```python
from backend.core.logging import logger

logger.info("Application started")
logger.warning("Camera temperature high: 45°C")
logger.error("Failed to connect to Raspberry Pi", exc_info=True)
```

---

## Troubleshooting

### Common Issues

**1. Database connection failed**
- Check PostgreSQL is running: `pg_ctl status`
- Verify DATABASE_URL in .env
- Check firewall settings
- Ensure database exists: `psql -l`

**2. Raspberry Pi not responding**
- Check RPi is powered on and on network
- Verify RPI_URL in .env
- Check motor-controller service: `sudo systemctl status motor-controller`
- Check RPi logs: `sudo journalctl -u motor-controller -f`

**3. Camera not detected**
- Check camera is connected
- Verify CAMERA_INDEX in .env
- Test with OpenCV: `python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"`
- Check camera permissions on Windows

**4. Frontend build fails**
- Delete node_modules and reinstall: `rm -rf node_modules && npm install`
- Clear npm cache: `npm cache clean --force`
- Check Node.js version: `node --version` (should be 18+)

**5. WebSocket connection fails**
- Check CORS settings
- Verify WebSocket endpoint: `ws://localhost:8000/ws`
- Check browser console for errors
- Ensure uvicorn is running with WebSocket support

---

## Testing Strategy

### Backend Tests

**Unit Tests:**
- Test individual functions
- Mock external dependencies (database, RPi)
- Fast execution

**Integration Tests:**
- Test API endpoints
- Use test database
- Test database operations

**Example test structure:**

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="function")
def test_db():
    """Create test database for each test"""
    engine = create_engine("sqlite:///./test.db")
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(test_db):
    """FastAPI test client"""
    return TestClient(app)

@pytest.fixture
def mock_camera(monkeypatch):
    """Mock camera for testing"""
    class MockCamera:
        def capture(self):
            return {"status": "success"}
    
    monkeypatch.setattr("backend.services.camera.Camera", MockCamera)
```

---

### Frontend Tests

**Unit Tests (Vitest):**
- Test components in isolation
- Test composables
- Test utilities

**E2E Tests (Playwright):**
- Test user workflows
- Test full application
- Run in real browser

**Example component test:**

```typescript
import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import StageControl from '@/components/StageControl.vue';

describe('StageControl', () => {
  it('emits move event when arrow clicked', async () => {
    const wrapper = mount(StageControl);
    
    await wrapper.find('.arrow-up').trigger('click');
    
    expect(wrapper.emitted('move')).toBeTruthy();
    expect(wrapper.emitted('move')[0][0]).toEqual({
      x: 0,
      y: 100,
      z: 0,
      relative: true
    });
  });
});
```

---

## Performance Optimization

### 1. Database Indexing

All frequently queried columns have indexes (see database schema).

### 2. Image Optimization

- Generate thumbnails on capture (400px max dimension)
- Serve images with appropriate MIME types
- Consider CDN for image serving in production

### 3. WebSocket Optimization

- Throttle position updates (max 10/second)
- Batch multiple updates when possible
- Use binary protocol for large data

### 4. Frontend Optimization

- Lazy load components
- Virtual scrolling for image gallery
- Image lazy loading
- Code splitting by route

---

## Future Enhancements

### Phase 2 Features

1. **User Authentication**
   - Multi-user support
   - Role-based access control
   - API key authentication

2. **Advanced Image Processing**
   - Focus stacking
   - HDR imaging
   - Image stitching for large scans

3. **AI Integration**
   - Auto-focus
   - Object detection
   - Image quality assessment

4. **Cloud Storage**
   - AWS S3 / Azure Blob integration
   - Automatic backup
   - Remote access via cloud

5. **Mobile App**
   - iOS/Android native apps
   - Push notifications
   - Offline job queue

6. **Advanced Job Types**
   - Multi-position timelapse
   - Adaptive scanning (focus on regions of interest)
   - Event-triggered capture

---

## Support & Documentation

### Internal Documentation

- **API Docs:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`
- **OpenAPI JSON:** `http://localhost:8000/openapi.json`

### Code Documentation

- Python: Docstrings following Google style
- TypeScript: JSDoc comments
- README.md in each major directory

### Getting Help

1. Check logs: `logs/microscope.log`
2. Check system health: `GET /api/health`
3. Review error messages in browser console
4. Check GitHub Issues

---

## Appendix

### A. Hardware Requirements

**Windows PC:**
- Windows 10/11
- 8GB RAM minimum (16GB recommended)
- 100GB free disk space (for images)
- USB 3.0 port for camera
- Network connection

**Raspberry Pi 5:**
- 4GB RAM minimum
- MicroSD card (32GB+)
- Power supply (5V 5A)
- GPIO pins for stepper motor drivers
- Network connection (Ethernet or WiFi)

**Stepper Motors:**
- NEMA 17 or similar
- Appropriate drivers (A4988, DRV8825, TMC2208, etc.)
- Limit switches for homing
- Power supply for motors

---

### B. Dependencies

**Backend (`requirements.txt`):**
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
alembic==1.12.1
pydantic==2.5.0
pydantic-settings==2.1.0
python-multipart==0.0.6
Pillow==10.1.0
opencv-python==4.8.1.78
httpx==0.25.1
python-dotenv==1.0.0
aiofiles==23.2.1
websockets==12.0
```

**Backend Dev (`requirements-dev.txt`):**
```
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
pytest-mock==3.12.0
black==23.12.0
flake8==6.1.0
mypy==1.7.1
pre-commit==3.6.0
```

**Raspberry Pi (`raspberry_pi/requirements.txt`):**
```
Flask==3.0.0
RPi.GPIO==0.7.1
```

**Frontend (`package.json` dependencies):**
```json
{
  "dependencies": {
    "vue": "^3.3.11",
    "vue-router": "^4.2.5",
    "pinia": "^2.1.7",
    "@vueuse/core": "^10.7.0",
    "axios": "^1.6.2"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^4.5.2",
    "@vue/test-utils": "^2.4.3",
    "typescript": "^5.3.3",
    "vite": "^5.0.8",
    "vitest": "^1.1.0",
    "vue-tsc": "^1.8.27",
    "eslint": "^8.56.0",
    "eslint-plugin-vue": "^9.19.2",
    "prettier": "^3.1.1"
  }
}
```

---

### C. API Rate Limits (Recommended for Production)

- `/api/capture`: 10 requests/minute
- `/api/move`: 60 requests/minute
- `/api/images`: 120 requests/minute
- `/api/jobs`: 30 requests/minute
- WebSocket messages: 100/second

---

### D. Storage Estimates

**Image Storage:**
- Typical microscope image: 2-5 MB (uncompressed)
- Thumbnail: 50-100 KB
- 1000 images ≈ 2-5 GB
- Plan for 100GB minimum for production use

**Database Storage:**
- Metadata is small: ~1KB per image
- 10,000 images ≈ 10 MB database size
- Logs can grow: plan for 100MB-1GB

---

### E. Network Requirements

**LAN Setup (Recommended):**
- Windows PC: Static IP (e.g., 192.168.1.100)
- Raspberry Pi: Static IP (e.g., 192.168.1.101)
- Client devices: Same network

**Remote Access Options:**
1. **VPN:** Set up VPN server on network
2. **Tailscale:** Easy mesh network
3. **ngrok:** Quick tunnel for testing
4. **Cloudflare Tunnel:** Production-ready tunnel

---

## Quick Start Checklist

- [ ] Install PostgreSQL and create database
- [ ] Clone repository
- [ ] Set up Python virtual environment
- [ ] Install backend dependencies
- [ ] Create and configure .env file
- [ ] Run database migrations
- [ ] Install Node.js and frontend dependencies
- [ ] Start backend development server
- [ ] Start frontend development server
- [ ] Set up Raspberry Pi with motor controller
- [ ] Test camera connection
- [ ] Test stage movement
- [ ] Capture first image
- [ ] Create first job
- [ ] Set up Git hooks
- [ ] Configure CI/CD pipeline
- [ ] Deploy to production

---

## Contact & Contributing

**Project Repository:** [Add GitHub URL]

**Bug Reports:** Create issue on GitHub

**Feature Requests:** Create issue with "enhancement" label

**Pull Requests:** Always welcome! Please follow:
1. Fork repository
2. Create feature branch
3. Write tests
4. Ensure CI passes
5. Submit PR with clear description

---

## License

[Specify your license - MIT, Apache 2.0, etc.]

---

## Acknowledgments

- FastAPI team for excellent web framework
- Vue.js team for great frontend framework
- PostgreSQL community
- Raspberry Pi Foundation

---

**Document Version:** 1.0.0  
**Last Updated:** 2025-10-06  
**Author:** [Your Name]

---

## Implementation Priority Order

For Claude Code to implement, follow this order:

### Phase 1: Core Infrastructure (Week 1)
1. Set up project structure
2. Configure PostgreSQL and create database
3. Implement database models and migrations
4. Create basic FastAPI application with health check
5. Set up configuration management

### Phase 2: Backend API (Week 2)
6. Implement image endpoints (CRUD)
7. Implement control endpoints (camera, stage)
8. Implement job endpoints (create, list, update)
9. Implement position endpoints
10. Add Pydantic schemas and validation
11. Add position validation and watchdog
12. Set up logging

### Phase 3: Hardware Integration (Week 3)
13. Implement camera service (OpenCV)
14. Implement stage service (HTTP client to RPi)
15. Implement Raspberry Pi motor controller
16. Test hardware communication
17. Implement WebSocket for real-time updates

### Phase 4: Job Queue (Week 4)
18. Implement job queue system
19. Implement timelapse job type
20. Implement grid scan job type
21. Implement z-stack job type
22. Test job execution

### Phase 5: Frontend (Week 5-6)
23. Set up Vue 3 project with TypeScript
24. Create main layout and navigation
25. Implement image viewer component
26. Implement image gallery component
27. Implement stage control component
28. Implement camera settings component
29. Implement job manager component
30. Implement position management
31. Connect to backend API
32. Implement WebSocket connection
33. Add state management (Pinia)

### Phase 6: Testing & CI/CD (Week 7)
34. Write backend unit tests
35. Write backend integration tests
36. Write frontend component tests
37. Set up GitHub Actions workflows
38. Configure pre-commit hooks
39. Test full deployment pipeline

### Phase 7: Production Deployment (Week 8)
40. Set up Windows service
41. Set up Raspberry Pi systemd service
42. Configure production environment
43. Deploy to production
44. Monitor and fix issues
45. Document deployment process

---

**This document provides complete specifications for building the microscope control system. Use it as the single source of truth for all implementation decisions.**
