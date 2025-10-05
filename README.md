# PyCore Dev Guide

A comprehensive guide and working examples for capturing images from Pixelink cameras using Python and the Pixelink SDK.

## 📋 Table of Contents

- [Overview](#-overview)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Quick Reference Cheat Sheet](#-quick-reference-cheat-sheet)
- [Understanding the Code](#-understanding-the-code)
- [Image Formats](#️-image-formats)
- [Camera Settings](#️-camera-settings)
- [Advanced Features](#-advanced-features-1)
- [API Reference](#-api-reference)
- [Troubleshooting](#-troubleshooting)
- [Sample Code Snippets](#-sample-code-snippets)
- [Performance Tips](#-performance-tips-1)

---

## 🎯 Overview

This project provides Python scripts to capture images from Pixelink cameras. The code is based on the **Pixelink Python wrapper** (`pixelinkWrapper`), which is a thin wrapper around the native Pixelink 4.0 API.

**Supported Cameras:**

- All Pixelink cameras compatible with the Pixelink 4.0 API
- FireWire, USB, USB3, GigE, and 10 GigE cameras
- Includes support for auto-focus, gain HDR, and polar cameras

**Your Current Camera:**

- Model: **Pixelink B701**
- Serial Number: **771001279**

---

## 📦 Prerequisites

### Required Software

1. **Pixelink SDK for Windows**

   - Download from: https://www.navitar.com/products/pixelink-cameras
   - Install either Pixelink Capture or Pixelink SDK
   - SDK installs to: `C:\Program Files\Pixelink\`

2. **Python 3.x** (64-bit recommended)

   - Python 3.8 or higher
   - Your system: Python 3.11

3. **pixelinkWrapper** - Python API wrapper
   - Installed via pip (see installation section)

### Hardware Requirements

- Pixelink camera connected via USB/Ethernet
- Camera should be visible in Windows Device Manager
- No other application using the camera

---

## 🔧 Installation

### Step 1: Install Pixelink SDK

1. Download Pixelink SDK from the official website
2. Run the installer and follow the prompts
3. Restart your computer after installation

### Step 2: Install Python Wrapper

Open PowerShell and run:

```powershell
pip install pixelinkWrapper
```

To upgrade to the latest version:

```powershell
pip install pixelinkWrapper --upgrade
```

### Step 3: Verify Installation

```powershell
python -c "from pixelinkWrapper import PxLApi; print('Success!')"
```

If you see "Success!", you're ready to go!

---

## 🚀 Quick Start

### Capture Your First Image

1. **Connect your camera** to your computer
2. **Navigate to the project folder**:

   ```powershell
   cd C:\Users\loren\Desktop\Link\PyCore
   ```

3. **Run the capture script**:

   ```powershell
   python capture_image.py
   ```

4. **Check the output** in the `captured_images` folder:
   - JPEG image (~80 KB) - compressed
   - BMP image (~1.3 MB) - uncompressed

### Expected Output

```
============================================================
Pixelink Camera Image Capture
============================================================

Searching for Pixelink cameras...
Found 1 camera(s)

Initializing Pixelink camera...
Camera initialized successfully. Handle: 1
Camera Model: B701
Serial Number: 771001279

Capturing JPEG image...
✓ Saved JPEG: captured_images\pixelink_capture_20251004_173616.jpg (80,453 bytes)

Capturing BMP image...
✓ Saved BMP: captured_images\pixelink_capture_20251004_173616.bmp (1,311,798 bytes)

Uninitializing camera...

Image capture completed successfully!
```

---

## ⚡ Quick Reference Cheat Sheet

For experienced users who need quick syntax lookups:

### Initialize & Cleanup

```python
from pixelinkWrapper import PxLApi

# Initialize camera (0 = first camera)
ret = PxLApi.initialize(0)
hCamera = ret[1]

# Always check success
if PxLApi.apiSuccess(ret[0]):
    # Success - use hCamera
    pass

# Cleanup when done
PxLApi.uninitialize(hCamera)
```

### Quick Capture (Copy & Paste)

```python
from pixelinkWrapper import PxLApi
from ctypes import create_string_buffer

# Initialize
ret = PxLApi.initialize(0)
hCamera = ret[1]

# Get buffer size
ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.ROI)
width = int(ret[2][PxLApi.RoiParams.WIDTH])
height = int(ret[2][PxLApi.RoiParams.HEIGHT])
ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.PIXEL_FORMAT)
pixel_format = int(ret[2][0])
buffer_size = width * height * PxLApi.getBytesPerPixel(pixel_format)

# Capture
rawImage = create_string_buffer(buffer_size)
PxLApi.setStreamState(hCamera, PxLApi.StreamState.START)
ret = PxLApi.getNextFrame(hCamera, rawImage)
frameDesc = ret[1]
PxLApi.setStreamState(hCamera, PxLApi.StreamState.STOP)

# Save as JPEG
ret = PxLApi.formatImage(rawImage, frameDesc, PxLApi.ImageFormat.JPEG)
with open("image.jpg", "wb") as f:
    f.write(ret[1])

# Cleanup
PxLApi.uninitialize(hCamera)
```

### Common Operations Quick Syntax

| Operation         | Code                                                                                               |
| ----------------- | -------------------------------------------------------------------------------------------------- |
| **Get Exposure**  | `ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.EXPOSURE)` <br> `exposure = ret[2][0]`          |
| **Set Exposure**  | `PxLApi.setFeature(hCamera, PxLApi.FeatureId.EXPOSURE,` <br> `PxLApi.FeatureFlags.MANUAL, [50.0])` |
| **Auto Exposure** | `PxLApi.setFeature(hCamera, PxLApi.FeatureId.EXPOSURE,` <br> `PxLApi.FeatureFlags.AUTO, [])`       |
| **Get Gain**      | `ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.GAIN)` <br> `gain = ret[2][0]`                  |
| **Set Gain**      | `PxLApi.setFeature(hCamera, PxLApi.FeatureId.GAIN,` <br> `PxLApi.FeatureFlags.MANUAL, [6.0])`      |
| **Start Stream**  | `PxLApi.setStreamState(hCamera, PxLApi.StreamState.START)`                                         |
| **Stop Stream**   | `PxLApi.setStreamState(hCamera, PxLApi.StreamState.STOP)`                                          |
| **Save Settings** | `PxLApi.saveSettings(hCamera, "config.pfs")`                                                       |
| **Load Settings** | `PxLApi.loadSettings(hCamera, "config.pfs")`                                                       |

### Image Format Constants

```python
PxLApi.ImageFormat.JPEG      # Compressed JPEG
PxLApi.ImageFormat.BMP       # Windows Bitmap
PxLApi.ImageFormat.TIFF      # TIFF format
PxLApi.ImageFormat.PNG       # PNG format
PxLApi.ImageFormat.RAW_BGR24 # 24-bit BGR raw
PxLApi.ImageFormat.RAW_RGB48 # 48-bit RGB raw
PxLApi.ImageFormat.RAW_MONO8 # 8-bit grayscale
```

---

## 📚 Understanding the Code

### Core Workflow

The image capture process follows these steps:

```
1. Initialize Camera → 2. Determine Image Size → 3. Allocate Buffer →
4. Start Stream → 5. Capture Frame → 6. Stop Stream →
7. Format Image → 8. Save to File → 9. Uninitialize Camera
```

### Key Functions Explained

#### 1. **Camera Initialization**

```python
ret = PxLApi.initialize(0)
hCamera = ret[1]
```

- `initialize(0)` connects to the first available camera
- Returns a tuple: `(return_code, camera_handle)`
- The camera handle (`hCamera`) is used for all subsequent operations

#### 2. **Determining Buffer Size**

```python
rawImageSize = determine_raw_image_size(hCamera)
```

This function calculates the required buffer size based on:

- **ROI (Region of Interest)**: Width and height of the capture area
- **Pixel Addressing**: Decimation/binning settings
- **Pixel Format**: Bytes per pixel (e.g., MONO8, RGB24)

**Formula:**

```
Buffer Size = (Width / PixelAddressingX) × (Height / PixelAddressingY) × BytesPerPixel
```

#### 3. **Creating the Buffer**

```python
from ctypes import create_string_buffer
rawImage = create_string_buffer(rawImageSize)
```

- Uses `ctypes` to create a mutable C-style buffer
- This buffer is passed to the camera API for efficient data transfer
- **Important:** Must use `create_string_buffer()` for compatibility

#### 4. **Capturing a Frame**

```python
ret = PxLApi.setStreamState(hCamera, PxLApi.StreamState.START)
ret = PxLApi.getNextFrame(hCamera, rawImage)
frameDescriptor = ret[1]
```

- **Start streaming**: Tells camera to begin capturing
- **getNextFrame**: Blocking call that waits for next frame
- **Frame descriptor**: Contains metadata (timestamp, frame number, etc.)

#### 5. **Formatting the Image**

```python
ret = PxLApi.formatImage(rawImage, frameDescriptor, PxLApi.ImageFormat.JPEG)
formattedImage = ret[1]
```

- Converts raw sensor data to standard image format
- Supported formats: JPEG, BMP, TIFF, PSD, PNG, and raw formats

#### 6. **Saving to File**

```python
with open(fileName, "wb") as file:
    file.write(formattedImage)
```

- Simple binary write operation
- No additional libraries needed for JPEG/BMP

### ⚠️ Critical Implementation Patterns

#### Return Value Pattern

**Every** API call returns a tuple: `(return_code, data)`

```python
ret = PxLApi.someFunction(hCamera)
if PxLApi.apiSuccess(ret[0]):
    result = ret[1]  # Only access on success - data location varies!
else:
    print(f"Error: {ret[0]}")
```

**Important**: Never access `ret[1]` or `ret[2]` without checking `ret[0]` first!

#### Feature API Data Location

When using `getFeature()`, the data is in **`ret[2]`**, not `ret[1]`:

```python
# Get feature - note ret[2]!
ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.EXPOSURE)
if PxLApi.apiSuccess(ret[0]):
    value = ret[2][0]  # Data is in ret[2], not ret[1]!
    print(f"Exposure: {value} ms")

# Set feature
PxLApi.setFeature(hCamera, PxLApi.FeatureId.EXPOSURE,
                  PxLApi.FeatureFlags.MANUAL, [50.0])
```

#### Camera Handle is Sacred

The camera handle from `initialize()` must be passed to **all** subsequent operations:

```python
ret = PxLApi.initialize(0)
hCamera = ret[1]  # ALWAYS store this!

# All operations need hCamera:
PxLApi.getFeature(hCamera, ...)
PxLApi.setStreamState(hCamera, ...)
PxLApi.getNextFrame(hCamera, ...)
PxLApi.uninitialize(hCamera)  # Don't forget cleanup!
```

Loss of this handle means you must re-initialize the camera.

#### Buffer Size Calculation - Never Hardcode!

**Always** calculate buffer size dynamically:

```python
# ✅ CORRECT - Calculate from camera settings
ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.ROI)
width = ret[2][PxLApi.RoiParams.WIDTH]
height = ret[2][PxLApi.RoiParams.HEIGHT]

ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.PIXEL_FORMAT)
pixel_format = int(ret[2][0])

buffer_size = width * height * PxLApi.getBytesPerPixel(pixel_format)
rawImage = create_string_buffer(buffer_size)

# ❌ WRONG - Hardcoded sizes will fail!
rawImage = create_string_buffer(1000000)  # Don't do this!
```

Formula: `(width / addressing_x) × (height / addressing_y) × bytes_per_pixel`

#### String Decoding Pattern

Camera info returns bytes - always decode:

```python
info = PxLApi.getCameraInfo(hCamera)[1]

# ✅ CORRECT - Decode bytes to string
model = info.ModelName.decode('utf-8')
serial = info.SerialNumber.decode('utf-8')

# ❌ WRONG - Using bytes directly
print(info.ModelName)  # Prints: b'B701' (not clean!)
```

---

## 🖼️ Image Formats

The Pixelink API supports multiple image formats:

| Format        | Constant                       | File Extension | Description          | Size            |
| ------------- | ------------------------------ | -------------- | -------------------- | --------------- |
| **JPEG**      | `PxLApi.ImageFormat.JPEG`      | `.jpg`         | Compressed, lossy    | Small (~80 KB)  |
| **BMP**       | `PxLApi.ImageFormat.BMP`       | `.bmp`         | Uncompressed bitmap  | Large (~1.3 MB) |
| **TIFF**      | `PxLApi.ImageFormat.TIFF`      | `.tiff`        | Uncompressed, tagged | Large           |
| **PSD**       | `PxLApi.ImageFormat.PSD`       | `.psd`         | Photoshop format     | Large           |
| **PNG**       | `PxLApi.ImageFormat.PNG`       | `.png`         | Compressed, lossless | Medium          |
| **RAW_BGR24** | `PxLApi.ImageFormat.RAW_BGR24` | `.bin`         | Raw 24-bit BGR       | Large           |
| **RAW_RGB48** | `PxLApi.ImageFormat.RAW_RGB48` | `.bin`         | Raw 48-bit RGB       | Very Large      |
| **RAW_MONO8** | `PxLApi.ImageFormat.RAW_MONO8` | `.bin`         | Raw 8-bit grayscale  | Medium          |

### When to Use Each Format

- **JPEG**: Quick previews, web display, space-constrained storage
- **BMP**: Fast processing, no compression artifacts, Windows applications
- **TIFF**: Professional photography, archival, multi-page documents
- **PNG**: Lossless compression, transparency support
- **RAW formats**: Scientific imaging, custom post-processing, maximum data preservation

---

## 🎛️ Camera Settings

### Get Camera Information

```python
camera_info = PxLApi.getCameraInfo(hCamera)
if PxLApi.apiSuccess(camera_info[0]):
    info = camera_info[1]
    print(f"Model: {info.ModelName.decode('utf-8')}")
    print(f"Serial: {info.SerialNumber.decode('utf-8')}")
    print(f"Firmware: {info.FirmwareVersion.decode('utf-8')}")
```

### Adjust Exposure

```python
# Get current exposure
ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.EXPOSURE)
current_exposure = ret[2][0]
print(f"Current exposure: {current_exposure} ms")

# Set new exposure (in milliseconds)
new_exposure = 50.0  # 50ms
params = [new_exposure]
ret = PxLApi.setFeature(hCamera, PxLApi.FeatureId.EXPOSURE,
                        PxLApi.FeatureFlags.MANUAL, params)
```

### Adjust Gain

```python
# Get current gain
ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.GAIN)
current_gain = ret[2][0]

