# 📚 Pixelink Camera Python Guide - START HERE

Welcome! This guide will help you learn to use your Pixelink camera with Python.

## 📁 What's in This Project

| File                   | Description                   | When to Use                   |
| ---------------------- | ----------------------------- | ----------------------------- |
| **README.md**          | Complete tutorial & reference | Learning how everything works |
| **QUICK_REFERENCE.md** | Code snippets cheat sheet     | Quick lookup while coding     |
| **EXAMPLES.md**        | 8 ready-to-use scripts        | Copy-paste solutions          |
| **capture_image.py**   | Working capture script        | Run it now to test camera     |

## 🚀 Getting Started (5 Minutes)

### Step 1: Test Your Setup

Run the working script to verify everything works:

```powershell
python capture_image.py
```

**Expected Result:** Two images saved in `captured_images` folder (JPEG and BMP)

### Step 2: Understand What Happened

Open `capture_image.py` and read through it. The main steps are:

1. **Initialize** camera → Get a handle
2. **Calculate** buffer size → Based on image dimensions
3. **Create** buffer → To hold raw image data
4. **Start** streaming → Camera begins capturing
5. **Get** frame → Capture one image
6. **Stop** streaming → Done capturing
7. **Format** image → Convert to JPEG/BMP
8. **Save** to file → Write to disk
9. **Cleanup** → Uninitialize camera

### Step 3: Try the Examples

Pick any example from `EXAMPLES.md` and try it:

- **Example 1**: Simplest possible capture (10 lines)
- **Example 4**: Time-lapse photography (cool!)
- **Example 6**: See live frame rate

## 📖 Learning Path

Follow this path to master the Pixelink camera API:

### Week 1: Basics

- [x] Run `capture_image.py` ← You are here!
- [ ] Read the "Understanding the Code" section in README.md
- [ ] Try Example 1 (simple_capture)
- [ ] Try Example 2 (list_cameras)
- [ ] Understand return codes and error handling

### Week 2: Settings

- [ ] Learn exposure control (Example 3)
- [ ] Try auto vs manual exposure (Example 5)
- [ ] Experiment with gain settings
- [ ] Save your favorite settings (Example 7)

### Week 3: Advanced

- [ ] Create a time-lapse (Example 4)
- [ ] Test different image formats (Example 8)
- [ ] Implement continuous capture
- [ ] Try ROI (Region of Interest)

### Week 4: Professional

- [ ] Add triggering (software/hardware)
- [ ] Implement white balance
- [ ] Create a preview window
- [ ] Build your own application!

## 🎯 Common Tasks - Quick Links

### "I want to..."

**...capture a single image**
→ Use `capture_image.py` or Example 1 in EXAMPLES.md

**...adjust brightness**
→ See "Exposure" section in QUICK_REFERENCE.md

**...capture multiple images**
→ See Example 4 (time-lapse) or Example 6 (continuous)

**...see all camera info**
→ Run Example 2 (list_cameras)

**...change image format**
→ See "Image Formats" section in README.md

**...save my settings**
→ Use Example 7 (save_load_settings)

**...understand an error**
→ See "Troubleshooting" in README.md

