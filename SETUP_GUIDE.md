# Setup Guide - Microscope Control System

Complete step-by-step guide for setting up the Microscope Control System.

## Prerequisites

### Required Software
- Python 3.11 or higher
- PostgreSQL 16
- Git (for version control)

### Optional
- PixelLink SDK (if using PixelLink camera)
- Raspberry Pi 5 (for motor control)

## Step 1: Install PostgreSQL

### Windows

1. Download PostgreSQL from https://www.postgresql.org/download/windows/
2. Run the installer
3. Remember the password you set for the `postgres` user
4. Keep the default port (5432)

### Verify Installation
```bash
psql --version
```

## Step 2: Create Database

Open PostgreSQL command line (psql) or pgAdmin:

```sql
-- Create database
CREATE DATABASE microscope_db;

-- Verify
\l  -- List databases
```

## Step 3: Install Python Dependencies

Navigate to project directory:
```bash
cd C:\Users\loren\Desktop\Link\PyCore
```

Create virtual environment:
```bash
python -m venv venv
```

Activate virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

## Step 4: Configure Environment

Copy environment template:
```bash
copy .env.example .env
```

Edit `.env` file with your settings:

```env
# Database - UPDATE WITH YOUR PASSWORD
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD_HERE@localhost:5432/microscope_db

# Raspberry Pi (if using real hardware)
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

# Safety Limits (adjust based on your hardware)
MAX_X_POSITION=10000
MAX_Y_POSITION=10000
MAX_Z_POSITION=5000
MIN_X_POSITION=0
MIN_Y_POSITION=0
MIN_Z_POSITION=0

# Watchdog
WATCHDOG_TIMEOUT=30

# CORS
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:8000

# Application
DEBUG=True
```

## Step 5: Verify Installation

Test Python imports:
```python
python -c "import fastapi, sqlalchemy, psycopg2; print('All dependencies installed!')"
```

## Step 6: Run the Application

Start the server:
```bash
python backend/main.py
```

You should see output like:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

## Step 7: Access the Application

Open your web browser and navigate to:

- **Web Interface**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/control/health

## Step 8: Test Basic Functionality

### Test Camera (Mock Mode)

In the web interface:
1. Click "Capture Image" button
2. Check Console log for success message
3. Image should appear in Recent Images section

Or via API:
```bash
curl -X POST http://localhost:8000/api/control/capture \
  -H "Content-Type: application/json" \
  -d '{"exposure": 100, "gain": 1.0}'
```

### Test Stage Movement

In the web interface:
1. Use arrow buttons to move stage
2. Watch position display update
3. Try "Home" button to return to origin

Or via API:
```bash
curl -X POST http://localhost:8000/api/control/move \
  -H "Content-Type: application/json" \
  -d '{"x": 100, "y": 100, "z": 0, "relative": true}'
```

### Test Job Creation

In the web interface:
1. Click "Timelapse" button
2. Check Console for job creation message
3. Job will execute automatically

## Troubleshooting

### Issue: "psycopg2 installation failed"

**Solution:**
```bash
pip install psycopg2-binary
```

### Issue: "Unable to connect to database"

**Solution:**
1. Verify PostgreSQL is running:
   ```bash
   # Windows
   sc query postgresql-x64-16

   # Start if not running
   net start postgresql-x64-16
   ```

2. Check connection string in `.env`
3. Verify database exists:
   ```bash
   psql -U postgres -l
   ```

### Issue: "PixelLink SDK not found"

**Solution:**
- This is normal if you don't have a PixelLink camera
- Application will run in mock mode
- To use real camera:
  1. Install PixelLink SDK from manufacturer
  2. Verify SDK is in `HELP/pixelinkPythonWrapper-master/`

### Issue: "Port 8000 already in use"

**Solution:**
Change port in `.env`:
```env
PORT=8001
```

Or stop the process using port 8000:
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Issue: "CORS error in browser"

**Solution:**
Add your frontend URL to ALLOWED_ORIGINS in `.env`:
```env
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:8000,http://localhost:3000
```

## Optional: PixelLink Camera Setup

If you have a PixelLink camera:

1. Install PixelLink SDK from manufacturer
2. Verify camera connection:
   ```python
   python HELP/pixelinkPythonWrapper-master/samples/Windows/getSnapshot.py
   ```
3. Restart application - it should detect camera automatically

## Optional: Raspberry Pi Setup

For motor control with Raspberry Pi:

### On Raspberry Pi

1. Install Raspberry Pi OS
2. Install Python and dependencies:
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv
   ```

3. Create motor controller service (future implementation)

### Update Configuration

Update `.env` with Raspberry Pi IP:
```env
RPI_URL=http://192.168.1.100:5000
```

## Next Steps

1. **Explore API Documentation**: http://localhost:8000/docs
2. **Read full specification**: `MICROSCOPE_PROJECT_SPECIFICATION.md`
3. **Test automated jobs**: Try timelapse, grid scan, z-stack
4. **Customize configuration**: Adjust safety limits and settings
5. **Monitor logs**: Check `logs/microscope.log` for detailed information

## Development Workflow

For development:

```bash
# Install development dependencies (if needed)
pip install pytest black flake8

# Run with auto-reload
python backend/main.py

# Format code
black backend/

# Lint code
flake8 backend/

# Run tests (when implemented)
pytest
```

## Production Deployment

For production use:

1. Set `DEBUG=False` in `.env`
2. Use production-grade PostgreSQL server
3. Set up proper authentication
4. Configure HTTPS with nginx/Apache
5. Use systemd/supervisor for process management
6. Set up monitoring and alerting
7. Configure backup strategy

## Getting Help

- Check logs in `logs/microscope.log`
- Review API documentation at `/docs`
- Check health endpoint: `/api/control/health`
- Refer to `README.md` for common issues

## Success Checklist

- [ ] PostgreSQL installed and running
- [ ] Database created
- [ ] Python dependencies installed
- [ ] `.env` file configured
- [ ] Application starts without errors
- [ ] Web interface accessible
- [ ] Camera capture works (mock or real)
- [ ] Stage movement works (mock)
- [ ] Jobs can be created and executed
- [ ] WebSocket connection established

If all items are checked, your setup is complete! 🎉
