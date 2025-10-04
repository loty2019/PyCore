# Pixelink Camera Quick Reference

A cheat sheet for common Pixelink camera operations.

## 🚀 Basic Operations

### Initialize Camera

```python
from pixelinkWrapper import PxLApi

ret = PxLApi.initialize(0)  # 0 = first camera
hCamera = ret[1]  # Camera handle
```

### Uninitialize Camera

```python
PxLApi.uninitialize(hCamera)
```

### Check API Success

```python
if PxLApi.apiSuccess(ret[0]):
    # Success!
    data = ret[1]
else:
    # Failed
    print(f"Error: {ret[0]}")
```

---

## 📸 Image Capture

### Quick Capture (Copy & Paste Ready)

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

# Create buffer and capture
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

---

## 🎛️ Camera Settings

### Exposure

```python
# Get exposure
ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.EXPOSURE)
current_exposure = ret[2][0]  # in milliseconds

# Set exposure (manual)
PxLApi.setFeature(hCamera, PxLApi.FeatureId.EXPOSURE,
                  PxLApi.FeatureFlags.MANUAL, [50.0])  # 50ms

# Auto exposure
PxLApi.setFeature(hCamera, PxLApi.FeatureId.EXPOSURE,
                  PxLApi.FeatureFlags.AUTO, [])
```

### Gain

```python
# Get gain
ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.GAIN)
current_gain = ret[2][0]  # in dB

# Set gain
PxLApi.setFeature(hCamera, PxLApi.FeatureId.GAIN,
                  PxLApi.FeatureFlags.MANUAL, [6.0])  # 6 dB

# Auto gain
PxLApi.setFeature(hCamera, PxLApi.FeatureId.GAIN,
                  PxLApi.FeatureFlags.AUTO, [])
```

### Region of Interest (ROI)

```python
# Get current ROI
ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.ROI)
x = ret[2][PxLApi.RoiParams.LEFT]
y = ret[2][PxLApi.RoiParams.TOP]
width = ret[2][PxLApi.RoiParams.WIDTH]
height = ret[2][PxLApi.RoiParams.HEIGHT]

# Set ROI
roi_params = [100, 100, 800, 600]  # x, y, width, height
PxLApi.setFeature(hCamera, PxLApi.FeatureId.ROI,
                  PxLApi.FeatureFlags.MANUAL, roi_params)
```

### White Balance

```python
# Auto white balance
PxLApi.setFeature(hCamera, PxLApi.FeatureId.WHITE_SHADING,
                  PxLApi.FeatureFlags.AUTO, [])

# Manual white balance
wb_params = [1.5, 1.0, 1.2]  # Red, Green, Blue gains
PxLApi.setFeature(hCamera, PxLApi.FeatureId.WHITE_SHADING,
                  PxLApi.FeatureFlags.MANUAL, wb_params)
```

### Gamma

```python
# Get gamma
ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.GAMMA)
current_gamma = ret[2][0]

# Set gamma
PxLApi.setFeature(hCamera, PxLApi.FeatureId.GAMMA,
                  PxLApi.FeatureFlags.MANUAL, [1.8])
```

---

## 🔄 Streaming

### Start/Stop Stream

```python
# Start
PxLApi.setStreamState(hCamera, PxLApi.StreamState.START)

# Pause
PxLApi.setStreamState(hCamera, PxLApi.StreamState.PAUSE)

# Stop
PxLApi.setStreamState(hCamera, PxLApi.StreamState.STOP)
```

### Check Stream State

```python
ret = PxLApi.getStreamState(hCamera)
if ret[1] == PxLApi.StreamState.START:
    print("Camera is streaming")
```

---

## 🖼️ Image Formats

| Format                         | Usage           |
| ------------------------------ | --------------- |
| `PxLApi.ImageFormat.JPEG`      | Compressed JPEG |
| `PxLApi.ImageFormat.BMP`       | Windows Bitmap  |
| `PxLApi.ImageFormat.TIFF`      | TIFF format     |
| `PxLApi.ImageFormat.PNG`       | PNG format      |
| `PxLApi.ImageFormat.PSD`       | Photoshop       |
| `PxLApi.ImageFormat.RAW_BGR24` | 24-bit BGR raw  |
| `PxLApi.ImageFormat.RAW_RGB48` | 48-bit RGB raw  |
| `PxLApi.ImageFormat.RAW_MONO8` | 8-bit mono raw  |

---

## ⚡ Triggering

### Software Trigger

```python
# Configure software trigger
trigger_params = [
    PxLApi.TriggerModes.MODE_0,
    PxLApi.TriggerTypes.SOFTWARE,
    PxLApi.Polarity.ACTIVE_HIGH,
    0,  # delay
    0   # parameter
]
PxLApi.setFeature(hCamera, PxLApi.FeatureId.TRIGGER,
                  PxLApi.FeatureFlags.MANUAL, trigger_params)

# Start stream
PxLApi.setStreamState(hCamera, PxLApi.StreamState.START)

# Send trigger
PxLApi.setFeature(hCamera, PxLApi.FeatureId.TRIGGER,
                  PxLApi.FeatureFlags.ONEPUSH, [])

# Get triggered frame
ret = PxLApi.getNextFrame(hCamera, rawImage)
```

### Hardware Trigger

```python
trigger_params = [
    PxLApi.TriggerModes.MODE_0,
    PxLApi.TriggerTypes.HARDWARE,
    PxLApi.Polarity.ACTIVE_HIGH,
    0,  # delay
    0   # parameter
]
PxLApi.setFeature(hCamera, PxLApi.FeatureId.TRIGGER,
                  PxLApi.FeatureFlags.MANUAL, trigger_params)
```

### Disable Trigger (Free Running)