# Set new gain (in dB)
new_gain = 6.0
params = [new_gain]
ret = PxLApi.setFeature(hCamera, PxLApi.FeatureId.GAIN,
                        PxLApi.FeatureFlags.MANUAL, params)
```

### Enable Auto Exposure

```python
ret = PxLApi.setFeature(hCamera, PxLApi.FeatureId.EXPOSURE,
                        PxLApi.FeatureFlags.AUTO, [])
```

### ROI (Region of Interest)

Capture only a portion of the sensor:

```python
# Set ROI: x=100, y=100, width=800, height=600
roi_params = [
    100,  # X offset
    100,  # Y offset
    800,  # Width
    600   # Height
]
ret = PxLApi.setFeature(hCamera, PxLApi.FeatureId.ROI,
                        PxLApi.FeatureFlags.MANUAL, roi_params)
```

### White Balance

```python
# Auto white balance
ret = PxLApi.setFeature(hCamera, PxLApi.FeatureId.WHITE_SHADING,
                        PxLApi.FeatureFlags.AUTO, [])

# Manual white balance (R, G, B gains)
wb_params = [1.5, 1.0, 1.2]  # Red, Green, Blue
ret = PxLApi.setFeature(hCamera, PxLApi.FeatureId.WHITE_SHADING,
                        PxLApi.FeatureFlags.MANUAL, wb_params)
