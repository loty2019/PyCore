"""
Test Autofocus Capabilities
This script checks if the camera supports autofocus and displays focus information
"""

import sys
import subprocess

# Fix for wmic error in pixelinkWrapper on newer Windows versions
try:
    from pixelinkWrapper import PxLApi
except Exception as e:
    print(f"Error importing pixelinkWrapper: {e}")
    print("\nTrying alternative import method...")
    try:
        # Try to import with subprocess workaround
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


def test_autofocus():
    """
    Test if the camera supports autofocus feature
    """
    print("=" * 60)
    print("Pixelink Camera Autofocus Test")
    print("=" * 60)
    print()
    
    # Initialize the camera
    print("Initializing camera...")
    ret = PxLApi.initialize(0)
    
    if not PxLApi.apiSuccess(ret[0]):
        print(f"ERROR: Could not initialize camera. Error code: {ret[0]}")
        return False
    
    hCamera = ret[1]
    print(f"✓ Camera initialized successfully. Handle: {hCamera}")
    
    # Get camera information
    camera_info = PxLApi.getCameraInfo(hCamera)
    if PxLApi.apiSuccess(camera_info[0]):
        model_name = camera_info[1].ModelName
        serial_num = camera_info[1].SerialNumber
        if isinstance(model_name, bytes):
            model_name = model_name.decode('utf-8')
        if isinstance(serial_num, bytes):
            serial_num = serial_num.decode('utf-8')
        print(f"Camera Model: {model_name}")
        print(f"Serial Number: {serial_num}")
    print()
    
    # Try to get the FOCUS feature
    print("Checking for FOCUS feature...")
    ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.FOCUS)
    
    if PxLApi.apiSuccess(ret[0]):
        print("✓ FOCUS feature is SUPPORTED!")
        print()
        
        # Get focus parameters
        flags = ret[1]
        params = ret[2]
        
        print("Focus Information:")
        print(f"  Flags: {flags}")
        print(f"  Current Focus Value: {params[0] if len(params) > 0 else 'N/A'}")
        
        # Check if auto focus is available
        print()
        print("Focus Capabilities:")
        
        # Check various flags
        if flags & PxLApi.FeatureFlags.PRESENCE:
            print("  ✓ Focus feature is present")
        
        if flags & PxLApi.FeatureFlags.MANUAL:
            print("  ✓ Manual focus control available")
        
        if flags & PxLApi.FeatureFlags.AUTO:
            print("  ✓ AUTO FOCUS is available!")
        else:
            print("  ✗ Auto focus is NOT available (manual focus only)")
        
        if flags & PxLApi.FeatureFlags.ONEPUSH:
            print("  ✓ One-push auto focus available")
        
        # Get feature parameters (min, max)
        ret_params = PxLApi.getCameraFeatures(hCamera, PxLApi.FeatureId.FOCUS)
        if PxLApi.apiSuccess(ret_params[0]):
            feature_info = ret_params[1]
            print()
            print("Focus Range:")
            print(f"  Minimum: {feature_info.Params[0].fMinValue}")
            print(f"  Maximum: {feature_info.Params[0].fMaxValue}")
        
    else:
        print("✗ FOCUS feature is NOT supported on this camera")
        print(f"   Error code: {ret[0]}")
        print()
        print("This camera does not have focus control capabilities.")
    
    print()
    
    # List all supported features
    print("=" * 60)
    print("All Supported Camera Features:")
    print("=" * 60)
    
    # Common features to check
    features_to_check = [
        ("BRIGHTNESS", PxLApi.FeatureId.BRIGHTNESS),
        ("EXPOSURE", PxLApi.FeatureId.EXPOSURE),
        ("GAIN", PxLApi.FeatureId.GAIN),
        ("GAMMA", PxLApi.FeatureId.GAMMA),
        ("SATURATION", PxLApi.FeatureId.SATURATION),
        ("SHARPNESS", PxLApi.FeatureId.SHARPNESS),
        ("WHITE_BALANCE", PxLApi.FeatureId.WHITE_BALANCE),
        ("ZOOM", PxLApi.FeatureId.ZOOM),
        ("FOCUS", PxLApi.FeatureId.FOCUS),
        ("IRIS", PxLApi.FeatureId.IRIS),
    ]
    
    for feature_name, feature_id in features_to_check:
        ret = PxLApi.getFeature(hCamera, feature_id)
        if PxLApi.apiSuccess(ret[0]):
            flags = ret[1]
            auto_available = " [AUTO]" if (flags & PxLApi.FeatureFlags.AUTO) else ""
            onepush_available = " [ONE-PUSH]" if (flags & PxLApi.FeatureFlags.ONEPUSH) else ""
            print(f"  ✓ {feature_name}{auto_available}{onepush_available}")
        else:
            print(f"  ✗ {feature_name}")
    
    # Cleanup
    print()
    print("Uninitializing camera...")
    PxLApi.uninitialize(hCamera)
    print("✓ Done!")
    
    return True


if __name__ == "__main__":
    test_autofocus()