```python
PxLApi.setFeature(hCamera, PxLApi.FeatureId.TRIGGER,
                  PxLApi.FeatureFlags.OFF, [])
```

---

## 📊 Camera Information

### Get Camera Info

```python
ret = PxLApi.getCameraInfo(hCamera)
info = ret[1]

print(f"Model: {info.ModelName.decode('utf-8')}")
print(f"Serial: {info.SerialNumber.decode('utf-8')}")
print(f"Firmware: {info.FirmwareVersion.decode('utf-8')}")
print(f"FPGA Version: {info.FPGAVersion.decode('utf-8')}")
print(f"XML Version: {info.XMLVersion.decode('utf-8')}")
```

### Get Frame Rate

```python
ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.ACTUAL_FRAME_RATE)
fps = ret[2][0]
print(f"Frame rate: {fps} FPS")
```

### Get Temperature

```python
ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.TEMPERATURE)
if PxLApi.apiSuccess(ret[0]):
    temp = ret[2][0]
    print(f"Camera temperature: {temp}°C")
```

---

## 💾 Settings Management

### Save Settings

```python
# Save to file
PxLApi.saveSettings(hCamera, "my_settings.pfs")

# Save to factory defaults channel
PxLApi.saveSettings(hCamera, PxLApi.Settings.SETTINGS_FACTORY)
```

### Load Settings

```python
# Load from file
PxLApi.loadSettings(hCamera, "my_settings.pfs")

# Load factory defaults
PxLApi.loadSettings(hCamera, PxLApi.Settings.SETTINGS_FACTORY)
```

---

## 🔍 Feature Queries

### Check if Feature is Supported

```python
ret = PxLApi.getCameraFeatures(hCamera, PxLApi.FeatureId.EXPOSURE)
if PxLApi.apiSuccess(ret[0]):
    print("Exposure is supported")
    features = ret[1]
    # features contains detailed info
```

### Get Feature Range

```python
ret = PxLApi.getCameraFeatures(hCamera, PxLApi.FeatureId.EXPOSURE)
if PxLApi.apiSuccess(ret[0]):
    features = ret[1]
    for param in features.Params:
        print(f"Min: {param.fMinValue}")
        print(f"Max: {param.fMaxValue}")
```

---

## 🐛 Error Handling

### Common Return Codes

```python
PxLApi.ReturnCode.ApiSuccess              # Success
PxLApi.ReturnCode.ApiInvalidHandleError   # Bad handle
PxLApi.ReturnCode.ApiInvalidParameterError # Bad param
PxLApi.ReturnCode.ApiNotSupportedError    # Not supported
PxLApi.ReturnCode.ApiCameraTimeoutError   # Timeout
PxLApi.ReturnCode.ApiBufferTooSmall       # Buffer too small
PxLApi.ReturnCode.ApiStreamStopped        # Stream not running
```

### Error Check Template

```python
ret = PxLApi.someFunction(hCamera, params)
if PxLApi.apiSuccess(ret[0]):
    # Success path
    result = ret[1]
    print(f"Success! Result: {result}")
else:
    # Error path
    error_code = ret[0]
    if error_code == PxLApi.ReturnCode.ApiInvalidHandleError:
        print("Invalid camera handle")
    elif error_code == PxLApi.ReturnCode.ApiCameraTimeoutError:
        print("Camera timeout - retry")
    else:
        print(f"Error code: {error_code}")
```

---

## 🔄 Continuous Capture Loop

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

## 📏 Helper Functions

### Get Bytes Per Pixel

```python
pixel_format = PxLApi.PixelFormat.MONO8
bytes_per_pixel = PxLApi.getBytesPerPixel(pixel_format)
```

### Calculate Image Size

```python
width = 1920
height = 1080
pixel_format = PxLApi.PixelFormat.MONO8

image_size = PxLApi.imageSize(width, height, pixel_format)
```

### Create Aligned Buffer

```python
# For decompressed frames (64-byte aligned)
buffer = PxLApi.createByteAlignedBuffer(buffer_size)
```

---

## 📋 Common Pixel Formats

| Format         | Description       | Bytes/Pixel |
| -------------- | ----------------- | ----------- |
| `MONO8`        | 8-bit grayscale   | 1           |
| `MONO16`       | 16-bit grayscale  | 2           |
| `BAYER8_GRBG`  | 8-bit Bayer GRBG  | 1           |
| `BAYER16_GRBG` | 16-bit Bayer GRBG | 2           |
| `RGB24`        | 24-bit RGB        | 3           |
| `RGB48`        | 48-bit RGB        | 6           |
| `YUV422`       | YUV 4:2:2         | 2           |

---

## 💡 Pro Tips

1. **Always check return codes** with `apiSuccess()`
2. **Start stream before** calling `getNextFrame()`
3. **Stop stream before** uninitializing
4. **Use retries** for timeout errors
5. **Calculate buffer size** properly to avoid crashes
6. **Save settings** to preserve configurations
7. **Use auto features** for quick setup
8. **Check feature support** before using

---

## 🎯 Performance Tips

### Optimize Frame Capture

```python
# Pre-allocate buffer once
buffer = create_string_buffer(buffer_size)

# Reuse buffer in loop
for i in range(100):
    ret = PxLApi.getNextFrame(hCamera, buffer)
    # Process frame...
```

### Reduce Overhead

```python
# Keep stream running for multiple captures
PxLApi.setStreamState(hCamera, PxLApi.StreamState.START)

for i in range(100):
    ret = PxLApi.getNextFrame(hCamera, rawImage)
    # Process...

PxLApi.setStreamState(hCamera, PxLApi.StreamState.STOP)
```

---

**Need more help?** Check the full README.md or official Pixelink SDK documentation!
