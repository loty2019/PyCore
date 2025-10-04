# Pixelink Camera Python Guide

A comprehensive guide and working examples for capturing images from Pixelink cameras using Python and the Pixelink SDK.

## 📋 Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Understanding the Code](#understanding-the-code)
- [Image Formats](#image-formats)
- [Advanced Features](#advanced-features)
- [API Reference](#api-reference)
- [Troubleshooting](#troubleshooting)
- [Sample Code Snippets](#sample-code-snippets)

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

## 🎛️ Advanced Features

### 1. Camera Settings

#### Get Camera Information

```python
camera_info = PxLApi.getCameraInfo(hCamera)
if PxLApi.apiSuccess(camera_info[0]):
    info = camera_info[1]
    print(f"Model: {info.ModelName.decode('utf-8')}")
    print(f"Serial: {info.SerialNumber.decode('utf-8')}")
    print(f"Firmware: {info.FirmwareVersion.decode('utf-8')}")
```

#### Adjust Exposure

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

#### Adjust Gain

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

#### Enable Auto Exposure

```python
ret = PxLApi.setFeature(hCamera, PxLApi.FeatureId.EXPOSURE,
                        PxLApi.FeatureFlags.AUTO, [])
```

### 2. ROI (Region of Interest)

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

### 3. White Balance

```python
# Auto white balance
ret = PxLApi.setFeature(hCamera, PxLApi.FeatureId.WHITE_SHADING,
                        PxLApi.FeatureFlags.AUTO, [])

# Manual white balance (R, G, B gains)
wb_params = [1.5, 1.0, 1.2]  # Red, Green, Blue
ret = PxLApi.setFeature(hCamera, PxLApi.FeatureId.WHITE_SHADING,
                        PxLApi.FeatureFlags.MANUAL, wb_params)
```

### 4. Triggering

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

### 5. Continuous Capture

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

### Learning Path

1. ✅ **You are here**: Basic image capture
2. 📖 Experiment with different image formats
3. 🎛️ Try adjusting camera settings (exposure, gain)
4. 📹 Implement continuous capture
5. ⚡ Add triggering capabilities
6. 🖥️ Create a preview window
7. 🚀 Build a custom application

---

## 📝 Notes

- The script includes a workaround for Windows `wmic` deprecation
- All camera operations use the handle returned by `initialize()`
- Always call `uninitialize()` when done
- Use `setStreamState(STOP)` before uninitializing
- Buffer allocation is critical for performance
- Frame capture is a blocking operation

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
**SDK Version**: 10.0.0  
**Python Version**: 3.11
