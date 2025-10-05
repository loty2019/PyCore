# Pixelink Camera - Example Scripts

Collection of ready-to-use Python scripts for common camera operations.

---

## Example 1: Simple Single Capture

**File: `simple_capture.py`**

```python
"""
Simplest possible image capture - just run and get a JPEG
"""
from pixelinkWrapper import PxLApi
from ctypes import create_string_buffer

# Initialize camera
ret = PxLApi.initialize(0)
if not PxLApi.apiSuccess(ret[0]):
    print("Failed to initialize camera")
    exit(1)

hCamera = ret[1]
print("Camera initialized")

# Get image dimensions
ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.ROI)
width = int(ret[2][PxLApi.RoiParams.WIDTH])
height = int(ret[2][PxLApi.RoiParams.HEIGHT])

ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.PIXEL_FORMAT)
pixel_format = int(ret[2][0])
pixel_size = PxLApi.getBytesPerPixel(pixel_format)

buffer_size = width * height * pixel_size
rawImage = create_string_buffer(buffer_size)

# Capture one frame
PxLApi.setStreamState(hCamera, PxLApi.StreamState.START)
ret = PxLApi.getNextFrame(hCamera, rawImage)
frameDesc = ret[1]
PxLApi.setStreamState(hCamera, PxLApi.StreamState.STOP)

# Save as JPEG
ret = PxLApi.formatImage(rawImage, frameDesc, PxLApi.ImageFormat.JPEG)
with open("simple_capture.jpg", "wb") as f:
    f.write(ret[1])

print("Image saved: simple_capture.jpg")

# Cleanup
PxLApi.uninitialize(hCamera)
```

---

## Example 2: List All Cameras

**File: `list_cameras.py`**

```python
"""
Display information about all connected Pixelink cameras
"""
from pixelinkWrapper import PxLApi

# Get number of cameras
ret = PxLApi.getNumberCameras()
if not PxLApi.apiSuccess(ret[0]):
    print("Error getting camera count")
    exit(1)

num_cameras = ret[1]
print(f"Found {num_cameras} Pixelink camera(s)\n")

if num_cameras == 0:
    print("No cameras found. Please check connections.")
    exit(0)

# Enumerate each camera
for i in range(num_cameras):
    ret = PxLApi.initialize(i)
    if PxLApi.apiSuccess(ret[0]):
        hCamera = ret[1]

        print(f"Camera #{i}:")
        print("-" * 50)

        # Get detailed info
        ret = PxLApi.getCameraInfo(hCamera)
        if PxLApi.apiSuccess(ret[0]):
            info = ret[1]

            print(f"  Model:        {info.ModelName.decode('utf-8')}")
            print(f"  Serial:       {info.SerialNumber.decode('utf-8')}")
            print(f"  Firmware:     {info.FirmwareVersion.decode('utf-8')}")
            print(f"  Description:  {info.Description.decode('utf-8')}")

        # Get current settings
        ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.ROI)
        if PxLApi.apiSuccess(ret[0]):
            width = int(ret[2][PxLApi.RoiParams.WIDTH])
            height = int(ret[2][PxLApi.RoiParams.HEIGHT])
            print(f"  Resolution:   {width} x {height}")

        ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.ACTUAL_FRAME_RATE)
        if PxLApi.apiSuccess(ret[0]):
            fps = ret[2][0]
            print(f"  Frame Rate:   {fps:.2f} FPS")

        print()

        PxLApi.uninitialize(hCamera)
```

---

## Example 3: Adjust Exposure and Gain

**File: `adjust_settings.py`**

