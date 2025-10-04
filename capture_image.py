"""
Pixelink Camera Image Capture Script
This script initializes a Pixelink camera and captures an image

Based on the official Pixelink SDK samples
"""

import sys
import os
from datetime import datetime
from ctypes import create_string_buffer

# Fix for wmic error in pixelinkWrapper on newer Windows versions
try:
    from pixelinkWrapper import PxLApi
except Exception as e:
    print(f"Error importing pixelinkWrapper: {e}")
    print("\nTrying alternative import method...")
    try:
        # Try to import with subprocess workaround
        import subprocess
        original_check_output = subprocess.check_output
        
        def patched_check_output(*args, **kwargs):
            try:
                return original_check_output(*args, **kwargs)
            except FileNotFoundError:
                # Return a dummy version string if wmic fails
                return b"10.0.0"
        
        subprocess.check_output = patched_check_output
        from pixelinkWrapper import PxLApi
        subprocess.check_output = original_check_output
    except Exception as e2:
        print(f"Alternative import also failed: {e2}")
        print("\nPlease ensure the Pixelink SDK is properly installed.")
        sys.exit(1)

SUCCESS = 0
FAILURE = 1


def determine_raw_image_size(hCamera):
    """
    Query the camera for region of interest (ROI), decimation, and pixel format
    Using this information, we can calculate the size of a raw image
    
    Returns 0 on failure
    """
    assert 0 != hCamera

    # Get region of interest (ROI)
    ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.ROI)
    params = ret[2]
    roiWidth = params[PxLApi.RoiParams.WIDTH]
    roiHeight = params[PxLApi.RoiParams.HEIGHT]

    # Query pixel addressing
    # assume no pixel addressing (in case it is not supported)
    pixelAddressingValueX = 1
    pixelAddressingValueY = 1

    ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.PIXEL_ADDRESSING)
    if PxLApi.apiSuccess(ret[0]):
        params = ret[2]
        if PxLApi.PixelAddressingParams.NUM_PARAMS == len(params):
            # Camera supports symmetric and asymmetric pixel addressing
            pixelAddressingValueX = params[PxLApi.PixelAddressingParams.X_VALUE]
            pixelAddressingValueY = params[PxLApi.PixelAddressingParams.Y_VALUE]
        else:
            # Camera supports only symmetric pixel addressing
            pixelAddressingValueX = params[PxLApi.PixelAddressingParams.VALUE]
            pixelAddressingValueY = params[PxLApi.PixelAddressingParams.VALUE]

    # We can calculate the number of pixels now.
    numPixels = (roiWidth / pixelAddressingValueX) * (roiHeight / pixelAddressingValueY)
    ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.PIXEL_FORMAT)

    # Knowing pixel format means we can determine how many bytes per pixel.
    params = ret[2]
    pixelFormat = int(params[0])

    # And now the size of the frame
    pixelSize = PxLApi.getBytesPerPixel(pixelFormat)

    return int(numPixels * pixelSize)


def get_raw_image(hCamera, rawImage):
    """
    Capture an image from the camera.
    
    NOTE: PxLApi.getNextFrame is a blocking call. 
    i.e. PxLApi.getNextFrame won't return until an image is captured.
    So, if you're using hardware triggering, it won't return until the camera is triggered.
    
    Returns a return code with success and frame descriptor information or API error
    """
    assert 0 != hCamera
    assert 0 != len(rawImage)

    MAX_NUM_TRIES = 4

    # Put camera into streaming state so we can capture an image
    ret = PxLApi.setStreamState(hCamera, PxLApi.StreamState.START)
    if not PxLApi.apiSuccess(ret[0]):
        return FAILURE
      
    # Get an image
    # NOTE: PxLApi.getNextFrame can return ApiCameraTimeoutError on occasion.
    # How you handle this depends on your situation and how you use your camera. 
    # For this sample app, we'll just retry a few times.
    ret = (PxLApi.ReturnCode.ApiUnknownError,)

    for i in range(MAX_NUM_TRIES):
        ret = PxLApi.getNextFrame(hCamera, rawImage)
        if PxLApi.apiSuccess(ret[0]):
            break

    # Done capturing, so no longer need the camera streaming images.
    # Note: If ret is used for this call, it will lose frame descriptor information.
    PxLApi.setStreamState(hCamera, PxLApi.StreamState.STOP)

    return ret


def save_image_to_file(fileName, formattedImage):
    """
    Save the encoded image buffer to a file
    This overwrites any existing file
    
    Returns SUCCESS or FAILURE
    """
    assert fileName
    assert 0 != len(formattedImage)

    # Open a file for binary write
    file = open(fileName, "wb")
    if None == file:
        return FAILURE
    numBytesWritten = file.write(formattedImage)
    file.close()

    if numBytesWritten == len(formattedImage):
        return SUCCESS

    return FAILURE


