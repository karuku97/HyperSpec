import cv2.cv2 as cv
import numpy as np
from spectral import envi
from pypylon import pylon           # version 1.9
from pypylon import genicam

def create_Metadata(h :int, w :int, frames :int):
    meta = {}
    meta["description"] = "Hyper X1 (Prototype)"
    meta["samples"] = h
    meta["lines"] = frames
    meta["bands"] = w
    meta["spectral binning"] = 1
    meta["interleave"] = "bil"
    meta["bit depth"] = 10
    meta["header offset"] = 0
    meta["framerate"] = 30
    meta["shutter"] = 1 / 25
    meta["gain"] = 1
    meta["imager type"] = "RaspiCam HQ"
    meta["imager serial number"] = "001"
    meta["wavelength units"] = "nm"
    meta["wavelength"] = create_BandInfo(w)
    meta["reflectance scale factor"] = 1
    print("Metadata created!")
    return meta

def create_BandInfo(wide :int):
    #correcturFAktor
    #Wellenlängen
    #543.5 nm -> 399 Pixel
    #632.8 nm -> 715 Pixe
    #655.0 nm -> 799 Pixel
    w = [543.5, 632.8, 655, 940]
    #pixelWerte
    p = [399, 715, 799, 1733]
    A, B, C = np.polyfit(p,w,2)
    print("A: {} , B: {} C: {}".format(A,B,C))
    BandInfo = f"{{ {', '.join(str(A * i*i +B*i +C) for i in range(0, wide))} }}"
    BandInfo = range(wide)
    print("Band Info calculated!")
    return BandInfo

def initCamera():

    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
    camera.Open()
    width = camera.Width.GetValue()
    height = camera.Height.GetValue()
    camera.ExposureTime.SetValue(200000)
    print(camera.ExposureTime.GetValue())
    print(camera.ResultingFrameRate.GetValue())
    return camera

path = "/Users/karlkuckelsberg/Desktop/HyperSpec"
filename = "/first_capture_basler"
vid_name = "/first_capture_basler.mp4"

camera = initCamera()

imgArray = []

numberOfImagesToGrab = 100
camera.StartGrabbingMax(numberOfImagesToGrab)

while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
    if grabResult.GrabSucceeded():
        img = grabResult.Array
        imgArray.append(img)


    grabResult.Release()
camera.Close()

imgArray = np.stack(imgArray, axis=0)  # dimensions (T, H, W, C)

print(imgArray.dtype)

#convert 4D Numpy Matrix to Hyperspac file
envi.save_image(f"{path}/Bil{filename}.hdr", imgArray, metadata=create_Metadata(imgArray[0].shape[0], imgArray[0].shape[1], imgArray.shape[0]), force=True, ext="bil",dtype= np.uint16)
print("HyperSpactral Image saved successfully in {}".format(f"{path}/Bil{filename}.hdr"))
