# PyCore - Pixelink Camera Python Development Guide

## Project Overview

This is a Python project for capturing images from Pixelink cameras (specifically B701 model) using the `pixelinkWrapper` library, a ctypes-based wrapper around the native Pixelink 4.0 API (C DLL/shared library). The project provides working examples and comprehensive documentation for camera control.

## Architecture & Key Patterns

### Core Workflow

All camera operations follow this sequence:

1. **Initialize** → `PxLApi.initialize(0)` returns `(return_code, camera_handle)`
2. **Calculate buffer size** → Query ROI, pixel format, and addressing to determine raw image size
3. **Allocate buffer** → `create_string_buffer(size)` - MUST use ctypes buffer for C API compatibility
4. **Stream control** → Start/stop streaming with `setStreamState()`
5. **Capture** → `getNextFrame()` is a **blocking call** - won't return until frame available
6. **Format** → Convert raw sensor data to standard formats (JPEG, BMP, etc.)
7. **Cleanup** → Always `setStreamState(STOP)` before `uninitialize()`

### Return Value Pattern

**Every** API call returns a tuple: `(return_code, data)`

```python
ret = PxLApi.someFunction(hCamera)
if PxLApi.apiSuccess(ret[0]):
    result = ret[1]  # Only access on success
```

Never skip error checking - camera operations can timeout or fail.

### Camera Handle is Sacred

The camera handle from `initialize()` must be passed to all subsequent operations. Loss of this handle means re-initialization. Always store: `hCamera = ret[1]`

### Feature API Pattern

All camera settings (exposure, gain, ROI, white balance) use the same interface:

```python
# Get feature
ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.EXPOSURE)
value = ret[2][0]  # Note: data is in ret[2], not ret[1]!

# Set feature
PxLApi.setFeature(hCamera, PxLApi.FeatureId.EXPOSURE,
                  PxLApi.FeatureFlags.MANUAL, [50.0])
```

## Critical Implementation Details

### Buffer Size Calculation

**Never hardcode buffer sizes**. Use the `determine_raw_image_size()` function pattern from `capture_image.py`:

- Query ROI dimensions
- Account for pixel addressing (binning/decimation)
- Multiply by bytes-per-pixel based on pixel format
- Formula: `(width/addressing_x) * (height/addressing_y) * bytes_per_pixel`

### Windows-Specific Workaround

The wrapper has a known issue with modern Windows (wmic deprecation). See `capture_image.py` lines 12-30 for the subprocess patching pattern. This is required for import success.

### Streaming State Management

Camera must be streaming to capture frames:

```python
PxLApi.setStreamState(hCamera, PxLApi.StreamState.START)
# ... capture operations ...
PxLApi.setStreamState(hCamera, PxLApi.StreamState.STOP)  # Always stop before uninit
```

### Retry Logic for Timeouts

`getNextFrame()` occasionally returns `ApiCameraTimeoutError`. Standard practice is 4 retry attempts (see `get_raw_image()` in `capture_image.py`).

## File Organization

- **`capture_image.py`** - Main working script, captures JPEG + BMP. Use as reference implementation.
- **`README.md`** - Comprehensive 400+ line tutorial covering all concepts
- **`QUICK_REFERENCE.md`** - Copy-paste code snippets for common operations
- **`EXAMPLES.md`** - 8 complete example scripts for specific use cases
- **`START_HERE.md`** - Navigation guide for the documentation
- **`pixelinkPythonWrapper-master/`** - Vendored wrapper library (do not modify)
- **`captured_images/`** - Default output directory

## When Writing New Scripts

1. **Start from `capture_image.py`** - It's the canonical reference with all patterns
2. **Import with error handling** - Use the subprocess workaround pattern
3. **Create buffer correctly** - Use `from ctypes import create_string_buffer`
4. **Check all return codes** - Use `PxLApi.apiSuccess(ret[0])` before accessing data
5. **Manage streaming state** - Start before capture, stop before uninitialize
6. **Use retry loops** - `getNextFrame()` can timeout, retry 3-4 times

## Common Operations Quick Reference

### Initialize and get camera info

```python
ret = PxLApi.initialize(0)
hCamera = ret[1]
info = PxLApi.getCameraInfo(hCamera)[1]
model = info.ModelName.decode('utf-8')  # Handle bytes/string conversion
```

### Set exposure/gain