```python
"""
Capture images with different exposure and gain settings
"""
from pixelinkWrapper import PxLApi
from ctypes import create_string_buffer
import os

def capture_with_settings(hCamera, rawImage, exposure_ms, gain_db, filename):
    """Capture image with specific exposure and gain"""

    # Set exposure
    ret = PxLApi.setFeature(hCamera, PxLApi.FeatureId.EXPOSURE,
                            PxLApi.FeatureFlags.MANUAL, [exposure_ms])
    if not PxLApi.apiSuccess(ret[0]):
        print(f"Failed to set exposure to {exposure_ms}ms")
        return False

    # Set gain
    ret = PxLApi.setFeature(hCamera, PxLApi.FeatureId.GAIN,
                            PxLApi.FeatureFlags.MANUAL, [gain_db])
    if not PxLApi.apiSuccess(ret[0]):
        print(f"Failed to set gain to {gain_db}dB")
        return False

    # Capture frame
    ret = PxLApi.getNextFrame(hCamera, rawImage)
    if not PxLApi.apiSuccess(ret[0]):
        print("Failed to capture frame")
        return False

    frameDesc = ret[1]

    # Save as JPEG
    ret = PxLApi.formatImage(rawImage, frameDesc, PxLApi.ImageFormat.JPEG)
    with open(filename, "wb") as f:
        f.write(ret[1])

    print(f"✓ Captured: {filename} (Exp: {exposure_ms}ms, Gain: {gain_db}dB)")
    return True


# Initialize camera
ret = PxLApi.initialize(0)
hCamera = ret[1]

# Setup buffer
ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.ROI)
width = int(ret[2][PxLApi.RoiParams.WIDTH])
height = int(ret[2][PxLApi.RoiParams.HEIGHT])
ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.PIXEL_FORMAT)
pixel_format = int(ret[2][0])
buffer_size = width * height * PxLApi.getBytesPerPixel(pixel_format)
rawImage = create_string_buffer(buffer_size)

# Create output directory
os.makedirs("exposure_test", exist_ok=True)

# Start streaming
PxLApi.setStreamState(hCamera, PxLApi.StreamState.START)

# Test different exposure values
exposures = [10, 25, 50, 100]  # milliseconds
gains = [0, 3, 6]  # dB

print("Capturing images with different settings...\n")

for exp in exposures:
    for gain in gains:
        filename = f"exposure_test/exp_{exp}ms_gain_{gain}db.jpg"
        capture_with_settings(hCamera, rawImage, exp, gain, filename)

# Cleanup
PxLApi.setStreamState(hCamera, PxLApi.StreamState.STOP)
PxLApi.uninitialize(hCamera)

print("\nAll images saved in 'exposure_test' folder")
```

---

## Example 4: Time-Lapse Photography

**File: `timelapse.py`**

```python
"""
Capture images at regular intervals for time-lapse
"""
from pixelinkWrapper import PxLApi
from ctypes import create_string_buffer
from datetime import datetime
import time
import os

# Configuration
INTERVAL_SECONDS = 5      # Time between captures
DURATION_MINUTES = 2      # How long to capture
OUTPUT_DIR = "timelapse"

# Calculate number of captures
num_captures = (DURATION_MINUTES * 60) // INTERVAL_SECONDS

print("=" * 60)
print("TIME-LAPSE CAPTURE")
print("=" * 60)
print(f"Interval: {INTERVAL_SECONDS} seconds")
print(f"Duration: {DURATION_MINUTES} minutes")
print(f"Total captures: {num_captures}")
print("=" * 60)
print()

# Initialize camera
ret = PxLApi.initialize(0)
hCamera = ret[1]

# Get camera info
ret = PxLApi.getCameraInfo(hCamera)
info = ret[1]
print(f"Camera: {info.ModelName.decode('utf-8')}")
print(f"Serial: {info.SerialNumber.decode('utf-8')}")
print()

# Setup buffer
ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.ROI)
width = int(ret[2][PxLApi.RoiParams.WIDTH])
height = int(ret[2][PxLApi.RoiParams.HEIGHT])
ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.PIXEL_FORMAT)
pixel_format = int(ret[2][0])
buffer_size = width * height * PxLApi.getBytesPerPixel(pixel_format)
rawImage = create_string_buffer(buffer_size)

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Start streaming
PxLApi.setStreamState(hCamera, PxLApi.StreamState.START)

# Capture loop
start_time = time.time()

try:
    for i in range(num_captures):
        # Capture frame
        ret = PxLApi.getNextFrame(hCamera, rawImage)
        if PxLApi.apiSuccess(ret[0]):
            frameDesc = ret[1]

            # Format as JPEG
            ret = PxLApi.formatImage(rawImage, frameDesc, PxLApi.ImageFormat.JPEG)

            # Save with sequence number and timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{OUTPUT_DIR}/frame_{i:04d}_{timestamp}.jpg"

            with open(filename, "wb") as f:
                f.write(ret[1])

            elapsed = time.time() - start_time
            remaining = (num_captures - i - 1) * INTERVAL_SECONDS

            print(f"[{i+1}/{num_captures}] {filename} | "
                  f"Elapsed: {elapsed:.0f}s | Remaining: {remaining:.0f}s")
        else:
            print(f"Error capturing frame {i+1}")

        # Wait for next interval (but break if this is the last frame)
        if i < num_captures - 1:
            time.sleep(INTERVAL_SECONDS)

except KeyboardInterrupt:
    print("\n\nTime-lapse interrupted by user")

finally:
    # Cleanup
    PxLApi.setStreamState(hCamera, PxLApi.StreamState.STOP)
    PxLApi.uninitialize(hCamera)

    total_time = time.time() - start_time
    print(f"\nTime-lapse complete!")
    print(f"Total time: {total_time:.1f} seconds")
    print(f"Images saved in: {OUTPUT_DIR}/")
```

