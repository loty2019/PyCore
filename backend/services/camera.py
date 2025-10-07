"""
Camera control service using PixelLink SDK
"""
import sys
import os
from typing import Optional, Tuple
from datetime import datetime
from backend.core.logging import logger

# Add PixelLink wrapper to path
pixelink_path = os.path.join(os.getcwd(), "HELP", "pixelinkPythonWrapper-master")
if pixelink_path not in sys.path:
    sys.path.insert(0, pixelink_path)

try:
    from pixelinkWrapper import PxLApi
    from ctypes import create_string_buffer
    PIXELINK_AVAILABLE = True
except ImportError as e:
    logger.warning(f"PixelLink SDK not available: {e}. Using mock camera.")
    PIXELINK_AVAILABLE = False


class CameraService:
    """Service for controlling the microscope camera"""

    def __init__(self):
        self.camera_handle = None
        self.is_initialized = False
        self.current_exposure = 100  # ms
        self.current_gain = 1.0
        self.resolution = {"width": 1920, "height": 1080}

    def initialize(self) -> bool:
        """Initialize camera connection"""
        if not PIXELINK_AVAILABLE:
            logger.info("Using mock camera (PixelLink SDK not available)")
            self.is_initialized = True
            return True

        try:
            ret = PxLApi.initialize(0)
            if PxLApi.apiSuccess(ret[0]):
                self.camera_handle = ret[1]
                self.is_initialized = True
                logger.info(f"Camera initialized successfully. Handle: {self.camera_handle}")
                return True
            else:
                logger.error(f"Failed to initialize camera: {ret[0]}")
                return False
        except Exception as e:
            logger.error(f"Error initializing camera: {e}")
            return False

    def uninitialize(self):
        """Close camera connection"""
        if self.camera_handle and PIXELINK_AVAILABLE:
            try:
                PxLApi.uninitialize(self.camera_handle)
                logger.info("Camera uninitialized")
            except Exception as e:
                logger.error(f"Error uninitializing camera: {e}")
        self.is_initialized = False
        self.camera_handle = None

    def set_exposure(self, exposure_ms: int) -> bool:
        """Set camera exposure time"""
        if not self.is_initialized:
            logger.error("Camera not initialized")
            return False

        if not PIXELINK_AVAILABLE:
            self.current_exposure = exposure_ms
            logger.info(f"Mock camera: Set exposure to {exposure_ms}ms")
            return True

        try:
            # Set exposure using PixelLink API
            ret = PxLApi.setFeature(self.camera_handle, PxLApi.FeatureId.EXPOSURE,
                                    PxLApi.FeatureFlags.MANUAL, [exposure_ms / 1000.0])
            if PxLApi.apiSuccess(ret[0]):
                self.current_exposure = exposure_ms
                logger.info(f"Exposure set to {exposure_ms}ms")
                return True
            else:
                logger.error(f"Failed to set exposure: {ret[0]}")
                return False
        except Exception as e:
            logger.error(f"Error setting exposure: {e}")
            return False

    def set_gain(self, gain: float) -> bool:
        """Set camera gain"""
        if not self.is_initialized:
            logger.error("Camera not initialized")
            return False

        if not PIXELINK_AVAILABLE:
            self.current_gain = gain
            logger.info(f"Mock camera: Set gain to {gain}")
            return True

        try:
            # Set gain using PixelLink API
            ret = PxLApi.setFeature(self.camera_handle, PxLApi.FeatureId.GAIN,
                                    PxLApi.FeatureFlags.MANUAL, [gain])
            if PxLApi.apiSuccess(ret[0]):
                self.current_gain = gain
                logger.info(f"Gain set to {gain}")
                return True
            else:
                logger.error(f"Failed to set gain: {ret[0]}")
                return False
        except Exception as e:
            logger.error(f"Error setting gain: {e}")
            return False

    def capture_image(self, filename: str) -> Tuple[bool, Optional[dict]]:
        """
        Capture an image and save to file.

        Returns:
            (success, image_info_dict)
        """
        if not self.is_initialized:
            logger.error("Camera not initialized")
            return False, None

        # Create images directory if it doesn't exist
        os.makedirs("images", exist_ok=True)
        filepath = os.path.join("images", filename)

        if not PIXELINK_AVAILABLE:
            # Mock capture - create a simple test file
            try:
                with open(filepath, 'w') as f:
                    f.write("Mock image data")
                logger.info(f"Mock camera: Captured image to {filepath}")
                return True, {
                    "filename": filepath,
                    "width": self.resolution["width"],
                    "height": self.resolution["height"],
                    "file_size": 1024,
                    "exposure": self.current_exposure,
                    "gain": self.current_gain
                }
            except Exception as e:
                logger.error(f"Error creating mock image: {e}")
                return False, None

        try:
            # Capture using PixelLink API
            raw_image_size = self._determine_raw_image_size()
            if raw_image_size == 0:
                logger.error("Failed to determine image size")
                return False, None

            raw_image = create_string_buffer(raw_image_size)

            # Start streaming
            ret = PxLApi.setStreamState(self.camera_handle, PxLApi.StreamState.START)
            if not PxLApi.apiSuccess(ret[0]):
                logger.error("Failed to start streaming")
                return False, None

            # Capture frame
            ret = PxLApi.getNextFrame(self.camera_handle, raw_image)
            if PxLApi.apiSuccess(ret[0]):
                frame_descriptor = ret[1]

                # Stop streaming
                PxLApi.setStreamState(self.camera_handle, PxLApi.StreamState.STOP)

                # Format image as JPEG
                ret = PxLApi.formatImage(raw_image, frame_descriptor, PxLApi.ImageFormat.JPEG)
                if ret[0] == 0:  # SUCCESS
                    formatted_image = ret[1]

                    # Save to file
                    with open(filepath, "wb") as f:
                        f.write(formatted_image)

                    logger.info(f"Image captured and saved to {filepath}")

                    return True, {
                        "filename": filepath,
                        "width": int(frame_descriptor.uiWidth),
                        "height": int(frame_descriptor.uiHeight),
                        "file_size": os.path.getsize(filepath),
                        "exposure": self.current_exposure,
                        "gain": self.current_gain
                    }
                else:
                    logger.error("Failed to format image")
                    return False, None
            else:
                logger.error(f"Failed to capture frame: {ret[0]}")
                PxLApi.setStreamState(self.camera_handle, PxLApi.StreamState.STOP)
                return False, None

        except Exception as e:
            logger.error(f"Error capturing image: {e}")
            return False, None

    def _determine_raw_image_size(self) -> int:
        """Determine the size of raw image buffer needed"""
        if not PIXELINK_AVAILABLE or not self.camera_handle:
            return 0

        try:
            # Get ROI
            ret = PxLApi.getFeature(self.camera_handle, PxLApi.FeatureId.ROI)
            params = ret[2]
            roi_width = params[PxLApi.RoiParams.WIDTH]
            roi_height = params[PxLApi.RoiParams.HEIGHT]

            # Get pixel addressing
            pixel_addressing_x = 1
            pixel_addressing_y = 1

            ret = PxLApi.getFeature(self.camera_handle, PxLApi.FeatureId.PIXEL_ADDRESSING)
            if PxLApi.apiSuccess(ret[0]):
                params = ret[2]
                if len(params) == PxLApi.PixelAddressingParams.NUM_PARAMS:
                    pixel_addressing_x = params[PxLApi.PixelAddressingParams.X_VALUE]
                    pixel_addressing_y = params[PxLApi.PixelAddressingParams.Y_VALUE]
                else:
                    pixel_addressing_x = params[PxLApi.PixelAddressingParams.VALUE]
                    pixel_addressing_y = params[PxLApi.PixelAddressingParams.VALUE]

            # Calculate number of pixels
            num_pixels = (roi_width / pixel_addressing_x) * (roi_height / pixel_addressing_y)

            # Get pixel format
            ret = PxLApi.getFeature(self.camera_handle, PxLApi.FeatureId.PIXEL_FORMAT)
            params = ret[2]
            pixel_format = int(params[0])

            # Get bytes per pixel
            pixel_size = PxLApi.getBytesPerPixel(pixel_format)

            return int(num_pixels * pixel_size)
        except Exception as e:
            logger.error(f"Error determining image size: {e}")
            return 0

    def get_settings(self) -> dict:
        """Get current camera settings"""
        return {
            "exposure": self.current_exposure,
            "gain": self.current_gain,
            "resolution": self.resolution,
            "available_resolutions": [
                {"width": 1920, "height": 1080},
                {"width": 1280, "height": 720}
            ]
        }


# Global camera service instance
camera_service = CameraService()