```python
PxLApi.setFeature(hCamera, PxLApi.FeatureId.EXPOSURE,
                  PxLApi.FeatureFlags.MANUAL, [50.0])  # 50ms
PxLApi.setFeature(hCamera, PxLApi.FeatureId.GAIN,
                  PxLApi.FeatureFlags.MANUAL, [6.0])   # 6dB
```

### Auto vs Manual modes

```python
# Auto: pass empty list, use AUTO flag
PxLApi.setFeature(hCamera, PxLApi.FeatureId.EXPOSURE,
                  PxLApi.FeatureFlags.AUTO, [])

# Manual: pass parameters, use MANUAL flag
PxLApi.setFeature(hCamera, PxLApi.FeatureId.EXPOSURE,
                  PxLApi.FeatureFlags.MANUAL, [50.0])
```

### Save/Load settings

```python
PxLApi.saveSettings(hCamera, "config.pfs")  # Persist configuration
PxLApi.loadSettings(hCamera, "config.pfs")  # Restore configuration
```

## Testing Patterns

1. **Always test with camera connected** - These are hardware integration scripts
2. **Check Device Manager** - Camera must appear under "Imaging devices" (Windows)
3. **No unit tests** - This is a hardware interface project; use manual verification
4. **Verify image output** - Check `captured_images/` directory for results
5. **Frame rate verification** - Use Example 6 (live preview) to check performance

## Dependencies & Environment

### Required Software

- **Pixelink SDK** - Provides `PxLAPI40.dll` (Windows) or `libPxLApi.so` (Linux)
- **Python 3.8+** - Currently using Python 3.11
- **pixelinkWrapper** - Installed via pip: `pip install pixelinkWrapper`

### Target Hardware

- Primary: Pixelink B701 (Serial: 771001279)
- Support: All Pixelink 4.0 API compatible cameras (FireWire, USB, USB3, GigE)

## Error Handling Philosophy

**Always check return codes**. Common errors:

- `ApiInvalidHandleError` - Camera handle invalid/uninitialized
- `ApiCameraTimeoutError` - Frame capture timeout (retry)
- `ApiBufferTooSmall` - Incorrect buffer size calculation
- `ApiNotSupportedError` - Feature not available on this camera model

Pattern from codebase:

```python
ret = PxLApi.getNextFrame(hCamera, rawImage)
if not PxLApi.apiSuccess(ret[0]):
    # Handle error, possibly retry
    return FAILURE
frameDescriptor = ret[1]
```

## Documentation Structure

The documentation is designed for **learning by exploration**:

- **START_HERE.md** - Entry point, explains navigation
- **README.md** - Deep dive on concepts, explanations, troubleshooting
- **QUICK_REFERENCE.md** - Syntax lookup while coding
- **EXAMPLES.md** - Copy-paste solutions for specific tasks

When helping users, reference the appropriate doc based on their needs.

## Performance Considerations

- **Reuse buffers** - Allocate once, use in loop (see Example 6)
- **Keep stream running** - Don't stop/start between frames in continuous capture
- **Format selection** - JPEG (~80KB) vs BMP (~1.3MB) vs raw formats
- **Blocking calls** - `getNextFrame()` blocks thread; consider async patterns for UI apps

## Platform Notes

### macOS

This project is developed on macOS but **targets Windows/Linux** where Pixelink SDK is available. The code won't run on macOS (no Pixelink SDK for macOS). Development on macOS is for documentation/script writing only.

### Windows

Primary platform. Note the wmic deprecation workaround in imports. SDK installs to `C:\Program Files\Pixelink\`.

### Linux

Supported via `libPxLApi.so`. See `samples/Linux/` for platform-specific examples.

## What NOT to Do

- ❌ Don't modify files in `pixelinkPythonWrapper-master/` - it's vendored code
- ❌ Don't access `ret[1]` without checking `ret[0]` first
- ❌ Don't uninitialize camera while streaming
- ❌ Don't hardcode buffer sizes - calculate from camera features
- ❌ Don't assume frame capture succeeds - implement retry logic
- ❌ Don't forget `decode('utf-8')` on camera info strings (they're bytes)

## Key Files to Reference

When working on camera features, reference these patterns:

- **Exposure/Gain** → `EXAMPLES.md` Example 3 and 5
- **Time-lapse** → `EXAMPLES.md` Example 4
- **Multiple formats** → `EXAMPLES.md` Example 8
- **Buffer allocation** → `capture_image.py` `determine_raw_image_size()`
- **Error handling** → `capture_image.py` `get_raw_image()` retry loop
- **Feature API** → `QUICK_REFERENCE.md` Camera Settings section