def get_snapshot(hCamera, imageFormat, fileName):
    """
    Get a snapshot from the camera, and save to a file.
    """
    assert 0 != hCamera
    assert fileName
    
    # Determine the size of buffer we'll need to hold an image from the camera
    rawImageSize = determine_raw_image_size(hCamera)
    if 0 == rawImageSize:
        return FAILURE

    # Create a buffer to hold the raw image
    rawImage = create_string_buffer(rawImageSize)

    if 0 != len(rawImage):
        # Capture a raw image. The raw image buffer will contain image data on success. 
        ret = get_raw_image(hCamera, rawImage)
        if PxLApi.apiSuccess(ret[0]):
            frameDescriptor = ret[1]
            
            assert 0 != len(rawImage)
            assert frameDescriptor
            
            # Encode the raw image into something displayable
            ret = PxLApi.formatImage(rawImage, frameDescriptor, imageFormat)
            if SUCCESS == ret[0]:
                formattedImage = ret[1]
                # Save formatted image into a file
                if save_image_to_file(fileName, formattedImage) == SUCCESS:
                    return SUCCESS
            
    return FAILURE

def capture_image():
    """
    Capture an image from a Pixelink camera and save it to disk
    """
    # Initialize the camera (connect to the first available camera)
    print("Initializing Pixelink camera...")
    ret = PxLApi.initialize(0)
    
    if not PxLApi.apiSuccess(ret[0]):
        print(f"ERROR: Could not initialize camera. Error code: {ret[0]}")
        return False
    
    hCamera = ret[1]
    print(f"Camera initialized successfully. Handle: {hCamera}")
    
    # Get camera information
    camera_info = PxLApi.getCameraInfo(hCamera)
    if PxLApi.apiSuccess(camera_info[0]):
        model_name = camera_info[1].ModelName
        serial_num = camera_info[1].SerialNumber
        # Handle both string and bytes
        if isinstance(model_name, bytes):
            model_name = model_name.decode('utf-8')
        if isinstance(serial_num, bytes):
            serial_num = serial_num.decode('utf-8')
        print(f"Camera Model: {model_name}")
        print(f"Serial Number: {serial_num}")
    
    # Create output directory if it doesn't exist
    output_dir = "captured_images"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Capture multiple formats
    success = True
    
    # JPEG
    filename_jpg = os.path.join(output_dir, f"pixelink_capture_{timestamp}.jpg")
    print(f"\nCapturing JPEG image...")
    retVal = get_snapshot(hCamera, PxLApi.ImageFormat.JPEG, filename_jpg)
    if SUCCESS == retVal:
        file_size = os.path.getsize(filename_jpg)
        print(f"✓ Saved JPEG: {filename_jpg} ({file_size:,} bytes)")
    else:
        print(f"✗ Failed to capture JPEG")
        success = False
    
    # BMP
    filename_bmp = os.path.join(output_dir, f"pixelink_capture_{timestamp}.bmp")
    print(f"\nCapturing BMP image...")
    retVal = get_snapshot(hCamera, PxLApi.ImageFormat.BMP, filename_bmp)
    if SUCCESS == retVal:
        file_size = os.path.getsize(filename_bmp)
        print(f"✓ Saved BMP: {filename_bmp} ({file_size:,} bytes)")
    else:
        print(f"✗ Failed to capture BMP")
        success = False
    
    # Tell the camera we're done with it
    print("\nUninitializing camera...")
    PxLApi.uninitialize(hCamera)
    
    return success


def list_cameras():
    """
    List all available Pixelink cameras
    """
    try:
        print("Searching for Pixelink cameras...")
        ret = PxLApi.getNumberCameras()
        
        if PxLApi.apiSuccess(ret[0]):
            num_cameras = ret[1]
            # Handle case where num_cameras might be a list
            if isinstance(num_cameras, list):
                num_cameras = len(num_cameras)
                print(f"Found {num_cameras} camera(s)")
            else:
                print(f"Found {num_cameras} camera(s)")
            
            if num_cameras > 0:
                # Get camera IDs
                try:
                    ret = PxLApi.getCameraIdInformation()
                    if PxLApi.apiSuccess(ret[0]):
                        camera_ids = ret[1]
                        if isinstance(camera_ids, list):
                            for i, cam_id in enumerate(camera_ids):
                                try:
                                    serial = getattr(cam_id, 'CameraSerialNum', 'Unknown')
                                    print(f"  Camera {i}: Serial Number: {serial}")
                                except:
                                    print(f"  Camera {i}: Info available")
                        else:
                            print(f"  Camera 0: Serial Number: {camera_ids.CameraSerialNum}")
                except Exception as e:
                    print(f"  Could not get detailed camera info: {e}")
        else:
            print(f"Error getting camera count. Error code: {ret[0]}")
            
    except Exception as e:
        print(f"An error occurred while listing cameras: {str(e)}")


if __name__ == "__main__":
    print("=" * 60)
    print("Pixelink Camera Image Capture")
    print("=" * 60)
    print()
    
    # List available cameras
    list_cameras()
    print()
    
    # Capture an image
    success = capture_image()
    
    if success:
        print("\nImage capture completed successfully!")
    else:
        print("\nImage capture failed. Please check the error messages above.")