---

## Example 5: Auto vs Manual Exposure

**File: `auto_exposure_test.py`**

```python
"""
Compare auto exposure vs manual exposure
"""
from pixelinkWrapper import PxLApi
from ctypes import create_string_buffer

def capture_and_save(hCamera, rawImage, filename, label):
    """Helper to capture and save an image"""
    ret = PxLApi.getNextFrame(hCamera, rawImage)
    if PxLApi.apiSuccess(ret[0]):
        frameDesc = ret[1]
        ret = PxLApi.formatImage(rawImage, frameDesc, PxLApi.ImageFormat.JPEG)
        with open(filename, "wb") as f:
            f.write(ret[1])
        print(f"✓ {label}: {filename}")
        return True
    return False

# Initialize
ret = PxLApi.initialize(0)
hCamera = ret[1]

# Setup buffer
ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.ROI)
width = int(ret[2][PxLApi.RoiParams.WIDTH])
height = int(ret[2][PxLApi.RoiParams.HEIGHT])
ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.PIXEL_FORMAT)
pixel_format = int(ret[2][0])
buffer_size = width * height * PxLApi.getBytesPerPixel(pixel_format)
rawImage = create_string_buffer(buffer_size)

# Start streaming
PxLApi.setStreamState(hCamera, PxLApi.StreamState.START)

print("Capturing with AUTO exposure...")

# Set auto exposure
PxLApi.setFeature(hCamera, PxLApi.FeatureId.EXPOSURE,
                  PxLApi.FeatureFlags.AUTO, [])

# Wait a moment for auto exposure to stabilize
import time
time.sleep(1)

# Capture with auto
capture_and_save(hCamera, rawImage, "auto_exposure.jpg", "Auto Exposure")

# Get the auto exposure value
ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.EXPOSURE)
auto_exposure_value = ret[2][0]
print(f"  Auto exposure value: {auto_exposure_value:.2f}ms")

print("\nCapturing with MANUAL exposure...")

# Try different manual exposures
manual_exposures = [
    auto_exposure_value * 0.5,  # Half
    auto_exposure_value,         # Same as auto
    auto_exposure_value * 2.0    # Double
]

for i, exp in enumerate(manual_exposures):
    PxLApi.setFeature(hCamera, PxLApi.FeatureId.EXPOSURE,
                      PxLApi.FeatureFlags.MANUAL, [exp])

    filename = f"manual_exposure_{i+1}_{exp:.1f}ms.jpg"
    capture_and_save(hCamera, rawImage, filename, f"Manual {exp:.1f}ms")

# Cleanup
PxLApi.setStreamState(hCamera, PxLApi.StreamState.STOP)
PxLApi.uninitialize(hCamera)

print("\nDone! Compare the images to see the difference.")
```

