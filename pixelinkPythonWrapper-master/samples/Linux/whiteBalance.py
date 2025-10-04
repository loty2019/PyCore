"""
whiteBalance.py

Demonstrates how you can control the white balance on a (color) camera. Furthermore, it also can 
instruct the camera to perform automatic white balance.

Note 1: The sample application 'autoexposure.py' also shows how to control camera features that 
support continuous and one-time auto adjustments (such as white balance). However, that particular 
sample will also show how to cancel these auto adjustments.
"""

from pixelinkWrapper import*
from select import select
import threading
import time
import sys
import tty
import termios

# Color channel defines
redChannel = 0
greenChannel = 1
blueChannel = 2

"""
Returns true if the camera supports one-time auto adjustment of the specified feature, false otherwise
"""
def camera_supports_feature(hCamera, featureId):
    
    # Read the feature information
    ret = PxLApi.getCameraFeatures(hCamera, featureId)
    assert PxLApi.apiSuccess(ret[0]), "getCameraFeatures failed"
    
    cameraFeatures = ret[1]

    # Check the sanity of the return information
    assert 1 == cameraFeatures.uNumberOfFeatures, "Unexpected number of features" # We only asked about one feature...
    assert featureId == cameraFeatures.Features[0].uFeatureId, "Unexpected returned featureId" # ... and that feature is the one requested
    isSupported = ((cameraFeatures.Features[0].uFlags & PxLApi.FeatureFlags.PRESENCE) != 0)
    supportsOneTimeAuto = ((cameraFeatures.Features[0].uFlags & PxLApi.FeatureFlags.ONEPUSH) != 0)

    if(isSupported and supportsOneTimeAuto):
        # This app does not need/use these -- but yours might....
        global colorLimits
        redColorLimits = cameraFeatures.Features[0].Params[redChannel]
        greenColorLimits = cameraFeatures.Features[0].Params[greenChannel]
        blueColorLimits = cameraFeatures.Features[0].Params[blueChannel]
        colorLimits = [redColorLimits, greenColorLimits, blueColorLimits]

    return isSupported and supportsOneTimeAuto

"""
Changes the specified color channel - increasing or decreasing its value by a fixed amount.
"""
def change_channel(hCamera, color, increase):
    # Get the current color settings
    ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.WHITE_SHADING)
    assert PxLApi.apiSuccess(ret[0]), "getFeature for current color settings failed"
    
    flags = ret[1]
    cameraColors = ret[2]

    # adjust the specified color
    if increase:
        cameraColors[color] += cameraColors[color]*0.1
    else:
        cameraColors[color] -= cameraColors[color]*0.1

    # set the new color value, if it's in range
    if (cameraColors[color] > colorLimits[color].fMinValue) and \
       (cameraColors[color] < colorLimits[color].fMaxValue):
        ret = PxLApi.setFeature(hCamera, PxLApi.FeatureId.WHITE_SHADING, flags, cameraColors)
        if not PxLApi.apiSuccess(ret[0]):
            print("!! Attempt to set White Balance to R:%.2f, G:%.2f, B:%.2f returned %i!" % \
                 (cameraColors[0], cameraColors[1], cameraColors[2], ret[0]))

"""
Initiates a one-time auto adjustment of the white balance. Note that this routine does not wait for the operation to complete.
"""
def auto_white_balance(hCamera):

    cameraColors = [0, 0, 0] # Intialize to 0 (no color), but these values are ignored when initating auto adjustment.

    ret = PxLApi.setFeature(hCamera, PxLApi.FeatureId.WHITE_SHADING, PxLApi.FeatureFlags.ONEPUSH, cameraColors)
    if not(PxLApi.apiSuccess(ret[0])):
        print("!! Attempt to set Auto White Balance returned %i!" % ret[0])

