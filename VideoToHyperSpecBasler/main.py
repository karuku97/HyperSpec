import os

import cv2 as cv #version 4.5.562
import numpy as np
from spectral import envi
from pypylon import pylon           # version 1.9
from pypylon import genicam
import tkinter 
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

import kira_image_capture as kic


class mainwindow():
    def __init__(self):
        self.expTime = 12000
        #self.filepath = "C:/Users/HSBI/Documents/Softwareentwicklung/CaptureCubeBasler/tmp"
        self.filepath = "/Users/karlkuckelsberg/Desktop/tmp"
        self.samples = 20
        self.filename = "test"
        self.Basler = kic.Basler()
        self.CM = self.init_camera()

        self.img = None


        root = tkinter.Tk()
        root.title("Hyper Spectral Cube Aufnahme")
        #root.geometry("800x600")
        #root.minsize(width=250, height=250)

        self.lb_samples = ttk.Label(root, text="Number of Samples:")
        self.lb_samples.grid(row=0, column=0)

        self.ent_samples = ttk.Entry(root)
        self.ent_samples.grid(row=0, column=1,columnspan=2,sticky="ew")
        self.ent_samples.insert(0,self.samples)

        self.lb_expTime = ttk.Label(root, text="Exposure Time:")
        self.lb_expTime.grid(row=1, column=0)

        self.ent_expTime = ttk.Entry(root)
        self.ent_expTime.grid(row=1, column=1,columnspan=2,sticky="ew")
        self.ent_expTime.insert(0,self.expTime)

        self.lb_file = ttk.Label(root, text="Filepath:")
        self.lb_file.grid(row=2, column=0)

        self.ent_file = ttk.Entry(root)
        self.ent_file.grid(row=2, column=1,columnspan=2,sticky="ew")
        self.ent_file.insert(0,self.filepath)

        self.lb_filename = ttk.Label(root, text="Filename:")
        self.lb_filename.grid(row=2, column=0)

        self.ent_filename = ttk.Entry(root)
        self.ent_filename.grid(row=3, column=1,columnspan=2,sticky="ew")
        self.ent_filename.insert(0, self.filename)

        self.btn_apply = ttk.Button(root, text="Apply", command=self.apply_Values)
        self.btn_apply.grid(row=4, column=1)

        self.btn_capture = ttk.Button(root, command=self.capture_Cube, text="Capture Cube")
        self.btn_capture.grid(row=5, column=2)

        self.btn_capture_black = ttk.Button(root, command=self.black_cube, text="Black Correction")
        self.btn_capture_black.grid(row=5, column=0)

        self.btn_capture_white = ttk.Button(root, command=self.white_cube, text="White Correction")
        self.btn_capture_white.grid(row=5, column=1)

        self.btn_capture = ttk.Button(root, command=self.new_test_image, text="Test Image")
        self.btn_capture.grid(row=4, column=2)

        self.lb_test_img = ttk.Label(root,image=self.img)
        self.lb_test_img.grid(row=6,column=0,columnspan=3)

        root.mainloop()

    def white_cube(self):
        tkinter.messagebox.showinfo(title="Info",message="Ready to record white frame. Place reference material in the field of view of imager.")

        white_cube = self.CM.grab_white_cube(self.Basler.SERIAL_NUMBER)
        meta = kic.HyperspecUtility.generate_metadata(self.CM.cameras[0], 30, self.Basler.Y_OFFSET,
                                                      kic.Basler.Y_BINNING, self.Basler.A, self.Basler.B, self.Basler.C,
                                                      0)

        kic.HyperspecUtility.write_cube(white_cube, meta, f'{self.filepath}/Corr', f'white_cube.hdr')
        tkinter.messagebox.showinfo(title="Info", message="white Cube captured successfully")
        #print("Cube Captured")

    def black_cube(self):
        tkinter.messagebox.showinfo(title="Info",message="Ready to record dark frame. Place a lens cap on the imager.")
        dark_cube = self.CM.grab_dark_cube(self.Basler.SERIAL_NUMBER)
        meta = kic.HyperspecUtility.generate_metadata(self.CM.cameras[0], 30, self.Basler.Y_OFFSET,
                                               kic.Basler.Y_BINNING, self.Basler.A, self.Basler.B, self.Basler.C, 0)

        kic.HyperspecUtility.write_cube(dark_cube,meta,f'{self.filepath}/Corr',f'dark_cube.hdr')
        tkinter.messagebox.showinfo(title="Info",message="dark Cube captured successfully")
        #print("Cube Captured")

    def new_test_image(self):
        img = self.CM.capture_frame(self.Basler.SERIAL_NUMBER)
        img = cv.resize(img,(600,400))
        img = ImageTk.PhotoImage(Image.fromarray(img))
        self.lb_test_img.configure(image=img)
        self.lb_test_img.image = img

    def apply_Values(self):

        self.expTime = float(self.ent_expTime.get())
        self.filepath = self.ent_file.get()
        self.samples = int(self.ent_samples.get())
        self.filename = self.ent_filename.get()

        self.CM.set_exposure(self.Basler.SERIAL_NUMBER,float(self.expTime))
        self.expTime = self.CM.cameras[0].ExposureTime.GetValue()
        self.ent_expTime.delete(0,tkinter.END)
        self.ent_expTime.insert(0,int(self.expTime))
        print(f'Framerate set to: {self.CM.cameras[0].ExposureTime.GetValue()}')
        print(f'filepath: {self.filepath}/{self.filename}.hdr')
        print(f'Number of Samples: {self.samples}')

        tkinter.messagebox.showinfo(title="Applied Values", message=f'Exposure TIme:{self.CM.cameras[0].ExposureTime.GetValue()}{os.linesep}FPS:{self.CM.cameras[0].ResultingFrameRate.GetValue()}{os.linesep}Number of Samples: {self.samples}{os.linesep}Filepath: {self.filepath}/{self.filename}.hdr')

    def capture_Cube(self):
        #cube = self.CM.grab_hyperspec(self.Basler.SERIAL_NUMBER, self.samples, 3, False, 1)

        cube = self.CM.grab_hyperspec(self.Basler.SERIAL_NUMBER, self.samples, f'{self.filepath}/Corr', True, 1)
        # Calibration
        w = [405, 632.8, 980]
        # pixelWerte
        p = [20, 225, 508]

        A, B, C = np.polyfit(p, w, 2)

        # PikaL (camera data class parameter
        meta = kic.HyperspecUtility.generate_metadata(self.CM.cameras[0], self.samples, self.Basler.Y_OFFSET, kic.Basler.Y_BINNING, self.Basler.A, self.Basler.B, self.Basler.C, 0)

        #manuelle Kalibrirung
        #meta = kic.HyperspecUtility.generate_metadata(self.CM.cameras[0], self.samples, self.Basler.Y_OFFSET, kic.Basler.Y_BINNING, A, B, C, 0)

        kic.HyperspecUtility.write_cube(cube,meta,self.filepath,f'{self.filename}.hdr')

        tkinter.messagebox.showinfo(title="Info",message="Cube captures Successfully")

    def init_camera(self):
        CM = kic.CameraManager()
        CM.add_cameras()
        CM.cameras[0].DeviceLinkThroughputLimitMode.SetValue("Off")
        CM.set_camera_window(self.Basler.SERIAL_NUMBER,self.Basler.ROI_WIDTH,self.Basler.ROI_HEIGHT,self.Basler.X_OFFSET,self.Basler.Y_OFFSET,self.Basler.Y_BINNING)

        return CM

mw =mainwindow()