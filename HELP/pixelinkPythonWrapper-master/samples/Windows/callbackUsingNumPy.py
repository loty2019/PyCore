"""
callbackUsingNumPy.py

Demonstrates how to use callbacks with Callback.PREVIEW, using a NumPy image
The callback function will modify the preview buffer supplied by the API.
"""

from pixelinkWrapper import*
from ctypes import*
import ctypes.wintypes
import time
import threading
import numpy as np

def get_pixel_format_as_string(dataFormat):
    switcher = {
        PxLApi.PixelFormat.MONO8: "MONO8",
        PxLApi.PixelFormat.MONO16: "MONO16",
        PxLApi.PixelFormat.YUV422: "YUV422",
        PxLApi.PixelFormat.BAYER8_GRBG: "BAYER8_GRBG",
        PxLApi.PixelFormat.BAYER16_GRBG: "BAYER16_GRBG",
        PxLApi.PixelFormat.RGB24: "RGB24",
        PxLApi.PixelFormat.RGB48: "RGB48",
        PxLApi.PixelFormat.BAYER8_RGGB: "BAYER8_RGGB",
        PxLApi.PixelFormat.BAYER8_GBRG: "BAYER8_GBRG",
        PxLApi.PixelFormat.BAYER8_BGGR: "BAYER8_BGGR",
        PxLApi.PixelFormat.BAYER16_RGGB: "BAYER16_RGGB",
        PxLApi.PixelFormat.BAYER16_GBRG: "BAYER16_GBRG",
        PxLApi.PixelFormat.BAYER16_BGGR: "BAYER16_BGGR",
        PxLApi.PixelFormat.MONO12_PACKED: "MONO12_PACKED",
        PxLApi.PixelFormat.BAYER12_GRBG_PACKED: "BAYER12_GRBG_PACKED",
        PxLApi.PixelFormat.BAYER12_RGGB_PACKED: "BAYER12_RGGB_PACKED",
        PxLApi.PixelFormat.BAYER12_GBRG_PACKED: "BAYER12_GBRG_PACKED",
        PxLApi.PixelFormat.BAYER12_BGGR_PACKED: "BAYER12_BGGR_PACKED",
        PxLApi.PixelFormat.RGB24_NON_DIB: "RGB24_NON_DIB",
        PxLApi.PixelFormat.RGB48_DIB: "RGB48_DIB",
        PxLApi.PixelFormat.MONO12_PACKED_MSFIRST: "MONO12_PACKED_MSFIRST",
        PxLApi.PixelFormat.BAYER12_GRBG_PACKED_MSFIRST: "BAYER12_GRBG_PACKED_MSFIRST",
        PxLApi.PixelFormat.BAYER12_RGGB_PACKED_MSFIRST: "BAYER12_RGGB_PACKED_MSFIRST",
        PxLApi.PixelFormat.BAYER12_GBRG_PACKED_MSFIRST: "BAYER12_GBRG_PACKED_MSFIRST",
        PxLApi.PixelFormat.BAYER12_BGGR_PACKED_MSFIRST: "BAYER12_BGGR_PACKED_MSFIRST",
        PxLApi.PixelFormat.MONO10_PACKED_MSFIRST: "MONO10_PACKED_MSFIRST",
        PxLApi.PixelFormat.BAYER10_GRBG_PACKED_MSFIRST: "BAYER10_GRBG_PACKED_MSFIRST",
        PxLApi.PixelFormat.BAYER10_RGGB_PACKED_MSFIRST: "BAYER10_RGGB_PACKED_MSFIRST",
        PxLApi.PixelFormat.BAYER10_GBRG_PACKED_MSFIRST: "BAYER10_GBRG_PACKED_MSFIRST",
        PxLApi.PixelFormat.BAYER10_BGGR_PACKED_MSFIRST: "BAYER10_BGGR_PACKED_MSFIRST",
        PxLApi.PixelFormat.STOKES4_12: "STOKES4_12",
        PxLApi.PixelFormat.POLAR4_12: "POLAR4_12",
        PxLApi.PixelFormat.POLAR_RAW4_12: "POLAR_RAW4_12",
        PxLApi.PixelFormat.HSV4_12: "HSV4_12",
        PxLApi.PixelFormat.BGR24_NON_DIB: "BGR24_NON_DIB"        
        }
    return switcher.get(dataFormat, "Unknown data format")

"""
Creates a NumPy 2D array representation of a byte pointer used the the Pixelink API.
    frameData: Byte pointer to the image provided by the Pixelink API
    width:     Width of the image (in pixels)
    height:    Height of the image (in pixels)
    bytesPerPixel: the number of bytes per pixel
""" 
def numPy_image (frameData, width, height, bytesPerPixel):
    buffer_from_memory = pythonapi.PyMemoryView_FromMemory
    buffer_from_memory.restype = py_object
    pBuffer = buffer_from_memory(frameData, width * height * bytesPerPixel, 0x200) # 0x200 == writable
    return np.frombuffer(pBuffer, np.uint8).reshape(height, width * bytesPerPixel)
   