"""
Prints out the current color channel values, or a message if the camera is currently adjusting them.
"""
def print_color_channels(hCamera):

    ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.WHITE_SHADING)
    assert PxLApi.apiSuccess(ret[0]), "%i" % ret[0]

    flags = ret[1]
    cameraColors = ret[2]

    # Is an auto adjustment still in progress?
    if flags & PxLApi.FeatureFlags.ONEPUSH:
        print("\r-- Camera is auto adjusting --           ", end="")
        return

    print("\rGains --> red:%.2f green:%.2f blue:%.2f  " % (cameraColors[0], cameraColors[1], cameraColors[2]), end="")


def main():

    global previewState # Controls preview thread
    done = False

    ret = PxLApi.initialize(0)
    if not(PxLApi.apiSuccess(ret[0])):
        print("Could not initialize the camera! rc = %i" % ret[0])
        return 1

    hCamera = ret[1]
    
    if not(camera_supports_feature(hCamera, PxLApi.FeatureId.WHITE_SHADING)):
        print("Camera does not support White Balance")
        PxLApi.uninitialize(hCamera)
        return 1

    print("Starting the stream for camera with handle: %i" % hCamera);
    print("    q   : to quit");
    print("    r/R : to decrease/increase red color channel by 10%");
    print("    g/G : to decrease/increase green color channel by 10%");
    print("    b/B : to decrease/increase blue color channel by 10%");
    print("    a   : Perform a one-time auto white balance on the camera\n");
    
    # Start the stream
    ret = PxLApi.setStreamState(hCamera, PxLApi.StreamState.START)
    if not(PxLApi.apiSuccess(ret[0])):
        print("Could not start the stream! rc = %i" % ret[0])
        PxLApi.uninitialize(hCamera)
        return 1

    # Start preview
    ret = PxLApi.setPreviewState(hCamera, PxLApi.PreviewState.START)
    if not(PxLApi.apiSuccess(ret[0])):
        print("Could not start the preview! rc = %i" % ret[0])
        PxLApi.setStreamState(hCamera, PxLApi.StreamState.STOP)
        PxLApi.uninitialize(hCamera)
        return 1
    
    setUnbufKb(True)
    while not(done):
        sys.stdin.flush()
        if kbhit():
            keyPressed = kbHit()
            if 'q' == keyPressed:
                print("")
                done = True
            elif 'r' == keyPressed:
                change_channel(hCamera, redChannel, False)
            elif 'R' == keyPressed:   
                change_channel(hCamera, redChannel, True)                
            elif 'g' == keyPressed:
                change_channel(hCamera, greenChannel, False)
            elif 'G' == keyPressed:
                change_channel(hCamera, greenChannel, True)
            elif 'b' == keyPressed:
                change_channel(hCamera, blueChannel, False)
            elif 'B' == keyPressed:
                change_channel(hCamera, blueChannel, True)
            elif 'a' == keyPressed:
                auto_white_balance(hCamera)
        sys.stdout.flush()
        if not(done):
            print_color_channels(hCamera)
            time.sleep(0.1) # 100 ms
    
    # Stop preview
    PxLApi.setPreviewState(hCamera, PxLApi.PreviewState.STOP)

    PxLApi.setStreamState(hCamera, PxLApi.StreamState.STOP)

    setUnbufKb(False)
    print("\r")
    PxLApi.uninitialize(hCamera)
    
    return 0

"""
Unbuffered non-blocking keyboard input on command line.
Keyboard input will be passed to the application without the user pressing
the enter key.
Note: IDLE does not support this functionality.
"""
# A couple of useful global variables
fd = sys.stdin.fileno()
original_term_settings = termios.tcgetattr(fd)

# Enable/disable unbuffered keyboard input
def setUnbufKb(enable):
    if enable:
        tty.setraw(sys.stdin.fileno())
    else:
        termios.tcsetattr(fd, termios.TCSADRAIN, original_term_settings)

# Unbuffered button hit check
def kbhit():
    rlist = select([sys.stdin], [], [], 0)
    if rlist[0] != []:
        return True
    return False

# Read hit button
def kbHit():
    return sys.stdin.read(1)


if __name__ == "__main__":
    # Global to remember the color gain limits. Set with a succesful call to camera_supports_feature
    colorLimits = None
    main()