---

## Example 6: Continuous Live Preview (Console)

**File: `live_preview_console.py`**

```python
"""
Display live frame information in console
"""
from pixelinkWrapper import PxLApi
from ctypes import create_string_buffer
import time

# Initialize
ret = PxLApi.initialize(0)
hCamera = ret[1]

# Get camera info
ret = PxLApi.getCameraInfo(hCamera)
info = ret[1]

print("=" * 60)
print(f"LIVE PREVIEW - {info.ModelName.decode('utf-8')}")
print("=" * 60)
print("Press Ctrl+C to stop")
print()

# Setup buffer
ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.ROI)
width = int(ret[2][PxLApi.RoiParams.WIDTH])
height = int(ret[2][PxLApi.RoiParams.HEIGHT])
ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.PIXEL_FORMAT)
pixel_format = int(ret[2][0])
buffer_size = width * height * PxLApi.getBytesPerPixel(pixel_format)
rawImage = create_string_buffer(buffer_size)

# Start streaming
PxLApi.setStreamState(hCamera, PxLApi.StreamState.START)

frame_count = 0
start_time = time.time()
last_frame_time = start_time

try:
    while True:
        ret = PxLApi.getNextFrame(hCamera, rawImage)
        if PxLApi.apiSuccess(ret[0]):
            frameDesc = ret[1]

            frame_count += 1
            current_time = time.time()

            # Calculate FPS
            frame_time = current_time - last_frame_time
            fps = 1.0 / frame_time if frame_time > 0 else 0

            # Calculate average FPS
            total_time = current_time - start_time
            avg_fps = frame_count / total_time if total_time > 0 else 0

            # Display info
            print(f"Frame #{frame_count:6d} | "
                  f"FPS: {fps:5.1f} | "
                  f"Avg FPS: {avg_fps:5.1f} | "
                  f"Frame Time: {frameDesc.fFrameTime:10.3f}s",
                  end='\r')

            last_frame_time = current_time

        time.sleep(0.01)  # Small delay

except KeyboardInterrupt:
    print("\n\nStopping preview...")

finally:
    PxLApi.setStreamState(hCamera, PxLApi.StreamState.STOP)
    PxLApi.uninitialize(hCamera)

    total_time = time.time() - start_time
    print(f"\nTotal frames: {frame_count}")
    print(f"Total time: {total_time:.1f}s")
    print(f"Average FPS: {frame_count/total_time:.1f}")
```

---

## Example 7: Save Camera Settings

**File: `save_load_settings.py`**

```python
"""
Save and load camera settings to/from file
"""
from pixelinkWrapper import PxLApi

SETTINGS_FILE = "my_camera_settings.pfs"

# Initialize
ret = PxLApi.initialize(0)
hCamera = ret[1]

print("Current Camera Settings")
print("=" * 60)

# Display current settings
ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.EXPOSURE)
exposure = ret[2][0]
print(f"Exposure: {exposure:.2f}ms")

ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.GAIN)
gain = ret[2][0]
print(f"Gain: {gain:.2f}dB")

ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.GAMMA)
if PxLApi.apiSuccess(ret[0]):
    gamma = ret[2][0]
    print(f"Gamma: {gamma:.2f}")

# Save settings
print(f"\nSaving settings to: {SETTINGS_FILE}")
ret = PxLApi.saveSettings(hCamera, SETTINGS_FILE)
if PxLApi.apiSuccess(ret[0]):
    print("✓ Settings saved successfully")
else:
    print("✗ Failed to save settings")

# Modify some settings
print("\nModifying settings...")
PxLApi.setFeature(hCamera, PxLApi.FeatureId.EXPOSURE,
                  PxLApi.FeatureFlags.MANUAL, [100.0])
PxLApi.setFeature(hCamera, PxLApi.FeatureId.GAIN,
                  PxLApi.FeatureFlags.MANUAL, [10.0])

ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.EXPOSURE)
print(f"New Exposure: {ret[2][0]:.2f}ms")
ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.GAIN)
print(f"New Gain: {ret[2][0]:.2f}dB")

# Load settings back
print(f"\nLoading settings from: {SETTINGS_FILE}")
ret = PxLApi.loadSettings(hCamera, SETTINGS_FILE)
if PxLApi.apiSuccess(ret[0]):
    print("✓ Settings loaded successfully")
else:
    print("✗ Failed to load settings")

# Verify settings restored
ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.EXPOSURE)
print(f"Restored Exposure: {ret[2][0]:.2f}ms")
ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.GAIN)
print(f"Restored Gain: {ret[2][0]:.2f}dB")

# Cleanup
PxLApi.uninitialize(hCamera)
```