```

### Gamma Correction

```python
# Get current gamma
ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.GAMMA)
current_gamma = ret[2][0]
print(f"Current gamma: {current_gamma}")

# Set gamma (typical values: 1.0 - 2.2)
PxLApi.setFeature(hCamera, PxLApi.FeatureId.GAMMA,
                  PxLApi.FeatureFlags.MANUAL, [1.8])
```

### Frame Rate

```python
# Get actual frame rate
ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.ACTUAL_FRAME_RATE)
fps = ret[2][0]
print(f"Current frame rate: {fps} FPS")
```

### Save and Load Camera Settings

```python
# Save current settings to file
ret = PxLApi.saveSettings(hCamera, "my_camera_config.pfs")
if PxLApi.apiSuccess(ret[0]):
    print("Settings saved successfully")

# Load settings from file
ret = PxLApi.loadSettings(hCamera, "my_camera_config.pfs")
if PxLApi.apiSuccess(ret[0]):
    print("Settings loaded successfully")

# Save to factory defaults
PxLApi.saveSettings(hCamera, PxLApi.Settings.SETTINGS_FACTORY)

# Load factory defaults
PxLApi.loadSettings(hCamera, PxLApi.Settings.SETTINGS_FACTORY)
```

### Check Feature Support

```python
# Check if a feature is supported
ret = PxLApi.getCameraFeatures(hCamera, PxLApi.FeatureId.FOCUS)
if PxLApi.apiSuccess(ret[0]):
    print("Focus is supported")
    features = ret[1]
    # Get min/max values
    for param in features.Params:
        print(f"Min: {param.fMinValue}")
        print(f"Max: {param.fMaxValue}")
