# Quick Start Guide

## 🚀 First Time Setup

### 1. Run Setup Script

Open PowerShell or Command Prompt in the project directory and run:

```bash
setup.bat
```

This will:
- ✅ Check Python installation
- ✅ Create virtual environment
- ✅ Install all Python dependencies
- ✅ Verify installation

### 2. Configure Database

**Option A: Use SQLite (Easiest for testing)**

Edit `.env` and change the database URL to SQLite:
```env
DATABASE_URL=sqlite:///./microscope.db
```

**Option B: Use PostgreSQL (Production)**

1. Install PostgreSQL 16
2. Create database:
   ```sql
   CREATE DATABASE microscope_db;
   ```
3. Update `.env`:
   ```env
   DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/microscope_db
   ```

### 3. Create .env file

```bash
copy .env.example .env
```

Edit `.env` with your settings (especially database URL).

### 4. Start the Backend

```bash
start.bat
```

Or manually:
```bash
venv\Scripts\activate
python backend\main.py
```

The server will start at: **http://localhost:8000**

### 5. Access the Application

- **Old Frontend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/control/health

### 6. Start Vue Frontend (Optional)

```bash
cd frontend-vue
npm install
npm run dev
```

Access at: **http://localhost:5173**

## 🔧 Troubleshooting

### "ModuleNotFoundError: No module named 'fastapi'"

**Solution:**
```bash
# Run setup script
setup.bat

# OR manually:
venv\Scripts\activate
pip install -r requirements.txt
```

### "python: command not found"

**Solution:**
- Install Python 3.11+ from https://www.python.org/
- Make sure "Add Python to PATH" is checked during installation
- Restart your terminal

### Virtual environment activation fails

**Solution:**
```bash
# Windows PowerShell (if execution policy blocks)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try again
venv\Scripts\activate
```

### Database connection error

**Solution:**

For quick testing, use SQLite in `.env`:
```env
DATABASE_URL=sqlite:///./microscope.db
```

For PostgreSQL:
1. Make sure PostgreSQL is running
2. Verify database exists
3. Check connection string in `.env`

### Port 8000 already in use

**Solution:**
```bash
# Find and kill process using port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or change port in .env
PORT=8001
```

## ✅ Verify Installation

After setup, verify everything works:

1. **Check backend health:**
   ```bash
   curl http://localhost:8000/api/control/health
   ```

2. **Open API docs:**
   - Go to http://localhost:8000/docs
   - You should see interactive API documentation

3. **Test camera (mock):**
   - POST to `/api/control/capture`
   - Should return success with mock image

## 📋 Next Steps

1. ✅ Backend is running
2. ✅ Database is connected
3. ✅ API is accessible

Now you can:
- Use the web interface
- Create jobs (timelapse, grid, z-stack)
- Capture images
- Control the stage

For Vue frontend:
```bash
cd frontend-vue
npm install
npm run dev
```

## 🆘 Still Having Issues?

1. Check `logs/microscope.log` for errors
2. Verify all dependencies are installed:
   ```bash
   pip list
   ```
3. Make sure Python version is 3.11+:
   ```bash
   python --version
   ```

## 📚 Documentation

- **Full Setup Guide**: `SETUP_GUIDE.md`
- **Frontend Setup**: `FRONTEND_SETUP.md`
- **API Specification**: `MICROSCOPE_PROJECT_SPECIFICATION.md`
- **Main README**: `README_MICROSCOPE.md`