---

## Example 8: Multiple Image Formats

**File: `capture_all_formats.py`**

```python
"""
Capture images in all available formats
"""
from pixelinkWrapper import PxLApi
from ctypes import create_string_buffer
import os

# Initialize
ret = PxLApi.initialize(0)
hCamera = ret[1]

# Setup buffer
ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.ROI)
width = int(ret[2][PxLApi.RoiParams.WIDTH])
height = int(ret[2][PxLApi.RoiParams.HEIGHT])
ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.PIXEL_FORMAT)
pixel_format = int(ret[2][0])
buffer_size = width * height * PxLApi.getBytesPerPixel(pixel_format)
rawImage = create_string_buffer(buffer_size)

# Create output directory
os.makedirs("all_formats", exist_ok=True)

# Start streaming
PxLApi.setStreamState(hCamera, PxLApi.StreamState.START)

# Capture one frame
ret = PxLApi.getNextFrame(hCamera, rawImage)
frameDesc = ret[1]

# Stop streaming
PxLApi.setStreamState(hCamera, PxLApi.StreamState.STOP)

# Define all formats to test
formats = [
    (PxLApi.ImageFormat.JPEG, "image.jpg", "JPEG"),
    (PxLApi.ImageFormat.BMP, "image.bmp", "BMP"),
    (PxLApi.ImageFormat.TIFF, "image.tiff", "TIFF"),
    (PxLApi.ImageFormat.PNG, "image.png", "PNG"),
    (PxLApi.ImageFormat.PSD, "image.psd", "PSD"),
    (PxLApi.ImageFormat.RAW_BGR24, "image_bgr24.bin", "RAW BGR24"),
    (PxLApi.ImageFormat.RAW_RGB48, "image_rgb48.bin", "RAW RGB48"),
]

print("Saving captured frame in multiple formats...")
print("=" * 60)

for img_format, filename, description in formats:
    filepath = os.path.join("all_formats", filename)

    ret = PxLApi.formatImage(rawImage, frameDesc, img_format)
    if PxLApi.apiSuccess(ret[0]):
        formattedImage = ret[1]

        with open(filepath, "wb") as f:
            f.write(formattedImage)

        size_kb = len(formattedImage) / 1024
        print(f"✓ {description:15s} -> {filename:25s} ({size_kb:8.1f} KB)")
    else:
        print(f"✗ {description:15s} -> Failed (error code: {ret[0]})")

# Cleanup
PxLApi.uninitialize(hCamera)

print("\nAll images saved in 'all_formats' folder")
```

---

## How to Use These Examples

1. **Copy the code** you want to use
2. **Save it** as a `.py` file in your project directory
3. **Run it** with: `python filename.py`
4. **Modify** the parameters as needed for your use case

## Quick Selection Guide

- **Just want a photo?** → Use Example 1
- **Need to find cameras?** → Use Example 2
- **Testing lighting?** → Use Example 3
- **Making a time-lapse?** → Use Example 4
- **Auto vs manual?** → Use Example 5
- **Check frame rate?** → Use Example 6
- **Save config?** → Use Example 7
- **Compare formats?** → Use Example 8

---

**Pro Tip:** Start with Example 1 to make sure everything works, then experiment with the others!