else:
    print("Focus is NOT supported")
```

---

## 🚀 Advanced Features

### Triggering

#### Software Trigger

```python
# Enable software trigger
trigger_params = [
    PxLApi.TriggerModes.MODE_0,  # Trigger mode
    PxLApi.TriggerTypes.SOFTWARE,  # Trigger type
    PxLApi.Polarity.ACTIVE_HIGH,  # Polarity
    0,  # Delay
    0   # Parameter
]
ret = PxLApi.setFeature(hCamera, PxLApi.FeatureId.TRIGGER,
                        PxLApi.FeatureFlags.MANUAL, trigger_params)

# Start stream
PxLApi.setStreamState(hCamera, PxLApi.StreamState.START)

# Trigger the camera
ret = PxLApi.setFeature(hCamera, PxLApi.FeatureId.TRIGGER,
                        PxLApi.FeatureFlags.ONEPUSH, [])

# Get the triggered frame
ret = PxLApi.getNextFrame(hCamera, rawImage)
```

### Continuous Capture

```python
# Capture 10 images
for i in range(10):
    ret = PxLApi.getNextFrame(hCamera, rawImage)
    if PxLApi.apiSuccess(ret[0]):
        frameDescriptor = ret[1]

        # Format and save
        ret = PxLApi.formatImage(rawImage, frameDescriptor,
                                 PxLApi.ImageFormat.JPEG)
        with open(f"image_{i:03d}.jpg", "wb") as f:
            f.write(ret[1])

        print(f"Captured frame {i+1}/10")

    time.sleep(0.1)  # 100ms delay
```

---

### Stream Control

```python
# Start streaming
PxLApi.setStreamState(hCamera, PxLApi.StreamState.START)

# Pause streaming
PxLApi.setStreamState(hCamera, PxLApi.StreamState.PAUSE)

# Stop streaming
PxLApi.setStreamState(hCamera, PxLApi.StreamState.STOP)

# Check current stream state
ret = PxLApi.getStreamState(hCamera)
if ret[1] == PxLApi.StreamState.START:
    print("Camera is streaming")
```

### Continuous Capture Loop

```python
import time

PxLApi.setStreamState(hCamera, PxLApi.StreamState.START)

try:
    while True:
        ret = PxLApi.getNextFrame(hCamera, rawImage)
        if PxLApi.apiSuccess(ret[0]):
            frameDesc = ret[1]
            # Process frame here
            print(f"Frame {frameDesc.uFrameNumber}")
        else:
            print(f"Error: {ret[0]}")

        time.sleep(0.1)  # 100ms delay

except KeyboardInterrupt:
    print("Stopping...")

finally:
    PxLApi.setStreamState(hCamera, PxLApi.StreamState.STOP)
    PxLApi.uninitialize(hCamera)
```

---

## 📖 API Reference

### Common Return Codes

```python
PxLApi.ReturnCode.ApiSuccess              # Operation successful
PxLApi.ReturnCode.ApiInvalidHandleError   # Invalid camera handle
PxLApi.ReturnCode.ApiInvalidParameterError # Invalid parameter
PxLApi.ReturnCode.ApiNotSupportedError    # Feature not supported
PxLApi.ReturnCode.ApiCameraTimeoutError   # Camera timeout (retry)
PxLApi.ReturnCode.ApiBufferTooSmall       # Buffer too small
```

### Checking for Success

```python
if PxLApi.apiSuccess(ret[0]):
    # Operation succeeded
    data = ret[1]
else:
    # Operation failed
    print(f"Error code: {ret[0]}")
