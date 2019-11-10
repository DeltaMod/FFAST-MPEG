# -*- coding: utf-8 -*-
"""
FFAST-MPEG - A quicker than usual way to make gifs, trim videos, split videos and so on!
"""
import os, subprocess
import matplotlib
matplotlib.use('TKagg') 
import tkinter as tk
from tkinter import filedialog as fd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np
import time

plt.rcParams['figure.dpi']         = 90
plt.rcParams['axes.grid']          = False
plt.rcParams['axes.axisbelow']     = False
plt.rcParams['axes.spines.left']   = False
plt.rcParams['axes.spines.right']  = False
plt.rcParams['axes.spines.bottom'] = False
plt.rcParams['axes.spines.top']    = False
plt.rcParams['axes.spines.top']    = False
plt.rcParams['ytick.left']         = False
plt.rcParams['ytick.labelleft']    = False
plt.rcParams['xtick.bottom']       = False
plt.rcParams['xtick.labelbottom']  = False

FOP = [ "Remove Video Footage Before Timetamp",
        "Remove Video Footage After Timetamp",
        "Split Video at Timestamp",
        "Merge Multichannel Audio of Video",
        "Convert Video to Gif",
        "Convert Video to Image Sequence",
        "Convert Gif to Video",
        "Convert Gif to Image Sequence", 
        "Merge Videos",
        "Convert Image Sequence to Video",
        "Convert Image Sequence to Gif",
    ]
FOP = [str(n)+' - '+FOP[n] for n in range(len(FOP))]
FOPWidth = len(max(FOP, key=len))
VSAV = {'FFMPEG Mode':0}
#Define Colours to use for certain components
rootBG      = 'bisque'
frameBG     = 'moccasin'
VideoBG     = 'ghostwhite'
ButtonBG    = 'WhiteSmoke'
ButtonABG   = 'azure'
LabelBG     = 'aliceblue'
VarBG       = LabelBG 
LabelRelief = 'flat'
DDRelief    = 'sunken'

AspectRatioMaintain = False
##Set up a command to handle keeping a correct time format
def GetTime(rawtime):
        seconds  = np.floor(rawtime)
        decimals = rawtime - seconds
        SecTime = time.strftime("%H:%M:%S", time.gmtime(seconds))
        RealTime = SecTime+str(decimals)[1:5]
        return(RealTime,rawtime)
        