**...find a code snippet**
→ Use QUICK_REFERENCE.md (it's a cheat sheet!)

## 📚 Document Guide

### README.md - The Complete Guide

**Size:** ~400 lines  
**Reading Time:** 20 minutes  
**Best For:** Understanding concepts in depth

**Key Sections:**

- Quick Start (get running fast)
- Understanding the Code (how it works)
- Image Formats (JPEG, BMP, TIFF, etc.)
- Advanced Features (exposure, gain, ROI, triggering)
- API Reference (all the important functions)
- Troubleshooting (fix common problems)
- Sample Code Snippets (copy and modify)

**When to Read:**

- You want to really understand what's happening
- You're stuck and need detailed help
- You want to learn advanced features

---

### QUICK_REFERENCE.md - The Cheat Sheet

**Size:** ~250 lines  
**Reading Time:** 5 minutes  
**Best For:** Quick lookup while coding

**What's Inside:**

- Common operations (copy-paste ready)
- All camera settings with examples
- Error handling templates
- Pro tips and performance tricks

**When to Use:**

- "How do I set exposure again?"
- "What was the ROI parameter order?"
- "Quick, I need to save settings!"
- Keep it open while coding!

---

### EXAMPLES.md - Ready-to-Use Scripts

**Size:** ~350 lines (8 complete scripts)  
**Reading Time:** 10 minutes  
**Best For:** Getting stuff done quickly

**Contains:**

1. Simple capture (10 lines!)
2. List all cameras
3. Adjust exposure/gain
4. Time-lapse photography
5. Auto vs manual exposure
6. Live preview (console)
7. Save/load settings
8. All image formats

**When to Use:**

- "I need to do X, is there an example?"
- You want to get something working NOW
- You learn better by example

---

### capture_image.py - Working Script

**Size:** ~180 lines  
**What it Does:** Captures JPEG and BMP images

**When to Use:**

- First thing to run!
- Template for your own scripts
- Verify camera is working

## 🔍 Finding What You Need

### Search Tips

**Looking for code?**
→ Try QUICK_REFERENCE.md or EXAMPLES.md first

**Looking for explanation?**
→ Try README.md

**Looking for specific feature?**
→ Use Ctrl+F to search in README.md

**Looking for troubleshooting?**
→ README.md has a whole section on it

### Common Searches

| I want to find...   | Look in...         | Section                        |
| ------------------- | ------------------ | ------------------------------ |
| How to set exposure | QUICK_REFERENCE.md | Camera Settings > Exposure     |
| Complete example    | EXAMPLES.md        | Pick any example               |
| Error explanation   | README.md          | Troubleshooting                |
| Image formats       | README.md          | Image Formats                  |
| ROI settings        | QUICK_REFERENCE.md | Camera Settings > ROI          |
| Return codes        | QUICK_REFERENCE.md | Error Handling                 |
| Triggering          | README.md          | Advanced Features > Triggering |
| Save settings       | EXAMPLES.md        | Example 7                      |

## 💡 Tips for Success

### 1. Start Small

Don't try to learn everything at once. Run Example 1, understand it, then move on.

### 2. Experiment Safely

The camera won't break from code! Try different settings and see what happens.

### 3. Read Error Messages

They're actually helpful! If you get an error:

1. Read the error message
2. Check Troubleshooting in README.md
3. Make sure camera is connected and not in use

### 4. Use the Samples

The SDK includes official samples in:
`pixelinkPythonWrapper-master\samples\Windows\`

### 5. Keep Documentation Open

While coding, keep these tabs open:

- QUICK_REFERENCE.md (for syntax)
- Your Python file (what you're writing)
- Example in EXAMPLES.md (for reference)

### 6. Save Your Work

When you get something working, save the settings:

```python
PxLApi.saveSettings(hCamera, "my_config.pfs")
```

## 🎓 Understanding Core Concepts

### The Camera Handle

```python
ret = PxLApi.initialize(0)
hCamera = ret[1]  # This is your "connection" to the camera
```

Everything you do uses this handle. Don't lose it!

### Return Values

Every function returns a tuple:

```python
ret = PxLApi.someFunction(hCamera)
# ret[0] = return code (success or error)
# ret[1] = data (if successful)
```

Always check: `if PxLApi.apiSuccess(ret[0]):`

### The Buffer

Raw images need somewhere to live:

```python
from ctypes import create_string_buffer
rawImage = create_string_buffer(buffer_size)
```

This is like a container for the image data.

### Streaming

Camera must be streaming to capture:

```python
PxLApi.setStreamState(hCamera, PxLApi.StreamState.START)
# ... capture images ...
PxLApi.setStreamState(hCamera, PxLApi.StreamState.STOP)
```

### Features

Everything adjustable is a "feature":

- Exposure → `PxLApi.FeatureId.EXPOSURE`
- Gain → `PxLApi.FeatureId.GAIN`
- ROI → `PxLApi.FeatureId.ROI`

Get them: `PxLApi.getFeature(hCamera, feature_id)`  
Set them: `PxLApi.setFeature(hCamera, feature_id, flags, params)`

## 🛠️ Development Workflow

### Typical Session

1. **Test camera works**

   ```powershell
   python capture_image.py
   ```

2. **Find example close to what you need**

   - Look in EXAMPLES.md
   - Copy the code

3. **Modify for your needs**

   - Change file names
   - Adjust settings
   - Add your logic

4. **Test incrementally**

   - Run after each small change
   - Check for errors
   - Verify output

5. **Save good settings**
   - When you get good image quality
   - `PxLApi.saveSettings(...)`

## 📞 When You Need Help

### Self-Help Checklist

- [ ] Did you check Troubleshooting in README.md?
- [ ] Did you read the error message carefully?
- [ ] Is the camera connected and working?
- [ ] Did you try the exact example from EXAMPLES.md?
- [ ] Did you search this document for keywords?

### Getting Support

**Pixelink Technical Support:**

- https://support.pixelink.com/support/tickets/new
- Include: Error message, camera model, what you tried

**Documentation:**

- Official SDK docs: `C:\Program Files\Pixelink\Documentation\`
- GitHub: https://github.com/pixelink-support/pixelinkPythonWrapper

## 🎯 Your First Project Ideas

Start with these beginner-friendly projects:

### Project 1: Photo Booth

- Capture image on keypress
- Save with timestamp
- Show preview message

### Project 2: Security Monitor

- Capture image every minute
- Save if motion detected (compare frames)
- Delete old images

### Project 3: Product Photography

- Set optimal exposure for your product
- Capture from multiple angles (manual)
- Save in consistent format

### Project 4: Time-Lapse

- Capture every X seconds
- Combine into video later
- Document a process

### Project 5: Quality Control

- Capture product images
- Save to organized folders
- Log metadata (timestamp, settings)

## ✅ Quick Self-Test

After spending time with these docs, you should be able to:

- [ ] Run capture_image.py successfully
- [ ] Find the syntax for setting exposure
- [ ] Locate an example for time-lapse
- [ ] Fix "camera not found" error
- [ ] Save camera settings to file
- [ ] Understand what a camera handle is
- [ ] Know where to look for ROI settings
- [ ] Create a buffer for image capture

If you can check all boxes, you're ready to build your own applications!

## 🚀 Next Steps

**Right Now:**

1. Run `capture_image.py`
2. Look at the captured images
3. Try Example 1 from EXAMPLES.md

**This Week:**

1. Read "Understanding the Code" in README.md
2. Try changing exposure in Example 3
3. Create your first custom script

**This Month:**

1. Complete a small project
2. Learn advanced features
3. Save your settings

## 📝 Quick Reference Card

**Print this out and keep it near your computer:**

```
PIXELINK CAMERA - ESSENTIAL COMMANDS

Initialize:    ret = PxLApi.initialize(0); hCamera = ret[1]
Uninitialize:  PxLApi.uninitialize(hCamera)

Start Stream:  PxLApi.setStreamState(hCamera, PxLApi.StreamState.START)
Stop Stream:   PxLApi.setStreamState(hCamera, PxLApi.StreamState.STOP)

Get Frame:     ret = PxLApi.getNextFrame(hCamera, rawImage)
Check Success: if PxLApi.apiSuccess(ret[0]):

Get Exposure:  ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.EXPOSURE)
Set Exposure:  PxLApi.setFeature(hCamera, PxLApi.FeatureId.EXPOSURE,
                                  PxLApi.FeatureFlags.MANUAL, [50.0])

Format Image:  ret = PxLApi.formatImage(rawImage, frameDesc,
                                        PxLApi.ImageFormat.JPEG)

Save Settings: PxLApi.saveSettings(hCamera, "config.pfs")
Load Settings: PxLApi.loadSettings(hCamera, "config.pfs")
```

---

**You've got this! Start with `capture_image.py` and build from there. Happy coding! 🎉**

---

_Last Updated: October 4, 2025_  
_Camera: Pixelink B701 (SN: 771001279)_  
_Your Camera is Ready - Start Capturing!_ 📸