"""
Callback function called by the API just before an image is displayed in the preview window. 
    N.B. This is called by the API on a thread created in the API.
"""
@PxLApi._dataProcessFunction
def callback_format_preview(hCamera, frameData, dataFormat, frameDesc, userData):
    # Copy frame descriptor information
    frameDescriptor = frameDesc.contents
    # Find image dimensions
    width = int(frameDescriptor.Roi.fWidth / frameDescriptor.PixelAddressingValue.fHorizontal)
    height = int(frameDescriptor.Roi.fHeight / frameDescriptor.PixelAddressingValue.fVertical)
    bytesPerPixel = PxLApi.getBytesPerPixel(dataFormat)

    # Recast the returned image as a NumPy 2-Darray, that we can modify
    npFrame = numPy_image (frameData, width, height, bytesPerPixel)

    print("callback_format_image: hCamera = {0}, frameData = {1}".format(hex(hCamera),
                                                                         hex(id(frameData))))
    print("    dataFormat = {0} {1}, FrameDesc = {2}".format(dataFormat,
                                                             get_pixel_format_as_string(dataFormat),
                                                             hex(id(frameDesc))))
    print("    userData = {0}, threadId = {1}".format(hex(userData), hex(id(threading.current_thread()))))
    print("    imageData = {0} {1} {2} {3} {4} {5} {6} {7}\n".format(hex(frameData[0]), hex(frameData[1]), hex(frameData[2]),
                                                                   hex(frameData[3]), hex(frameData[4]), hex(frameData[5]),
                                                                   hex(frameData[6]), hex(frameData[7])))
    
    # Just to see the effect of the callback, increase intensity of the middle 20% of the pixels, to 100%
    startRow = int((height/5)*2)
    endRow = int((height/5)*3)
    startCol = int(((width*bytesPerPixel)/5)*2)
    endCol = int(((width*bytesPerPixel)/5)*3)

    npFrame[startRow:endRow,startCol:endCol] = 0xff

    return 0

"""
Runs preview for a number of seconds by polling the message pump on Windows.
"""
def run_preview_window_for(hCamera, seconds):

    previewTime = 0
    startPreview = time.time()

    # The preview window will go 'Not Responding' if we do not poll the message pump, and 
    # forward events onto it's handler on Windows.
    user32 = windll.user32
    msg = ctypes.wintypes.MSG()
    pMsg = ctypes.byref(msg)

    # Start preview
    ret = PxLApi.setPreviewState(hCamera, PxLApi.PreviewState.START)
    if(not(PxLApi.apiSuccess(ret[0]))):
        print("ERROR setting preview state function: {0}".format(ret[0]))
        return
    
    # Run preview for a number of seconds by polling the message pump
    while seconds > previewTime:
        if user32.PeekMessageW(pMsg, 0, 0, 0, 1) != 0:            
            user32.TranslateMessage(pMsg)
            user32.DispatchMessageW(pMsg)
        previewTime = time.time() - startPreview

    # Stop preview
    ret = PxLApi.setPreviewState(hCamera, PxLApi.PreviewState.STOP)


def do_callback_on_preview(hCamera):
    # Set the callback function
    print("=====================================================\n")
    print("do_callback_on_preview\n")
    userData = 3735928559
    print("Registering PREVIEW callback with userData {0}\n".format(hex(userData)))
    ret = PxLApi.setCallback(hCamera, PxLApi.Callback.PREVIEW, userData, callback_format_preview)
    if(not(PxLApi.apiSuccess(ret[0]))):
        print("ERROR setting callback function: {0}".format(ret[0]))
        return

    ret = PxLApi.setStreamState(hCamera, PxLApi.StreamState.START)
    if(not(PxLApi.apiSuccess(ret[0]))):
        print("ERROR setting stream state function: {0}".format(ret[0]))
        return

    # Set the number of seconds to run preview for
    runPreviewFor = 10
    # We will start getting our callback called after we start previewing
    # Run preview for a number of seconds
    run_preview_window_for(hCamera, runPreviewFor)
        
    ret = PxLApi.setStreamState(hCamera, PxLApi.StreamState.STOP)

    # Disable callback on preview by setting the callback function to 0 or None
    ret = PxLApi.setCallback(hCamera, PxLApi.Callback.PREVIEW, userData, 0)


def main():
    
    ret = PxLApi.initialize(0)
    if(not(PxLApi.apiSuccess(ret[0]))):
        print("ERROR: {0}\n".format(ret[0]))
        return 1
    hCamera = ret[1]
    print("\nMain thread id = {}\n".format(hex(id(threading.current_thread()))))
    
    # do_callback_on_format_image(hCamera) /* Callback.FORMAT_IMAGE is not supported */
    do_callback_on_preview(hCamera)

    PxLApi.uninitialize(hCamera)
    return 0

if __name__ == "__main__":
    main()