class FFAST_MPEGUI(object):
    LABEL_TEXT = [
        "FFAST-MPEG!",
        "FFMPEG - But Fast",
        "I can't believe it's not commandline",
        "Seriously, I made this for me - but might as well release it for free",
        "Please, if you have some great ideas for additions/changes...",
        "fork this repository, and make them"]
    def __init__(self, master):
        self.master = master 
        master.title('FFASTMPEG')
        self.XDIM = int(1600/2)
        VIDH = 100
        self.YDIM = int(900/2)
        BDW  = 3
        root.geometry('{}x{}'.format(2*self.XDIM,self.YDIM+VIDH))
        root.config(bg=rootBG)
        #Creating Frame Preview Canvas
        self.FPFrame = tk.Frame(root, bg=rootBG, width=self.XDIM, height=self.YDIM, padx=10, pady=10, bd=BDW, relief='flat') # , 
        self.FPFrame.grid(row = 0, column = 0, rowspan=2,  sticky='nwes')
        
        self.FPrev = plt.figure(1)
        self.FPCanv = FigureCanvasTkAgg(self.FPrev,master=self.FPFrame)  # A tk.DrawingArea.
        self.FPCanv.draw()
        self.FPCanv.get_tk_widget().grid(column=0,row=0)
        #self.toolbar = NavigationToolbar2Tk(self.FPCanv, root)
        #self.toolbar.update()
        #self.toolbar.get_tk_widget().grid(row=1,column=0)
        
        
        #Creating Video Control Canvas
        self.VCCanv = tk.Frame(root, bg=rootBG, width=self.XDIM, height=VIDH, padx=10, pady=10, bd=BDW, relief='flat') # , 
        self.VCCanv.grid(row = 2, column = 0,  sticky='nwes')
        
        #Creating FFMPEG Commands Frame
        self.FFCanv = tk.Frame(root, bg=rootBG, width=self.XDIM,              padx=10, pady=10, bd=BDW, relief='flat')
        self.FFCanv.grid(row = 0, column = 1,sticky='nswe')
        self.FFCanv.bind('<Configure>',self.MaintainAspect)
        
        #Creating Additional Commands Frame
        self.AddCanv = tk.Frame(root,bg=frameBG,width=self.XDIM,             padx=10, pady=10, bd=BDW, relief='groove')
        self.AddCanv.grid(row = 1, column = 1, rowspan = 2, sticky='nswe')
        
        #Setting Weights of all root relevant columms to be 1
        for j in range(3):
            for i in range(1):
                tk.Grid.rowconfigure(root, j, weight=1)
                tk.Grid.columnconfigure(root, i, weight=1)
        
        ##%% Video Viewer
        #self.VideoPreview = tk.Canvas(self.FPCanv)
        #self.VideoPreview.grid(row=0,column=0,sticky='nw')
        
        #%% Video Viewer UI Frame
        ##Frame Slider 
        self.VCSlider = tk.Scale(self.VCCanv,from_=0, to=1,orient='horizontal',command = self.SliderTime_Update,length = 300)
        self.VCSlider.grid(row=1,column=1, columnspan=3,sticky='nswe')
        
        ##Current Time Editbox
        self.Timestamp   = GetTime(float(self.VCSlider.get()))[0] 
        self.CurrentTime = tk.StringVar(root); self.CurrentTime.set('00:00:00')
        self.EndTime     = tk.StringVar(root); self.EndTime.set('00:00:00')
        self.StartTime   = tk.StringVar(root); self.StartTime.set('00:00:00')
        
        self.VCTimeEdit = tk.Entry(self.VCCanv,textvariable=self.CurrentTime)
        self.VCTimeEdit.grid(row=0,column=2)
        self.VCTimeEdit.bind('<Enter>',self.Read_Frame)

        ##Left Time 
        self.VCLT = tk.Label(self.VCCanv, textvariable=self.StartTime ,relief=LabelRelief,bg=LabelBG).grid(row = 1, column = 0,sticky='nswe')
        
        ##Right Time
        self.VCRT = tk.Label(self.VCCanv, textvariable=self.EndTime ,relief=LabelRelief,bg=LabelBG).grid(row = 1, column = 4,sticky='nswe')
        
        #%% FFMPEG Control Frame                
        ##Select Files Button
        tk.Label(self.FFCanv, text="Select One (or multiple) Files",relief=LabelRelief,bg=LabelBG).grid(row = 2, column = 0,sticky='nswe')
        
        self.Select_Files_Button = tk.Button(self.FFCanv, text='Click Here to Select Files', command=self.Select_Files)
        self.Select_Files_Button.grid(row = 3,column = 0,sticky='nswe')
        
        #Defining StringVar for SIMSEL Options Menu
        self.FFSel = tk.StringVar(root)
        self.FFSel.set(FOP[VSAV['FFMPEG Mode']])
        
        #Generating the actual OptionsMenu
        self.DDFFM= tk.OptionMenu(self.FFCanv, self.FFSel, *FOP)
        tk.Label(self.FFCanv, text="Select FFMPEG Mode",relief=LabelRelief,bg=LabelBG).grid(row = 0, column = 0,sticky='nswe')
        self.DDFFM.grid(row = 1, column =0,sticky='nswe')
        self.DDFFM.config(width = FOPWidth, bg=ButtonBG,activebackground =ButtonABG)
        self.DDFFM["menu"].config(bg=ButtonABG)
        
        # link function to change dropdown
        def FFMPChange(*args):
            VSAV['FFMPEG Mode'] = int(self.FFSel.get()[0])
            print('Now using: ', FOP[int(self.FFSel.get()[0])])
        self.FFSel.trace('w',FFMPChange)
        
        #Generating the Listbox that will contain a file listing of all selected files
        self.SelFiles = tk.Listbox(self.FFCanv,width = 2*FOPWidth)
        self.SelFiles.grid(row=1,column=1,rowspan=3,sticky='nsew')
        tk.Label(self.FFCanv, text="List of Selected Files",relief=LabelRelief,bg=LabelBG).grid(row = 0, column = 1,sticky='nswe')
        
        #Close Button
        self.close_button = tk.Button(self.AddCanv, text='Close', command=self.close)
        self.close_button.grid(row = 5,column = 5,sticky='nw')
        
        #Convert Button
        self.Convert_Button = tk.Button(self.AddCanv, text='Convert', command=self.convert)
        self.Convert_Button.grid(row = 4,column = 5,sticky='nwse')
    
    
    def Select_Files(self):
        if len(self.SelFiles.get(0,'end')) !=0:
            self.SelFiles.delete(0,tk.END)
        self.file_paths = fd.askopenfilenames()
        file_paths = [str(self.file_paths[n]) for n in range(len(self.file_paths))]
        self.file_paths = [os.path.abspath(file_paths[n]) for n in range(len(file_paths))]
        self.save_location = [os.path.dirname(os.path.abspath(file_paths[n])) for n in range(len(file_paths))]
        print(self.file_paths)
        print(self.save_location)
        print('Loaded in:\n'+''.join(self.file_paths))
        
       
        for n in range(len(self.file_paths)):    
            self.SelFiles.insert(n,self.file_paths[n])
        self.Get_Video_Info() 
        self.Read_Frame(self)  
        #AspectRatio= self.VideoInfo['height']/self.VideoInfo['width']
        #self.VideoPreview.config(width = self.XDIM , height = self.XDIM*AspectRatio )
    #def SliderRange_Update(self):
    #    print()
    def SliderTime_Update(self,event):
        self.CurrentTime.set(GetTime(float(self.VCSlider.get()))[0])
        self.Timestamp = GetTime(float(self.VCSlider.get()))[0]
        self.Read_Frame(self)
    def Read_Frame(self,event):
        self.Timestamp = GetTime(float(self.VCSlider.get()))[0]
        if len(self.SelFiles.get(0,'end')) !=0:
            RFConmm = ['ffmpeg',
                        '-ss', self.Timestamp,
                        '-i','\"'+self.file_paths[0]+'\"',
                        '-ss', '1',
                        '-f', 'image2pipe',
                        '-pix_fmt', 'rgb24',
                        '-vcodec','rawvideo', '-']
            self.pipe = subprocess.Popen(" ".join(RFConmm), stdout=subprocess.PIPE,stderr=subprocess.PIPE, bufsize=10**8)
            
            # read width*height*3 bytes (= 1 frame)
            raw_image = self.pipe.stdout.read(self.VideoInfo['height']*self.VideoInfo['width']*3)
            # transform the byte read into a numpy array 
            mpimage =  np.frombuffer(raw_image, dtype='uint8')
            mpimage = mpimage.reshape((self.VideoInfo['height'],self.VideoInfo['width'],3))
            self.FPrev = plt.imshow(mpimage)
            self.FPCanv.draw()
            self.pipe.kill()
    def Get_Video_Info(self):
        INFOPROBE = ['ffprobe',
                     '-v error -select_streams v:0 -show_entries',
                     'stream=width,height,duration,bit_rate,r_frame_rate -of default=noprint_wrappers=1',
                     '\"'+self.file_paths[0]+'\"']
        result = subprocess.Popen(" ".join(INFOPROBE), shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        RAW = list(filter(None,result.communicate()[0].decode().split('\r\n')))
        INFO = [RAW[n].split('=') for n in range(len(RAW))]
        self.VideoInfo = {INFO[i][0]:eval(INFO[i][1]) for i in range(len(INFO))}
        self.VideoInfo['format'] = '.'+self.file_paths[0].rsplit('.',1)[-1]
        print(self.VideoInfo['format'] ) #we add this for convenience, so we can construct names and file-extensions separately
        VideoName = self.file_paths[0].rsplit('.',1)[0]
        self.VideoInfo['name'] = VideoName.rsplit('\\',1)[-1]
        print(self.VideoInfo['name'] ) 
        self.VCSlider.config(from_=0, to=self.VideoInfo['duration'])
        self.StartTime.set(GetTime(0)[0])
        self.Timestamp = GetTime(self.VideoInfo['duration'])[0]
        self.EndTime.set(GetTime(self.VideoInfo['duration'])[0])
        self.CurrentTime.set(GetTime(0)[0])
        self.VCSlider.config(resolution = 1/self.VideoInfo['r_frame_rate'])
        
    
    def MaintainAspect(self,event):
        if AspectRatioMaintain == True:
            self.XDIM = int(root.winfo_width() - root.winfo_width() % 32)
            self.YDIM = int(self.XDIM*9/32)
            root.geometry('{}x{}'.format(self.XDIM,self.YDIM))
     
     
    def convert(self):
        if len(self.file_paths) == 1:
            OUTPUT = '\"'  + self.save_location[0]+'\\'+self.VideoInfo['name']+'-Trim'+self.VideoInfo['format']+'\"' 
            print(OUTPUT)
            if self.FFSel.get() == FOP[0]: #Remove Video Footage Before Timetamp
                FFASTCMD = ['ffmpeg -i',
                            '\"'   + self.file_paths[0]  + '\"',
                            '-ss '+ self.Timestamp,
                            ' -map 0 -vcodec copy -acodec copy',
                            OUTPUT]
                H = subprocess.Popen(" ".join(FFASTCMD), shell=False)
                #For future reference, if you want to communicate with commandline:
                # p.stdout.readline().rstrip()
                #'what is your name'
                #p.communicate('mike')[0].rstrip()
            
            if self.FFSel.get() == FOP[1]: #Remove Video Footage After Timetamp
                print('Not Available Yet')
            if self.FFSel.get() == FOP[2]: #Split Video at Timestamp
                OUTPUT1 = '\"'  + self.save_location[0]+'\\'+self.VideoInfo['name']+'-A'+self.VideoInfo['format']+'\"' 
                OUTPUT2 = '\"'  + self.save_location[0]+'\\'+self.VideoInfo['name']+'-B'+self.VideoInfo['format']+'\"'
                FFASTCMD = ['ffmpeg -i',
                            '\"'   + self.file_paths[0]  + '\"',
                            '-t ' + self.Timestamp,
                            '-map 0 -c copy ' +OUTPUT1,
                            '-ss ' + self.Timestamp, 
                            '-map 0 -c copy ' +OUTPUT2]
                H = subprocess.Popen(" ".join(FFASTCMD), shell=False)
            if self.FFSel.get() == FOP[3]: #Merge Multichannel Audio of Video
                print('Not Available Yet')
            if self.FFSel.get() == FOP[4]: #Convert Video to Gif
                print('Not Available Yet')
            if self.FFSel.get() == FOP[5]: #Convert Video to Image Sequence
                print('Not Available Yet')
            if self.FFSel.get() == FOP[6]: #Convert Gif to Video
                print('Not Available Yet')
            if self.FFSel.get() == FOP[7]: #Convert Gif to Image Sequence
                print('Not Available Yet')
            if self.FFSel.get() == FOP[8]: #Merge Videos
                print('Not Available Yet')
            if self.FFSel.get() == FOP[9]: #Convert Image Sequence to Video
                print('Not Available Yet')
            if self.FFSel.get() == FOP[10]: #Convert Image Sequence to Gif
                print('Not Available Yet')
    
            
                        
            print('Executed code:\n'+" ".join(FFASTCMD))
    def close(self):
        print('Bye!')
        root.destroy()

root = tk.Tk()

FFASTGUI = FFAST_MPEGUI(root)
root.mainloop()

