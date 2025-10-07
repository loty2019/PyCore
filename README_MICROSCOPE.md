# Microscope Control System - Proof of Concept

A web-based microscope control system for remote control of camera, motorized stage, and automated job execution.

## 📋 Features

- **Camera Control**: Capture images using PixelLink SDK with custom exposure and gain settings
- **Stage Control**: Control motorized X/Y/Z stage with position validation and safety limits
- **Automated Jobs**: Execute timelapse, grid scans, and z-stack captures
- **Real-time Updates**: WebSocket for live position and status monitoring
- **Image Management**: Store, retrieve, and manage captured images
- **Safety Features**: Position validation, watchdog timers, emergency stop

## 🏗️ Architecture

```
Backend (FastAPI + Python)
├── Camera control (PixelLink SDK)
├── Stage control (Mock for PoC)
├── PostgreSQL database
├── Job queue system
└── WebSocket for real-time updates

Frontend (HTML/JS)
└── Simple web interface for testing
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 16
- PixelLink SDK (optional - will use mock if not available)

### Installation

1. **Clone or navigate to the project**
```bash
cd C:\Users\loren\Desktop\Link\PyCore
```

2. **Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up database**

Create a PostgreSQL database:
```sql
CREATE DATABASE microscope_db;
```

5. **Configure environment**

Copy `.env.example` to `.env` and update settings:
```bash
copy .env.example .env
```

Edit `.env` with your database credentials:
```
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/microscope_db
```

6. **Run the application**
```bash
python backend/main.py
```

Or use the convenience script:
```bash
start.bat
```

The server will start on `http://localhost:8000`

### Access the Application

- **Web Interface**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/control/health

## 📁 Project Structure

```
PyCore/
├── backend/
│   ├── main.py                    # FastAPI application entry point
│   ├── config.py                  # Configuration management
│   ├── database/                  # Database models and session
│   │   ├── base.py
│   │   ├── session.py
│   │   └── models.py
│   ├── schemas/                   # Pydantic validation schemas
│   │   ├── image.py
│   │   ├── job.py
│   │   ├── control.py
│   │   └── position.py
│   ├── api/                       # API routes
│   │   └── routes/
│   │       ├── control.py         # Camera & stage control
│   │       ├── images.py          # Image management
│   │       ├── jobs.py            # Job management
│   │       ├── positions.py       # Position management
│   │       └── websocket.py       # WebSocket endpoint
│   ├── services/                  # Business logic
│   │   ├── camera.py              # PixelLink camera service
│   │   ├── stage.py               # Stage control (mock)
│   │   ├── image_service.py       # Image processing
│   │   ├── job_queue.py           # Job execution
│   │   └── websocket_manager.py   # WebSocket manager
│   └── core/                      # Core utilities
│       ├── logging.py             # Logging configuration
│       └── watchdog.py            # Safety & validation
├── frontend/
│   └── index.html                 # Simple web interface
├── HELP/
│   └── pixelinkPythonWrapper-master/  # PixelLink SDK
├── images/                        # Captured images (auto-created)
├── thumbnails/                    # Image thumbnails (auto-created)
├── logs/                          # Application logs (auto-created)
├── .env                           # Environment variables (create from .env.example)
├── .env.example                   # Example environment configuration
├── .gitignore                     # Git ignore rules
├── requirements.txt               # Python dependencies
├── start.bat                      # Windows startup script
├── SETUP_GUIDE.md                 # Detailed setup instructions
├── MICROSCOPE_PROJECT_SPECIFICATION.md  # Complete specification
└── README_MICROSCOPE.md           # This file
```

## 🎮 Usage

### Camera Control

```python
# Capture an image via API
POST /api/control/capture
{
    "exposure": 100,
    "gain": 1.5
}
```

### Stage Control

```python
# Move stage
POST /api/control/move
{
    "x": 1000,
    "y": 500,
    "z": 100,
    "relative": false
}

# Home all axes
POST /api/control/home

# Emergency stop
POST /api/control/stop
```

### Create Automated Jobs

```python
# Timelapse
POST /api/jobs
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

# Grid Scan
POST /api/jobs
{
    "name": "Sample Grid",
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

# Z-Stack
POST /api/jobs
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

## 🔧 Configuration

Edit `.env` to configure:

- **Database**: PostgreSQL connection string
- **Camera**: Camera index (default: 0)
- **Storage**: Image and thumbnail directories
- **Safety Limits**: Min/Max positions for X/Y/Z axes
- **Server**: Host and port settings
- **CORS**: Allowed origins for web interface

## 📊 Database Schema

### Tables
- **images**: Captured image metadata
- **jobs**: Automated job tracking
- **positions**: Saved positions
- **system_logs**: System event logging
- **settings**: Persistent application settings

## 🔒 Safety Features

- **Position Validation**: Validates all movements before execution
- **Safety Limits**: Configurable min/max positions for each axis
- **Watchdog Timers**: Timeout protection for hardware operations
- **Emergency Stop**: Immediate halt of all movements

## 🐛 Troubleshooting

### Camera not detected
- Verify PixelLink SDK is installed
- Check camera is connected and powered
- Application will use mock camera if SDK not available

### Database connection failed
- Verify PostgreSQL is running
- Check DATABASE_URL in .env
- Ensure database exists

### Stage not responding
- This PoC uses mock stage controller
- For real hardware, implement Raspberry Pi controller
- Check network connectivity to RPi

## 📝 Development

### Running in development mode

```bash
# Install dependencies
pip install -r requirements.txt

# Run with auto-reload
python backend/main.py
```

### API Documentation

Interactive API documentation available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🚧 Production Deployment

For production deployment:

1. Set `DEBUG=False` in `.env`
2. Use proper PostgreSQL server
3. Implement Raspberry Pi motor controller
4. Set up HTTPS with reverse proxy (nginx)
5. Configure firewall rules
6. Set up monitoring and logging

## 📖 Documentation

- **SETUP_GUIDE.md**: Detailed setup instructions
- **MICROSCOPE_PROJECT_SPECIFICATION.md**: Complete technical specification
- **API Documentation**: http://localhost:8000/docs

## 🤝 Contributing

This is a proof of concept. For production use, consider:

- Adding authentication and authorization
- Implementing comprehensive error handling
- Adding unit and integration tests
- Improving frontend with Vue.js/React
- Adding image analysis features
- Implementing backup and recovery

## 📄 License

MIT

## 🙏 Acknowledgments

- FastAPI framework
- PixelLink SDK
- PostgreSQL database
- SQLAlchemy ORM

---

**Note**: This is a separate project from the PyCore PixelLink camera utilities. For camera-specific documentation, see the main README.md file.
