import cv2.cv2 as cv #version 4.5.562
import numpy as np
from spectral import envi
from pypylon import pylon           # version 1.9
from pypylon import genicam



def create_Metadata(h :int, w :int, frames :int):
    meta = {}
    meta["description"] = "Hyper X1 (Prototype) Basler"
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
    p = [457, 740, 814, 1625]
    A, B, C = np.polyfit(p,w,2)
    print("A: {} , B: {} C: {}".format(A,B,C))
    BandInfo = f"{{ {', '.join(str(A * i*i +B*i +C) for i in range(0, wide))} }}"
    #BandInfo = range(wide)
    print("Band Info calculated!")
    return BandInfo

def initCamera():

    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
    camera.Open()
    camera.Height.SetValue(996)
    camera.OffsetY.SetValue(104)
    width = camera.Width.GetValue()
    height = camera.Height.GetValue()
    camera.ExposureTime.SetValue(250000)
    camera.PixelFormat.SetValue("Mono12")
    camera.Gain.SetValue(0)
    print(f'Gain: {camera.Gain.GetValue()}')
    print(f'Height: {height}')
    print(f'Width: {width}')
    print(f'OffsetY: {camera.OffsetY.GetValue()}')
    print("Exposuretime:. ".format(camera.ExposureTime.GetValue()))
    print("Framerat: {}".format(camera.ResultingFrameRate.GetValue()))
    print("Pixeltype: {}".format(camera.PixelFormat.GetValue()))
    return camera

path = "C:/Users/kkuckelsberg/HyperSpec"

filename = "/Hallogen"

camera = initCamera()

imgArray = []

numberOfImagesToGrab = 40
camera.StartGrabbingMax(numberOfImagesToGrab)



while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
    if grabResult.GrabSucceeded():
        img = grabResult.Array
        imgArray.append(img)
    grabResult.Release()

camera.Close()

imgArray = np.stack(imgArray, axis=0)  # dimensions (T, H, W, C)

print(f'output datatyp: {imgArray.dtype}')

#convert 4D Numpy Matrix to Hyperspac file
envi.save_image(f"{path}/Bil{filename}.hdr", imgArray, metadata=create_Metadata(imgArray[0].shape[0], imgArray[0].shape[1], imgArray.shape[0]), force=True, ext="bil",dtype=np.uint16)
print("HyperSpactral Image saved successfully in {}".format(f"{path}/Bil{filename}.bil"))