```

### Essential Camera Features

| Feature       | FeatureId                            | Description           |
| ------------- | ------------------------------------ | --------------------- |
| Exposure      | `PxLApi.FeatureId.EXPOSURE`          | Integration time (ms) |
| Gain          | `PxLApi.FeatureId.GAIN`              | Sensor gain (dB)      |
| ROI           | `PxLApi.FeatureId.ROI`               | Region of interest    |
| Pixel Format  | `PxLApi.FeatureId.PIXEL_FORMAT`      | Color/mono format     |
| White Balance | `PxLApi.FeatureId.WHITE_SHADING`     | Color correction      |
| Gamma         | `PxLApi.FeatureId.GAMMA`             | Gamma correction      |
| Trigger       | `PxLApi.FeatureId.TRIGGER`           | Trigger configuration |
| Frame Rate    | `PxLApi.FeatureId.ACTUAL_FRAME_RATE` | Current frame rate    |

### Stream States

```python
PxLApi.StreamState.START   # Start streaming
PxLApi.StreamState.STOP    # Stop streaming
PxLApi.StreamState.PAUSE   # Pause streaming
```

### Feature Flags

```python
PxLApi.FeatureFlags.MANUAL    # Manual control
PxLApi.FeatureFlags.AUTO      # Automatic control
PxLApi.FeatureFlags.ONEPUSH   # One-time auto adjustment
PxLApi.FeatureFlags.OFF       # Feature disabled
PxLApi.FeatureFlags.PRESENCE  # Feature is present
```

### Common Pixel Formats

| Format         | Description       | Bytes/Pixel |
| -------------- | ----------------- | ----------- |
| `MONO8`        | 8-bit grayscale   | 1           |
| `MONO16`       | 16-bit grayscale  | 2           |
| `BAYER8_GRBG`  | 8-bit Bayer GRBG  | 1           |
| `BAYER16_GRBG` | 16-bit Bayer GRBG | 2           |
| `RGB24`        | 24-bit RGB        | 3           |
| `RGB48`        | 48-bit RGB        | 6           |
| `YUV422`       | YUV 4:2:2         | 2           |

### Helper Functions

```python
# Get bytes per pixel for a pixel format
pixel_format = PxLApi.PixelFormat.MONO8
bytes_per_pixel = PxLApi.getBytesPerPixel(pixel_format)

# Calculate image size
width = 1920
height = 1080
image_size = PxLApi.getBytesPerPixel(pixel_format) * width * height
```

---

## 🔍 Troubleshooting

### Common Issues and Solutions

#### 1. **"Module 'pixelinkWrapper' not found"**

**Solution:**

```powershell
# Install the wrapper
pip install pixelinkWrapper

# Or if using Python 3 explicitly
pip3 install pixelinkWrapper

# Check installation
pip list | Select-String pixelink
```

#### 2. **"WinError 2: The system cannot find the file specified"**

This error occurs because the wrapper tries to run `wmic` command which is deprecated in newer Windows versions.

**Solution:** The script includes a workaround that patches the subprocess call. You'll see a warning, but it will work.

#### 3. **"Could not initialize camera"**

**Checklist:**

- [ ] Camera is connected to USB port
- [ ] Camera drivers are installed (comes with SDK)
- [ ] Camera appears in Windows Device Manager
- [ ] No other application is using the camera
- [ ] Try a different USB port
- [ ] Restart the camera or computer

**Verify camera in Device Manager:**

```powershell
# Open Device Manager
devmgmt.msc
```

Look under "Imaging devices" or "Pixelink Cameras"

#### 4. **"ApiCameraTimeoutError"**

This can happen occasionally with frame capture.

**Solution:** The script includes retry logic (4 attempts). If it persists:

- Check USB cable connection
- Try a different USB port (USB 3.0 recommended)
- Reduce frame rate or increase exposure time

#### 5. **Images are too dark/bright**

**Solution:** Adjust exposure and gain:

```python
# Increase exposure for brighter images
params = [100.0]  # 100ms
PxLApi.setFeature(hCamera, PxLApi.FeatureId.EXPOSURE,
                  PxLApi.FeatureFlags.MANUAL, params)

# Or use auto exposure
PxLApi.setFeature(hCamera, PxLApi.FeatureId.EXPOSURE,
                  PxLApi.FeatureFlags.AUTO, [])
```

#### 6. **Buffer size errors**

**Error:** `ApiBufferTooSmall`

**Solution:** The script calculates buffer size automatically. If you get this error:

```python
# Manually allocate a larger buffer
MAX_IMAGE_SIZE = 5000 * 5000 * 2  # 50 megapixels
rawImage = create_string_buffer(MAX_IMAGE_SIZE)
```

---

## 💡 Sample Code Snippets

### Complete Minimal Example

```python
from pixelinkWrapper import PxLApi
from ctypes import create_string_buffer

# Initialize camera
ret = PxLApi.initialize(0)
hCamera = ret[1]

# Get image size
ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.ROI)
width = int(ret[2][PxLApi.RoiParams.WIDTH])
height = int(ret[2][PxLApi.RoiParams.HEIGHT])

ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.PIXEL_FORMAT)
pixel_format = int(ret[2][0])
pixel_size = PxLApi.getBytesPerPixel(pixel_format)

buffer_size = width * height * pixel_size
rawImage = create_string_buffer(buffer_size)

# Capture image
PxLApi.setStreamState(hCamera, PxLApi.StreamState.START)
ret = PxLApi.getNextFrame(hCamera, rawImage)
frameDesc = ret[1]
PxLApi.setStreamState(hCamera, PxLApi.StreamState.STOP)

