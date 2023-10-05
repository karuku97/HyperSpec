import os

import cv2.cv2 as cv #version 4.5.562
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
        self.FPS = 25
        self.filepath = "E:/Desktop/tmp"
        self.samples = 200
        self.filename = "test"
        self.CM = self.init_camera()
        self.Basler = kic.Basler()
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

        self.lb_FPS = ttk.Label(root, text="FPS:")
        self.lb_FPS.grid(row=1, column=0)

        self.ent_FPS = ttk.Entry(root)
        self.ent_FPS.grid(row=1, column=1,columnspan=2,sticky="ew")
        self.ent_FPS.insert(0,self.FPS)

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
        self.btn_apply.grid(row=4, column=0)

        self.btn_capture = ttk.Button(root, command=self.capture_Cube, text="Capture Cube")
        self.btn_capture.grid(row=4, column=1)

        self.btn_capture = ttk.Button(root, command=self.new_test_image, text="Test Image")
        self.btn_capture.grid(row=4, column=2)

        self.lb_test_img = ttk.Label(root,image=self.img)
        self.lb_test_img.grid(row=5,column=0,columnspan=3)

        root.mainloop()

    def new_test_image(self):
        img = self.CM.capture_frame(kic.Basler.SERIAL_NUMBER)
        img = cv.resize(img,(600,400))
        img = ImageTk.PhotoImage(Image.fromarray(img))
        self.lb_test_img.configure(image=img)
        self.lb_test_img.image = img

    def apply_Values(self):

        self.FPS = float(self.ent_FPS.get())
        self.filepath = self.ent_file.get()
        self.samples = int(self.ent_samples.get())
        self.filename = self.ent_filename.get()

        self.CM.set_framerate(self.Basler.SERIAL_NUMBER,float(self.FPS))
        self.FPS = self.CM.cameras[0].ResultingFrameRate.GetValue()
        self.ent_FPS.insert(0,self.FPS)
        print(f'Framerate set to: {self.CM.cameras[0].ResultingFrameRate.GetValue()}')
        print(f'filepath: {self.filepath}.{self.filename}.hdr')
        print(f'Number of Samples: {self.samples}')

        tkinter.messagebox.showinfo(title="Info", message=f'Applied Values{os.linesep}FPS:{self.CM.cameras[0].ResultingFrameRate.GetValue()}{os.linesep}Filepath: {self.filepath}.{self.filename}.hdr{os.linesep}Number of Samples: {self.samples}')

    def capture_Cube(self):
        cube = self.CM.grab_hyperspec(kic.Basler.SERIAL_NUMBER, self.samples, 3, False, 0)

        # Calibration
        w = [405, 632.8, 980]
        # pixelWerte
        p = [20, 225, 508]

        A, B, C = np.polyfit(p, w, 2)

        meta = kic.HyperspecUtility.generate_metadata(self.CM.cameras[0], self.samples, kic.Basler.Y_OFFSET, kic.Basler.Y_BINNING, A, B, C, 0)
        kic.HyperspecUtility.write_cube(cube,meta,self.filepath,f'{self.filename}.hdr')

        tkinter.messagebox.showinfo(title="Info",message="Cube captures Successfully")

    def init_camera(self):
        CM = kic.CameraManager()
        CM.add_cameras()
        CM.cameras[0].DeviceLinkThroughputLimitMode.SetValue("Off")

        return CM





#Basler.SERIAL_NUMBER = CM.cameras[0].GetDeviceInfo().GetSerialNumber()


#







mw =mainwindow()