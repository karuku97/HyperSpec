import os
import cv2 as cv #version 4.5.562
import numpy as np
import tkinter
from tkinter import ttk, messagebox, Frame
from PIL import Image, ImageTk
import kira_image_capture as kic



class mainwindow():
    def __init__(self):
        """Initalizing Mainwindow and defining GUI"""

        #os.environ["PYLON_CAMEMU"] = "1"
        #print(os.environ["PYLON_CAMEMU"])

        self.expTime = 83585
        # Lab PC Path
        #self.filepath = "C:/Users/HSBI/Documents/Softwareentwicklung/CaptureCubeBasler/tmp"
        # Mac Path
        self.filepath = "C:/Users/karlk/Desktop/Arbeit/Prototyp"
        self.samples = 500
        self.filename = "TestCube"
        self.Basler = kic.Basler()
        self.CM = self.init_camera()
        self.img = None
        self.SN = "40474076"
        self.width = 728
        self.height = 544
        self.bin = 1
        self.xoff = 0
        self.yoff = 0
        self.w1 = 405
        self.p1 = 20
        self.w2 = 628
        self.p2 = 506
        self.w3 = 808
        self.p3 = 894
        self.A = 0.00013639214204672206
        self.B = 1.0280932959428337
        self.C = 404.99999999999994

        if os.path.exists("save.txt"):
            self.read_txt()


        root = tkinter.Tk()
        root.title("Hyper Spectral Cube Aufnahme")

        tabControl = ttk.Notebook(root)

        tab1 = ttk.Frame(tabControl)
        tab2 = ttk.Frame(tabControl)
        tab3= ttk.Frame(tabControl)
        tabControl.add(tab1,text="Aufnahme")
        tabControl.add(tab2,text="Kamera")
        tabControl.add(tab3,text="Kalibrieren")
        tabControl.grid(row=0,column=0)


        # Aufnahme Tab
        # Anzahl an Samples
        self.lb_samples = ttk.Label(tab1, text="Number of Samples:")
        self.lb_samples.grid(row=1, column=0)

        self.ent_samples = ttk.Entry(tab1)
        self.ent_samples.grid(row=1, column=1,columnspan=2,sticky="ew")
        self.ent_samples.insert(0,self.samples)

        # Exposure Time
        self.lb_expTime = ttk.Label(tab1, text="Exposure Time:")
        self.lb_expTime.grid(row=2, column=0)

        self.ent_expTime = ttk.Entry(tab1)
        self.ent_expTime.grid(row=2, column=1,columnspan=2,sticky="ew")
        self.ent_expTime.insert(0,self.expTime)

        # File Lokation
        self.lb_file = ttk.Label(tab1, text="Filepath:")
        self.lb_file.grid(row=3, column=0)

        self.ent_file = ttk.Entry(tab1)
        self.ent_file.grid(row=3, column=1,columnspan=2,sticky="ew")
        self.ent_file.insert(0,self.filepath)

        # File name
        self.lb_filename = ttk.Label(tab1, text="Filename:")
        self.lb_filename.grid(row=4, column=0)

        self.ent_filename = ttk.Entry(tab1)
        self.ent_filename.grid(row=4, column=1,columnspan=2,sticky="ew")
        self.ent_filename.insert(0, self.filename)

        # Apply Button
        self.btn_apply = ttk.Button(tab1, text="Apply", command=self.apply_Values)
        self.btn_apply.grid(row=5, column=1)

        # Seperator
        sep1 = ttk.Separator(tab1, orient='horizontal')
        sep1.grid(row=6, column=0, columnspan=3,sticky="ew")

        # label without shading Correction
        self.lbl_without_shading = ttk.Label(tab1,text="without Shading Correction:")
        self.lbl_without_shading.grid(row=7,column=1)

        #Capture Test Image BUtton
        self.btn_capture_correct = ttk.Button(tab1, command=self.new_test_image, text="Test Image")
        self.btn_capture_correct.grid(row=8, column=0)


        # Capture Button without Shading
        self.btn_capture = ttk.Button(tab1, command=self.capture_Cube_without, text="Capture Cube")
        self.btn_capture.grid(row=8, column=1)

        # Seperator
        sep2 = ttk.Separator(tab1,orient='horizontal')
        sep2.grid(row=9,column=0,columnspan=3,sticky="ew")

        # label with shading correction
        self.lbl_with_shading = ttk.Label(tab1,text="with shading Correction:")
        self.lbl_with_shading.grid(row=10,column=1)


        # black Cube Button
        self.btn_capture_black = ttk.Button(tab1, command=self.black_cube, text="Black Correction")
        self.btn_capture_black.grid(row=11, column=0)

        # white Cube Button
        self.btn_capture_white = ttk.Button(tab1, command=self.white_cube, text="White Correction")
        self.btn_capture_white.grid(row=11, column=1)

        # Capture Button with Shading
        self.btn_capture_test = ttk.Button(tab1, command=self.capture_Cube_with, text="Capture Cube")
        self.btn_capture_test.grid(row=11, column=2)

        # Test Image label
        self.lb_test_img = ttk.Label(root, image=self.img)
        self.lb_test_img.grid(row=12, column=0, columnspan=3)


        # Kamera Tab
        # Serial number
        self.lbl_SN = ttk.Label(tab2,text="Serial Number:")
        self.lbl_SN.grid(row=1,column=0)

        self.ent_SN = ttk.Entry(tab2)
        self.ent_SN.grid(row=1, column=1, columnspan=2, sticky="ew")
        self.ent_SN.insert(0, self.SN)

        # width
        self.lbl_width = ttk.Label(tab2, text="Width:")
        self.lbl_width.grid(row=2, column=0)

        self.ent_width = ttk.Entry(tab2)
        self.ent_width.grid(row=2, column=1, columnspan=2, sticky="ew")
        self.ent_width.insert(0, str(self.width))

        # height
        self.lbl_height = ttk.Label(tab2, text="Height:")
        self.lbl_height.grid(row=3, column=0)

        self.ent_height = ttk.Entry(tab2)
        self.ent_height.grid(row=3, column=1, columnspan=2, sticky="ew")
        self.ent_height.insert(0, str(self.height))

        # Binning
        self.lbl_bin = ttk.Label(tab2, text="Binning:")
        self.lbl_bin.grid(row=4, column=0)

        self.ent_bin = ttk.Entry(tab2)
        self.ent_bin.grid(row=4, column=1, columnspan=2, sticky="ew")
        self.ent_bin.insert(0, str(self.bin))

        # X Offset
        self.lbl_xoff = ttk.Label(tab2, text="X-Offset:")
        self.lbl_xoff.grid(row=5, column=0)

        self.ent_xoff = ttk.Entry(tab2)
        self.ent_xoff.grid(row=5, column=1, columnspan=2, sticky="ew")
        self.ent_xoff.insert(0, str(self.xoff))

        # Y Offset
        self.lbl_yoff = ttk.Label(tab2, text="Y-Offset:")
        self.lbl_yoff.grid(row=6, column=0)

        self.ent_yoff = ttk.Entry(tab2)
        self.ent_yoff.grid(row=6, column=1, columnspan=2, sticky="ew")
        self.ent_yoff.insert(0, str(self.yoff))

        # Apply Button
        self.btn_apply_cam = ttk.Button(tab2, text="Apply", command=self.apply_Values_cam)
        self.btn_apply_cam.grid(row=7, column=1)


        # Kalibrierungs Tab
        #laser 1
        self.lbl_Laser1 = ttk.Label(tab3,text="Laser 1")
        self.lbl_Laser1.grid(row=2,column=0)

        self.lbl_welle1 = ttk.Label(tab3,text="Wavelenght:")
        self.lbl_welle1.grid(row=3,column=1)

        self.ent_welle1 = ttk.Entry(tab3)
        self.ent_welle1.grid(row=3,column=2,sticky="ew")
        self.ent_welle1.insert(0,str(self.w1))

        self.lbl_pixel1 = ttk.Label(tab3,text="Pixelvalue:")
        self.lbl_pixel1.grid(row=4,column=1)

        self.ent_pixel1 = ttk.Entry(tab3)
        self.ent_pixel1.grid(row=4,column=2)
        self.ent_pixel1.insert(0,str(self.p1))

        # laser 2
        self.lbl_Laser2 = ttk.Label(tab3, text="Laser 2")
        self.lbl_Laser2.grid(row=5, column=0)

        self.lbl_welle2 = ttk.Label(tab3, text="Wavelenght:")
        self.lbl_welle2.grid(row=6, column=1)

        self.ent_welle2 = ttk.Entry(tab3)
        self.ent_welle2.grid(row=6, column=2, sticky="ew")
        self.ent_welle2.insert(0, str(self.w2))

        self.lbl_pixel2 = ttk.Label(tab3, text="Pixelvalue:")
        self.lbl_pixel2.grid(row=7, column=1)

        self.ent_pixel2 = ttk.Entry(tab3)
        self.ent_pixel2.grid(row=7, column=2)
        self.ent_pixel2.insert(0, str(self.p2))

        # laser 3
        self.lbl_Laser3 = ttk.Label(tab3, text="Laser 3")
        self.lbl_Laser3.grid(row=8, column=0)

        self.lbl_welle3 = ttk.Label(tab3, text="Wavelenght:")
        self.lbl_welle3.grid(row=9, column=1)

        self.ent_welle3 = ttk.Entry(tab3)
        self.ent_welle3.grid(row=9, column=2, sticky="ew")
        self.ent_welle3.insert(0, str(self.w3))

        self.lbl_pixel3 = ttk.Label(tab3, text="Pixelvalue:")
        self.lbl_pixel3.grid(row=10, column=1)

        self.ent_pixel3 = ttk.Entry(tab3)
        self.ent_pixel3.grid(row=10, column=2)
        self.ent_pixel3.insert(0, str(self.p3))

        # Apply Button
        self.btn_apply_wave = ttk.Button(tab3, text="Apply", command=self.apply_Values_cal)
        self.btn_apply_wave.grid(row=11, column=1)




        root.mainloop()

    def __del__(self):
        """destruct mainwindow and close Camera"""
        self.CM.remove_camera(self.Basler.SERIAL_NUMBER)

    def white_cube(self):
        """Callback function for capturing bright Calibration cube"""
        tkinter.messagebox.showinfo(title="Info",message="Ready to record white frame. Place reference material in the field of view of imager.")

        white_cube = self.CM.grab_white_cube(self.Basler.SERIAL_NUMBER)
        meta = kic.HyperspecUtility.generate_metadata(self.CM.cameras[0], 30, self.Basler.Y_OFFSET,
                                                      self.Basler.Y_BINNING, self.Basler.A, self.Basler.B, self.Basler.C,
                                                      4096)

        kic.HyperspecUtility.write_cube(white_cube, meta, f'{self.filepath}/Corr', f'white_cube.hdr')
        tkinter.messagebox.showinfo(title="Info", message="white Cube captured successfully")


    def black_cube(self):
        """Callback function for capturing dark Calibration cube"""
        tkinter.messagebox.showinfo(title="Info",message="Ready to record dark frame. Place a lens cap on the imager.")
        dark_cube = self.CM.grab_dark_cube(self.Basler.SERIAL_NUMBER)
        meta = kic.HyperspecUtility.generate_metadata(self.CM.cameras[0], 30, self.Basler.Y_OFFSET,
                                               self.Basler.Y_BINNING, self.Basler.A, self.Basler.B, self.Basler.C, 4096)

        kic.HyperspecUtility.write_cube(dark_cube,meta,f'{self.filepath}/Corr',f'dark_cube.hdr')
        tkinter.messagebox.showinfo(title="Info",message="dark Cube captured successfully")


    def new_test_image(self):
        """Callback funktion for capturing one RAW frame from camera"""
        img = self.CM.capture_frame(self.Basler.SERIAL_NUMBER)
        img = cv.resize(img,(600,400))
        img = ImageTk.PhotoImage(Image.fromarray(img))
        self.lb_test_img.configure(image=img)
        self.lb_test_img.image = img

    def apply_Values(self):
        """Callback funktion for appling/setting  new Values"""
        self.expTime = float(self.ent_expTime.get())
        self.filepath = self.ent_file.get()
        self.samples = int(self.ent_samples.get())
        self.filename = self.ent_filename.get()

        self.CM.set_exposure(self.Basler.SERIAL_NUMBER,int(self.expTime))
        self.expTime = self.CM.cameras[0].ExposureTime.GetValue()
        self.ent_expTime.delete(0,tkinter.END)
        self.ent_expTime.insert(0,int(self.expTime))
        print(f'ExposureTime set to: {self.CM.cameras[0].ExposureTime.GetValue()}')
        print(f'filepath: {self.filepath}/{self.filename}.hdr')
        print(f'Number of Samples: {self.samples}')

        self.write_txt()

        tkinter.messagebox.showinfo(title="Applied Values", message=f'Exposure TIme:{self.CM.cameras[0].ExposureTime.GetValue()}{os.linesep}FPS:{self.CM.cameras[0].ResultingFrameRate.GetValue()}{os.linesep}Number of Samples: {self.samples}{os.linesep}Filepath: {self.filepath}/{self.filename}.hdr')

    def apply_Values_cam(self):
        """Callback funktion for appling/setting  new Values"""
        self.SN = str(self.ent_SN.get())
        self.width = int(self.ent_width.get())
        self.height = int(self.ent_height.get())
        self.bin = int(self.ent_bin.get())
        self.yoff = int(self.ent_yoff.get())
        self.xoff = int(self.ent_xoff.get())

        self.Basler.SERIAL_NUMBER = self.SN
        self.Basler.ROI_WIDTH = self.width
        self.Basler.ROI_HEIGHT = self.height
        self.Basler.bin = self.bin
        self.Basler.Y_OFFSET=self.yoff
        self.Basler.X_OFFSET = self.xoff

        self.CM.set_camera_window(self.Basler.SERIAL_NUMBER,self.Basler.ROI_WIDTH,self.Basler.ROI_HEIGHT,self.Basler.X_OFFSET,self.Basler.Y_OFFSET,self.Basler.Y_BINNING)

        self.write_txt()


        tkinter.messagebox.showinfo(title="Applied Values", message=f'SN:{self.Basler.SERIAL_NUMBER}{os.linesep}Width:{self.Basler.ROI_WIDTH}{os.linesep}Height: {self.Basler.ROI_HEIGHT}{os.linesep}Binning: {self.Basler.Y_BINNING} {os.linesep}X-Offset: {self.Basler.X_OFFSET}{os.linesep}Y-Offset: {self.Basler.Y_OFFSET}')

    def apply_Values_cal(self):
        """Callback function for appling new Values"""
        self.w1 = float(self.ent_welle1.get())
        self.p1 = int(self.ent_pixel1.get())

        self.w2 = float(self.ent_welle2.get())
        self.p2 = int(self.ent_pixel2.get())

        self.w3 = float(self.ent_welle3.get())
        self.p3 = int(self.ent_pixel3.get())

        self.A, self.B, self.C = np.polyfit([self.p1, self.p2, self.p3], [self.w1, self.w2, self.w3], 2)
        self.Basler.A = self.A
        self.Basler.B = self.B
        self.Basler.C = self.C

        self.write_txt()

        tkinter.messagebox.showinfo(title="Applied Values",
                                    message=f'A:{self.Basler.A}{os.linesep}B:{self.Basler.B}{os.linesep}C: {self.C}')

    def capture_Cube_without(self):
        """Callback function vor capturing a hyperspectral Cube"""
        # cube without correction
        cube = self.CM.grab_hyperspec(self.Basler.SERIAL_NUMBER, self.samples, 3, False, 4096)

        # cube with correction
        #cube = self.CM.grab_hyperspec(self.Basler.SERIAL_NUMBER, self.samples, f'{self.filepath}/Corr', True, 1)

        # PikaL (camera data class parameter
        meta = kic.HyperspecUtility.generate_metadata(self.CM.cameras[0], self.samples, self.Basler.Y_OFFSET, self.Basler.Y_BINNING, self.Basler.A, self.Basler.B, self.Basler.C, 4096)


        kic.HyperspecUtility.write_cube(cube,meta,self.filepath,f'{self.filename}.hdr')

        tkinter.messagebox.showinfo(title="Info",message="Cube captures Successfully")

    def capture_Cube_with(self):
        """Callback function vor capturing a hyperspectral Cube"""
        # cube without correction
        #cube = self.CM.grab_hyperspec(self.Basler.SERIAL_NUMBER, self.samples, 3, False, 1)

        # cube with correction
        cube = self.CM.grab_hyperspec(self.Basler.SERIAL_NUMBER, self.samples, f'{self.filepath}/Corr', True, 4096)

        # PikaL (camera data class parameter
        meta = kic.HyperspecUtility.generate_metadata(self.CM.cameras[0], self.samples, self.Basler.Y_OFFSET, self.Basler.Y_BINNING, self.Basler.A, self.Basler.B, self.Basler.C, 4096)


        kic.HyperspecUtility.write_cube(cube,meta,self.filepath,f'{self.filename}.hdr')

        tkinter.messagebox.showinfo(title="Info",message="Cube captures Successfully")

    def read_txt(self):
        f = open("save.txt","r")
        # exposure time
        line = f.readline()
        x = line.find(":") +1
        self.expTime = float(line[x:len(line)-1])

        # filepath
        line = f.readline()
        x = line.find(":") + 1
        self.filepath = str(line[x:len(line)-1])

        # filename
        line = f.readline()
        x = line.find(":") + 1
        self.filename = str(line[x:len(line)-1])

        # samples
        line = f.readline()
        x = line.find(":") + 1
        self.samples = int(line[x:])

        # SN
        line = f.readline()
        x = line.find(":") + 1
        self.SN = str(line[x:len(line)-1])

        # width
        line = f.readline()
        x = line.find(":") + 1
        self.width = int(line[x:])

        # height
        line = f.readline()
        x = line.find(":") + 1
        self.height = int(line[x:])

        # bin
        line = f.readline()
        x = line.find(":") + 1
        self.bin = int(line[x:])

        # yoff
        line = f.readline()
        x = line.find(":") + 1
        self.yoff = int(line[x:])

        # xoff
        line = f.readline()
        x = line.find(":") + 1
        self.xoff = int(line[x:])

        # w1
        line = f.readline()
        x = line.find(":") + 1
        self.w1 = float(line[x:])

        # w2
        line = f.readline()
        x = line.find(":") + 1
        self.w2 = float(line[x:])

        # w3
        line = f.readline()
        x = line.find(":") + 1
        self.w3 = float(line[x:])

        # p1
        line = f.readline()
        x = line.find(":") + 1
        self.p1 = int(line[x:])

        # p2
        line = f.readline()
        x = line.find(":") + 1
        self.p2 = int(line[x:])

        # p3
        line = f.readline()
        x = line.find(":") + 1
        self.p3 = int(line[x:])

        self.A, self.B, self.C = np.polyfit([self.p1, self.p2, self.p3], [self.w1, self.w2, self.w3], 2)
        self.Basler.A = self.A
        self.Basler.B = self.B
        self.Basler.C = self.C

        self.Basler.SERIAL_NUMBER = self.SN
        self.Basler.ROI_WIDTH = self.width
        self.Basler.ROI_HEIGHT = self.height
        self.Basler.bin = self.bin
        self.Basler.Y_OFFSET = self.yoff
        self.Basler.X_OFFSET = self.xoff

        self.CM.set_exposure(self.Basler.SERIAL_NUMBER, int(self.expTime))
        self.CM.set_camera_window(self.Basler.SERIAL_NUMBER, self.Basler.ROI_WIDTH, self.Basler.ROI_HEIGHT,
                                  self.Basler.X_OFFSET, self.Basler.Y_OFFSET, self.Basler.Y_BINNING)

        f.close()




    def write_txt(self):
        f = open("save.txt","w")
        f.write(f'exposure:{str(self.expTime)}\nfilepath:{str(self.filepath)}\nfilename:{str(self.filename)}\nsamples:{str(self.samples)}\nSN:{str(self.SN)}\nwidth:{str(self.width)}\nheight:{str(self.height)}\nbin:{str(self.bin)}\nyoff:{str(self.yoff)}\nxoff:{str(self.xoff)}\nw1:{str(self.w1)}\nw2:{str(self.w2)}\nw3:{str(self.w3)}\np1:{str(self.p1)}\np2:{str(self.p2)}\np3:{str(self.p3)}')
        f.close()


    def init_camera(self):
        """function for initializing Camera """
        CM = kic.CameraManager()
        CM.add_cameras()
        CM.cameras[0].DeviceLinkThroughputLimitMode.SetValue("Off")
        info = CM.cameras[0].GetDeviceInfo().GetSerialNumber()
        self.SN = info
        self.Basler.SERIAL_NUMBER = self.SN
        CM.set_camera_window(self.Basler.SERIAL_NUMBER,self.Basler.ROI_WIDTH,self.Basler.ROI_HEIGHT,self.Basler.X_OFFSET,self.Basler.Y_OFFSET,self.Basler.Y_BINNING)
        return CM


# new Mainwindow
mw =mainwindow()