# Save as JPEG
ret = PxLApi.formatImage(rawImage, frameDesc, PxLApi.ImageFormat.JPEG)
with open("capture.jpg", "wb") as f:
    f.write(ret[1])

# Cleanup
PxLApi.uninitialize(hCamera)
```

### List All Connected Cameras

```python
from pixelinkWrapper import PxLApi

ret = PxLApi.getNumberCameras()
if PxLApi.apiSuccess(ret[0]):
    num_cameras = ret[1]
    print(f"Found {num_cameras} camera(s)")

    for i in range(num_cameras):
        ret = PxLApi.initialize(i)
        if PxLApi.apiSuccess(ret[0]):
            hCamera = ret[1]

            info = PxLApi.getCameraInfo(hCamera)
            if PxLApi.apiSuccess(info[0]):
                print(f"\nCamera {i}:")
                print(f"  Model: {info[1].ModelName.decode('utf-8')}")
                print(f"  Serial: {info[1].SerialNumber.decode('utf-8')}")

            PxLApi.uninitialize(hCamera)
```

### Time-Lapse Capture

```python
import time
from datetime import datetime
from pixelinkWrapper import PxLApi
from ctypes import create_string_buffer

# Setup camera
ret = PxLApi.initialize(0)
hCamera = ret[1]

# Determine buffer size (use the determine_raw_image_size function)
rawImageSize = determine_raw_image_size(hCamera)
rawImage = create_string_buffer(rawImageSize)

# Start streaming
PxLApi.setStreamState(hCamera, PxLApi.StreamState.START)

# Capture every 5 seconds for 1 minute
interval = 5  # seconds
duration = 60  # seconds
num_captures = duration // interval

for i in range(num_captures):
    # Capture frame
    ret = PxLApi.getNextFrame(hCamera, rawImage)
    if PxLApi.apiSuccess(ret[0]):
        frameDesc = ret[1]

        # Format as JPEG
        ret = PxLApi.formatImage(rawImage, frameDesc, PxLApi.ImageFormat.JPEG)

        # Save with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"timelapse_{timestamp}.jpg"
        with open(filename, "wb") as f:
            f.write(ret[1])

        print(f"Captured {i+1}/{num_captures}: {filename}")

    # Wait for next interval
    time.sleep(interval)

# Cleanup
PxLApi.setStreamState(hCamera, PxLApi.StreamState.STOP)
PxLApi.uninitialize(hCamera)
```

### Save Camera Settings

```python
# Save current settings to a file
ret = PxLApi.saveSettings(hCamera, "my_camera_config.pfs")
if PxLApi.apiSuccess(ret[0]):
    print("Settings saved successfully")

# Load settings later
ret = PxLApi.loadSettings(hCamera, "my_camera_config.pfs")
if PxLApi.apiSuccess(ret[0]):
    print("Settings loaded successfully")
```

---

## ⚡ Performance Tips

### Optimize Frame Capture

```python
# Pre-allocate buffer ONCE outside loop
buffer_size = determine_raw_image_size(hCamera)
rawImage = create_string_buffer(buffer_size)

# Reuse buffer in loop - much faster!
for i in range(100):
    ret = PxLApi.getNextFrame(hCamera, rawImage)
    # Process frame...
```

### Keep Stream Running

```python
# DON'T do this (slow - stops/starts stream each time)
for i in range(100):
    PxLApi.setStreamState(hCamera, PxLApi.StreamState.START)
    ret = PxLApi.getNextFrame(hCamera, rawImage)
    PxLApi.setStreamState(hCamera, PxLApi.StreamState.STOP)

# DO this (fast - stream stays running)
PxLApi.setStreamState(hCamera, PxLApi.StreamState.START)
for i in range(100):
    ret = PxLApi.getNextFrame(hCamera, rawImage)
    # Process...
PxLApi.setStreamState(hCamera, PxLApi.StreamState.STOP)
```

### Retry Logic for Timeouts

```python
def get_frame_with_retry(hCamera, rawImage, max_retries=4):
    """Capture frame with automatic retry on timeout"""
    for attempt in range(max_retries):
        ret = PxLApi.getNextFrame(hCamera, rawImage)
        if PxLApi.apiSuccess(ret[0]):
            return ret
        elif ret[0] == PxLApi.ReturnCode.ApiCameraTimeoutError:
            print(f"Timeout, retry {attempt+1}/{max_retries}")
            continue
        else:
            # Different error - don't retry
            return ret
    return ret  # Return last attempt
```

### Error Handling Best Practices

```python
# Template for robust error handling
ret = PxLApi.someFunction(hCamera, params)
if PxLApi.apiSuccess(ret[0]):
    # Success path
    result = ret[1]
    print(f"Success: {result}")
else:
    # Error path - handle specific errors
    error_code = ret[0]
    if error_code == PxLApi.ReturnCode.ApiInvalidHandleError:
        print("ERROR: Invalid camera handle - reinitialize camera")
    elif error_code == PxLApi.ReturnCode.ApiCameraTimeoutError:
        print("WARNING: Camera timeout - will retry")
    elif error_code == PxLApi.ReturnCode.ApiNotSupportedError:
        print("INFO: Feature not supported on this camera")
    else:
        print(f"ERROR: Unknown error code {error_code}")
```

### Pro Tips

1. ✅ **Always check return codes** with `apiSuccess()` before using data
2. ✅ **Start stream before** calling `getNextFrame()`
3. ✅ **Stop stream before** calling `uninitialize()`
4. ✅ **Reuse buffers** instead of allocating new ones in loops
5. ✅ **Keep streams running** for continuous capture
6. ✅ **Implement retry logic** for timeout errors
7. ✅ **Save settings** to files for reproducible configurations
8. ✅ **Check feature support** before using advanced features
9. ✅ **Use auto features** (exposure, gain) for quick setup
10. ✅ **Calculate buffer size correctly** to avoid crashes

---

## ❌ Common Pitfalls & Best Practices

### What NOT to Do

1. **❌ Don't access return data without checking success**

   ```python
   # WRONG!
   ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.EXPOSURE)
   value = ret[2][0]  # Might crash if ret[0] is error!

   # CORRECT!
   ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.EXPOSURE)
   if PxLApi.apiSuccess(ret[0]):
       value = ret[2][0]  # Safe to access
   ```

2. **❌ Don't uninitialize camera while streaming**

   ```python
   # WRONG!
   PxLApi.setStreamState(hCamera, PxLApi.StreamState.START)
   PxLApi.uninitialize(hCamera)  # BAD - still streaming!

   # CORRECT!
   PxLApi.setStreamState(hCamera, PxLApi.StreamState.START)
   # ... capture frames ...
   PxLApi.setStreamState(hCamera, PxLApi.StreamState.STOP)  # Stop first!
   PxLApi.uninitialize(hCamera)  # Now safe
   ```

3. **❌ Don't hardcode buffer sizes**

   ```python
   # WRONG!
   rawImage = create_string_buffer(2000000)  # Magic number!

   # CORRECT!
   buffer_size = determine_raw_image_size(hCamera)
   rawImage = create_string_buffer(buffer_size)
   ```

4. **❌ Don't assume frame capture always succeeds**

   ```python
   # WRONG!
   ret = PxLApi.getNextFrame(hCamera, rawImage)
   frameDesc = ret[1]  # Might fail!

   # CORRECT!
   MAX_RETRIES = 4
   for attempt in range(MAX_RETRIES):
       ret = PxLApi.getNextFrame(hCamera, rawImage)
       if PxLApi.apiSuccess(ret[0]):
           frameDesc = ret[1]
           break
   ```

5. **❌ Don't modify vendored library files**

   - Never edit files in `pixelinkPythonWrapper-master/`
   - It's a vendored library - your changes will be lost on updates

6. **❌ Don't forget to decode camera info strings**

   ```python
   # WRONG!
   print(info.ModelName)  # Prints: b'B701'

   # CORRECT!
   print(info.ModelName.decode('utf-8'))  # Prints: B701
   ```

### Development Best Practices

#### When Writing New Scripts

1. **Start from `capture_image.py`** - It's the canonical reference
2. **Import with error handling** - Use the wmic workaround pattern
3. **Create buffers correctly** - Use `from ctypes import create_string_buffer`
4. **Check all return codes** - Use `PxLApi.apiSuccess(ret[0])` before accessing data
5. **Manage streaming state** - Start before capture, stop before uninitialize
6. **Use retry loops** - `getNextFrame()` can timeout, retry 3-4 times

#### Testing Patterns

1. **Always test with camera connected** - These are hardware integration scripts
2. **Check Device Manager** - Camera must appear under "Imaging devices" (Windows)
3. **No unit tests** - This is a hardware interface project; use manual verification
4. **Verify image output** - Check `captured_images/` directory for results
5. **Test error conditions** - Disconnect camera, use wrong settings, etc.

#### Auto vs Manual Modes

```python
# Auto mode: pass empty list, use AUTO flag
PxLApi.setFeature(hCamera, PxLApi.FeatureId.EXPOSURE,
                  PxLApi.FeatureFlags.AUTO, [])

# Manual mode: pass parameters, use MANUAL flag
PxLApi.setFeature(hCamera, PxLApi.FeatureId.EXPOSURE,
                  PxLApi.FeatureFlags.MANUAL, [50.0])

# One-push: trigger once, then manual
PxLApi.setFeature(hCamera, PxLApi.FeatureId.EXPOSURE,
                  PxLApi.FeatureFlags.ONEPUSH, [])
```

### Platform-Specific Notes

#### Windows

- **Primary platform** for Pixelink SDK
- **wmic workaround required** for Windows 10 21H1+ and Windows 11
- SDK installs to: `C:\Program Files\Pixelink\`
- Check Device Manager for camera (under "Imaging devices")

#### Linux

- Supported via `libPxLApi.so`
- See `samples/Linux/` for platform-specific examples
- No wmic issues on Linux

#### macOS

- **NOT SUPPORTED** - Pixelink SDK not available for macOS
- This project can be edited on macOS but cannot run
- Development on macOS is for documentation/script writing only

---

## 📚 Additional Resources

### Official Documentation

- **Pixelink SDK Documentation**: Included with SDK installation at:
  - `C:\Program Files\Pixelink\Documentation\`
- **Python Wrapper GitHub**:
  - https://github.com/pixelink-support/pixelinkPythonWrapper
- **Sample Code**: Located in:
  - `pixelinkPythonWrapper-master\samples\Windows\`

### Useful Samples in SDK

| Sample                | Description                                       |
| --------------------- | ------------------------------------------------- |
| `getSnapshot.py`      | Basic image capture (what our script is based on) |
| `getNextFrame.py`     | Continuous frame capture                          |
| `autoExposure.py`     | Auto exposure configuration                       |
| `autoWhiteBalance.py` | White balance adjustment                          |
| `triggering.py`       | Hardware/software triggering                      |
| `preview.py`          | Live preview window                               |
| `getCameraFeature.py` | Query camera capabilities                         |
| `setFeature.py`       | Modify camera settings                            |

### Support

**Pixelink Technical Support:**

- Create a ticket: https://support.pixelink.com/support/tickets/new
- Phone: Contact information on Navitar website
- Email: Available through support portal

### Key Reference Files in This Project

When working on specific features, reference these files:

| Feature                   | Reference File                                    |
| ------------------------- | ------------------------------------------------- |
| **Buffer allocation**     | `capture_image.py` → `determine_raw_image_size()` |
| **Error handling**        | `capture_image.py` → `get_raw_image()` retry loop |
| **Import workaround**     | `capture_image.py` → Lines 13-35 (wmic fix)       |
| **Camera info**           | `test_autofocus.py` → Feature detection pattern   |
| **Format conversion**     | `capture_image.py` → `get_snapshot()` function    |
| **Windows compatibility** | `capture_image.py` → subprocess patching pattern  |

### Project File Structure

```
PyCore/
├── capture_image.py              # Main reference implementation
├── test_autofocus.py             # Feature detection example
├── README.md                     # This comprehensive guide
├── email_to_pixelink.txt        # Support email template
├── captured_images/             # Output directory
└── pixelinkPythonWrapper-master/ # Vendored library (don't modify)
    ├── pixelinkWrapper/
    │   └── pixelink.py          # API wrapper
    └── samples/
        ├── Windows/             # Official Windows samples
        └── Linux/               # Official Linux samples
```

### Learning Path

1. ✅ **You are here**: Basic image capture
2. 📖 Experiment with different image formats
3. 🎛️ Try adjusting camera settings (exposure, gain)
4. 📹 Implement continuous capture
5. ⚡ Add triggering capabilities
6. 🖥️ Create a preview window
7. 🚀 Build a custom application

---

## 📝 Important Notes

### Critical Requirements

- ⚠️ **Return codes**: ALWAYS check `PxLApi.apiSuccess(ret[0])` before accessing data
- ⚠️ **Camera handle**: Store `hCamera = ret[1]` - needed for ALL operations
- ⚠️ **Streaming state**: Must call `setStreamState(STOP)` before `uninitialize()`
- ⚠️ **Buffer allocation**: NEVER hardcode sizes - calculate from camera settings
- ⚠️ **Blocking calls**: `getNextFrame()` blocks thread until frame available
- ⚠️ **Retry logic**: Implement 3-4 retry attempts for timeout errors

### Data Access Patterns

- 📍 `getFeature()` returns data in **`ret[2]`**, not `ret[1]`
- 📍 `getCameraInfo()` returns data in `ret[1]`
- 📍 `getNextFrame()` returns frame descriptor in `ret[1]`
- 📍 Camera info strings are **bytes** - use `.decode('utf-8')`

### Platform-Specific

- 🪟 **Windows**: wmic workaround required (included in `capture_image.py`)
- 🐧 **Linux**: Full support via `libPxLApi.so`
- 🍎 **macOS**: NOT SUPPORTED - no Pixelink SDK available

### Image Format Selection

- 🔬 **Scientific imaging**: Use BMP or raw formats (NOT JPEG)
- 📊 **JPEG compression**: Introduces artifacts unsuitable for quantitative analysis
- 💾 **File sizes**: JPEG (~80KB) vs BMP (~1.3MB) for typical image

### Camera Capabilities (B701 Specific)

- ✅ **Supported**: Exposure, Gain, Gamma, Sharpness
- ❌ **NOT Supported**: Focus (fixed lens), Brightness, Saturation, White Balance, Zoom, Iris

---

## ⚖️ License

This code is provided as-is for use with Pixelink cameras. Based on official Pixelink SDK samples and documentation.

---

## 🎓 Learning Tips

1. **Start Simple**: Run the basic capture script first
2. **Read Error Messages**: They're descriptive and helpful
3. **Use API Documentation**: Refer to SDK docs for feature details
4. **Experiment**: Try different settings and see what happens
5. **Check Return Codes**: Always verify `apiSuccess()` before using results
6. **Study Samples**: The SDK includes many example scripts

---

**Last Updated**: October 4, 2025  
**Camera Tested**: Pixelink B701 (Serial: 771001279)  
**Supported Features**: Exposure, Gain, Gamma, Sharpness  
**NOT Supported**: Focus, Brightness, Saturation, White Balance, Zoom, Iris  
**SDK Version**: 10.0.0  
**Python Version**: 3.11

---

## 📝 Notes

- All operations require a valid camera handle from `initialize()`
- The Pixelink B701 has a **fixed-focus lens** (no autofocus)
- `getNextFrame()` is a **blocking call** - won't return until frame is available
- Always call `setStreamState(STOP)` before `uninitialize()`
- Buffer size calculation is critical - use `determine_raw_image_size()`
- The wmic workaround is required for Windows 10 21H1+ and Windows 11
- For scientific imaging, use **BMP or raw formats** (not JPEG)
- JPEG compression introduces artifacts unsuitable for quantitative analysis
