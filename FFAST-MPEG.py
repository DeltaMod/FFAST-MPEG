# -*- coding: utf-8 -*-
"""
FFAST-MPEG - A quicker than usual way to make gifs, trim videos, split videos and so on!

Current Version: Beta v1.0
"""
import matplotlib
matplotlib.use('TKagg') 
from os import path,remove
import pkg_resources.py2_warn
import sys
import json
from subprocess import Popen,PIPE
import tkinter as tk
from tkinter import filedialog as fd
import matplotlib.pyplot as plt
plt.ioff()
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg) #, NavigationToolbar2Tk
from numpy import floor,arange,frombuffer,ceil,zeros,uint8
from time import gmtime, strftime, sleep

#pyinstaller --onefile --noconsole -i"C:\Users\Vidar\Dropbox\Code Projects\FFAST-MPEG\FFAST-MPEG-ICON.ico" "C:\Users\Vidar\Dropbox\Code Projects\FFAST-MPEG\FFAST-MPEG.py"
#pyinstaller "C:\Users\Vidar\Dropbox\Code Projects\FFAST-MPEG\FFAST-MPEG.spec"

plt.rcParams['figure.dpi']         = 20
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
        "Convert Image Sequence to Gif"]

FOPOUT = ['Video','Video','Video','Video','Gif','Image','Video','Image','Video','Video','Gif']

VidFormat = ['.mp4',
             '.webm',
             '.mkv',
             '.mov',
             '.flv',
             '.vob',
             '.ogv',
             '.avi',
             '.mts',
             '.wmv',
             '.yuv',
             '.asf']
GifFormat = ['.gif',
             '.apng']
ImgFormat = ['.png',
             '.tiff',
             '.bmp',
             'other']
OUTFORMAT = {'Video':VidFormat,'Gif':GifFormat,'Image':ImgFormat}

FOP = [str(n)+' - '+FOP[n] for n in range(len(FOP))]
FOPWidth = len(max(FOP, key=len))
VSAV = {'FFMPEG Mode':0,'Var_Complex':True,'Output Type':'Video'}
FOPN = {FOP[0]  :'TrimS',
        FOP[1]  :'TrimE',
        FOP[2]  :'Split',
        FOP[3]  :'MCM',
        FOP[4]  :'V2Gif',
        FOP[5]  :'V2Seq',
        FOP[6]  :'Gif2V',
        FOP[7]  :'Gif2Seq',
        FOP[8]  :'Merge',
        FOP[9]  :'Seq2V',
        FOP[10] :'Seq2Gif' } #This is to automatically name output properly!
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
    seconds  = floor(rawtime)
    decimals = rawtime - seconds
    SecTime = strftime("%H:%M:%S", gmtime(seconds))
    RealTime = SecTime+str(decimals)[1:5]
    return(RealTime,rawtime)

def SetTime(ST):
    ST = ST.replace(':','.').split('.')
    TIME = int(ST[0])*60**2 + int(ST[1])*60 + int(ST[2]) + eval('0.'+ST[3])
    return(TIME)
        
class FFAST_MPEGUI(object):
    LABEL_TEXT = [  "FFAST-MPEG!",
                    "FFMPEG - But Fast",
                    "I can't believe it's not commandline",
                    "Seriously, I made this for me - but might as well release it for free",
                    "Please, if you have some great ideas for additions/changes...",
                    "fork this repository, and make them"]
        
    def __init__(self, master):    
        self.master = master 
        self.surpress_verbose = False 
        master.title('FFASTMPEG')
        self.XDIM = int(1600/2)
        VIDH = 100
        self.YDIM = int(900/2)
        BDW  = 3
        root.geometry('{}x{}'.format(2*self.XDIM,self.YDIM+VIDH))
        root.config(bg=rootBG)
        
        #Creating Frame Preview Canvas
        #self.FPFrame = tk.Frame(root, bg=rootBG, width=self.XDIM, height=self.YDIM, padx=10, pady=10, bd=BDW, relief='flat') # , 
        #self.FPFrame.grid(row = 0, column = 0, rowspan=2,  sticky='nwes')
        
        self.FPrev = plt.figure(1)
        self.FPrev.subplots_adjust(bottom=0, top=1, left=0, right=1)
        self.FPCanv = FigureCanvasTkAgg(self.FPrev,master=root)  # A tk.DrawingArea.
        self.FPCanv.draw()
        self.FPCanv.get_tk_widget().grid(column=0,row=0,rowspan=2,sticky='nwes',padx=10,pady=10)
        #self.toolbar = NavigationToolbar2Tk(self.FPCanv, root)
        #self.toolbar.update()
        #self.toolbar.get_tk_widget().grid(row=1,column=0)
        
        
        #Creating Video Control Canvas
        self.VCCanv = tk.Frame(root, bg=rootBG, width=self.XDIM, height=VIDH, padx=10, pady=10, bd=BDW, relief='flat') # , 
        self.VCCanv.grid(row = 2, column = 0,  sticky='nwes')
        
        #Creating FFMPEG Commands Frame
        self.FFCanv = tk.Frame(root, bg=rootBG, width=self.XDIM,        padx=10, pady=10, bd=BDW, relief='flat')
        self.FFCanv.grid(row = 0, column = 1,sticky='nwe')
        self.FFCanv.bind('<Configure>',self.MaintainAspect)
        
        #Creating Additional Commands Frame
        self.AddCanv = tk.Frame(root,bg=frameBG,width=self.XDIM,             padx=10, pady=10, bd=BDW, relief='groove')
        self.AddCanv.grid(row = 1, column = 1, rowspan = 2, sticky='nwe')
        
        #Ensure that any click outside of entry will result in focus loss
        root.bind_class("Frame","<1>", lambda event:event.widget.focus_set())
        
        
        FILTEROPTIONS = ['FPS','Scale','Height','Width','Bitrate','Format']
         
        #for opt in FILTEROPTIONS:
        #       setattr(self,'Var_'+opt,tk.StringVar(root)); self.__getattribute__('Var_'+opt).set('0')
        self.VideosLoaded = 'None'
        self.FirstFrameLoad = False
        self.Var_Outputname     = tk.StringVar(root);  self.Var_Outputname.set('')
        self.Var_FPS            = tk.StringVar(root);  self.Var_FPS.set('0')
        #self.Var_Scale          = tk.StringVar(root);  self.Var_Scale.set('0')
        self.Var_Height         = tk.StringVar(root);  self.Var_Height.set('0')
        self.Var_Width          = tk.StringVar(root);  self.Var_Width.set('0')
        self.Var_Bitrate        = tk.StringVar(root);  self.Var_Bitrate.set('0')
        self.Var_Complex        = tk.BooleanVar(root); self.Var_Complex.set(False);
        self.Var_StatMode       = tk.StringVar(root);  self.Var_StatMode.set('diff')
        self.Var_PreserveAspect = tk.BooleanVar(root); self.Var_PreserveAspect.set(True);
         
         
         
        self.Edit_FileName = tk.Entry(self.AddCanv,justify='l',textvariable=self.Var_Outputname,state='disabled')
        self.Edit_FileName.grid(row=0,column=1,columnspan=5,sticky='nsew')
        self.Var_Outputname.trace_add('write',self.Check_Filename_Available)
        
        tk.Label(self.AddCanv,text='Use Complex Filter').grid(column=0,row=1,sticky='nswe')
        self.Edit_ComplexFilter= tk.Checkbutton(self.AddCanv,variable=self.Var_Complex,command=self.Toggle_Complex_Filter)
        self.Edit_ComplexFilter.grid(row=1,column=1,sticky='nswe')
        
        tk.Label(self.AddCanv,text='Keep Aspect Ratio').grid(column=0,row=2,sticky='nswe')
        self.Edit_PreserveAspect= tk.Checkbutton(self.AddCanv,variable=self.Var_PreserveAspect)
        self.Edit_PreserveAspect.grid(column=1,row=2,sticky='nswe')
        
        tk.Label(self.AddCanv,text='Set Custom').grid(column=3,row=1,sticky='nswe')
        self.Edit_FPS     = tk.Entry(self.AddCanv,justify='c',textvariable=self.Var_FPS)
        self.Edit_FPS.grid(     row=2,column=3,sticky='nsew')
        #self.Edit_Scale   = tk.Entry(self.AddCanv,justify='c',textvariable=self.Var_Scale)
        #self.Edit_Scale.grid(   row=3,column=3,sticky='nsew')
        self.Edit_Height  = tk.Entry(self.AddCanv,justify='c',textvariable=self.Var_Height)
        self.Edit_Height.bind('<FocusOut>',self.Preserve_Aspect_H)
        self.Edit_Height.grid(  row=3,column=3,sticky='nsew')
        self.Edit_Width   = tk.Entry(self.AddCanv,justify='c',textvariable=self.Var_Width)
        self.Edit_Width.bind('<FocusOut>',self.Preserve_Aspect_W)
        self.Edit_Width.grid(   row=4,column=3,sticky='nsew')
        self.Edit_Bitrate = tk.Entry(self.AddCanv,justify='c',textvariable=self.Var_Bitrate)
        self.Edit_Bitrate.grid( row=5,column=3,sticky='nsew')
        self.DD_Format_Gen()
        
        tk.Label(self.AddCanv,text='FPS').grid(    column=2,row=2,sticky='nswe')
        #tk.Label(self.AddCanv,text='Scale').grid(  column=2,row=3,sticky='nswe')
        tk.Label(self.AddCanv,text='Height').grid( column=2,row=3,sticky='nswe')
        tk.Label(self.AddCanv,text='Width').grid(  column=2,row=4,sticky='nswe')
        tk.Label(self.AddCanv,text='Bitrate').grid(column=2,row=5,sticky='nswe')
        tk.Label(self.AddCanv,text='Format').grid( column=2,row=6,sticky='nswe')
        
        tk.Label(self.AddCanv,text='Source Value').grid(column=5,row=1,sticky='nswe')
        self.Default_FPS     = tk.Label(self.AddCanv,justify='c',text='')
        self.Default_FPS.grid(    row=2,column=5,sticky='nsew')
        #self.Default_Scale   = tk.Label(self.AddCanv,justify='c',textvariable=self.Var_Scale)
        #self.Default_Scale.grid(  row=3,column=5,sticky='nsew')
        self.Default_Height  = tk.Label(self.AddCanv,justify='c',text='')
        self.Default_Height.grid( row=3,column=5,sticky='nsew')
        self.Default_Width   = tk.Label(self.AddCanv,justify='c',text='')
        self.Default_Width.grid(  row=4,column=5,sticky='nsew')
        self.Default_Bitrate = tk.Label(self.AddCanv,justify='c',text='')
        self.Default_Bitrate.grid(row=5,column=5,sticky='nsew')
        self.Default_Format  = tk.Label(self.AddCanv,justify='c',text='')
        self.Default_Format.grid( row=6,column=5,sticky='nsew')
        
        self.Toggle_Complex_Filter()
        #Close Button
        self.close_button = tk.Button(self.AddCanv, text='Close', command=self.close)
        self.close_button.grid(row = 10,column = 10,sticky='es')
        
        #Convert Button
        self.Convert_Button = tk.Button(self.AddCanv, text='Convert', command=self.Rename_Or_Overwrite,state='disabled')
        self.Convert_Button.grid(row = 0,column = 0,sticky='nwse')
        #Setting Weights of all root relevant columms to be 1
        for j in range(3):
            for i in range(1):
                tk.Grid.rowconfigure(root, j, weight=1)
                tk.Grid.columnconfigure(root, i, weight=1)
        
        ##%% Video Viewer
        #self.VideoPreview = tk.Canvas(self.FPCanv)
        #self.VideoPreview.grid(row=0,column=0,sticky='nw')
        
        #%% Video Viewer UI Frame
        for j in range(1,8):
            self.VCCanv.grid_columnconfigure(j, weight=1)
        for i in range(1):
            self.VCCanv.grid_rowconfigure(i, weight=1)
        ##Frame Slider 
        self.VCSlider = tk.Scale(self.VCCanv,from_=0, to=1,orient='horizontal',length=None,command = self.SliderTime_Update)
        self.VCSlider.grid(row=1,column=1, columnspan=7,sticky='nswe')
        
        ##Current Time Editbox
        self.Timestamp   = GetTime(float(self.VCSlider.get()))[0] 
        self.CurrentTime = tk.StringVar(root); self.CurrentTime.set('00:00:00')
        self.EndTime     = tk.StringVar(root); self.EndTime.set('00:00:00')
        self.StartTime   = tk.StringVar(root); self.StartTime.set('00:00:00')
        
        self.VCTimeEdit = tk.Entry(self.VCCanv,justify='center',textvariable=self.CurrentTime)
        self.VCTimeEdit.grid(row=0,column=4,sticky='s')
        self.VCTimeEdit.bind('<Return>',self.TimeEditToSlider)

        ##Left Time 
        self.VCLT = tk.Label(self.VCCanv, textvariable=self.StartTime ,relief=LabelRelief,anchor='w',bg=LabelBG)
        self.VCLT.grid(row = 1, column = 0,sticky='nsw')
        
        ##Right Time
        self.VCRT = tk.Label(self.VCCanv, textvariable=self.EndTime ,relief=LabelRelief,anchor='e',bg=LabelBG)
        self.VCRT.grid(row = 1, column = 8,sticky='nse')
        #%% FFMPEG Control Frame          
        ##Select Files Button
        
        
        self.Select_Files_Button = tk.Button(self.FFCanv, text='Select New File(s)', command=self.Select_Files)
        self.Add_Files_Button    = tk.Button(self.FFCanv, text='Add More File(s)',   command=self.Add_Files)
        self.Select_Files_Button.grid(row = 2,column = 0,rowspan=2,sticky='nswe')
        self.Add_Files_Button.grid(row = 4,column = 0,rowspan=2,sticky='nswe')
        #Defining StringVar for SIMSEL Options Menu
        self.FFSel = tk.StringVar(root)
        self.FFSel.set(FOP[VSAV['FFMPEG Mode']])
        
        #Generating the actual OptionsMenu
        self.DDFFM= tk.OptionMenu(self.FFCanv, self.FFSel, *FOP)
        tk.Label(self.FFCanv, text="Select FFMPEG Mode",relief=LabelRelief,bg=LabelBG).grid(row = 0, column = 0,sticky='nswe')
        self.DDFFM.grid(row = 1, column =0,sticky='nswe')
        self.DDFFM.config(width = FOPWidth, bg=ButtonBG,activebackground = ButtonABG)
        self.DDFFM["menu"].config(bg=ButtonABG)
        
        # link function to change dropdown
        def FFMPEG_MODE(*args):
            VSAV['FFMPEG Mode'] = int(self.FFSel.get()[0])
            self.Print_Console('Now using: '+ FOP[int(self.FFSel.get()[0])],'SettingsChange')
            self.Check_Format()
            if self.VideosLoaded != 'None':
                self.Var_Outputname.set(self.VideoInfo['name'][0]+'-'+FOPN[self.FFSel.get()])
            self.FF_Maker()

        def OUTPUT_Change(*args):
            self.Print_Console('Now using: '+ FOP[int(self.FFSel.get()[0])])
            if self.VideosLoaded != 'None':
                self.Var_Outputname.set(self.VideoInfo['name'][0]+'-'+FOPN[self.FFSel.get()])
                
                     
        self.FFSel.trace('w',FFMPEG_MODE)
        self.Var_Format.trace('w',OUTPUT_Change)
        
      
        #Generating the Listbox that will contain a file listing of all selected files
        self.SelFiles = tk.Listbox(self.FFCanv,width = 2*FOPWidth)
        self.SelFiles.grid(row=1,column=1,rowspan=6,sticky='nsew')
        tk.Label(self.FFCanv, text="List of Selected Files",relief=LabelRelief,bg=LabelBG).grid(row = 0, column = 1,sticky='nswe')
        
        # Generating the text widget that will contain all console entries
        tk.Label(self.FFCanv, text="Console Output",relief=LabelRelief,bg=LabelBG).grid(row = 6, column = 1,sticky='nwse')
        self.ConsoleOUT = tk.Text(self.FFCanv,width = 5,height=7,font=('CMU Serif', 8))
        self.ConsoleOUT.grid(row=7,column=1,rowspan=1,sticky='nswe')
        self.ConsoleOUT.bind("<Key>", lambda e: self.Allow_Text_Copy(e))
        self.ConsoleOUT.tag_config('warning', background="yellow", foreground="red")
        self.ConsoleOUT.tag_config('SettingsChange', background="white", foreground="green")
        self.ConsoleOUT.tag_config('normal', background="white", foreground="black")
        self.ConsoleOUT.tag_config('VideoInfo', background="white", foreground="blue")
        
        # Generating the text widget that will contain the current command that will be executed
        tk.Label(self.FFCanv, text="Current FFMPEG Command",relief=LabelRelief,bg=LabelBG).grid(row = 6, column = 0,sticky='nwse')
        self.FFCurrent = tk.Text(self.FFCanv,width = 5,height=7,font=('CMU Serif', 8))
        self.FFCurrent.grid(row=7,column=0,rowspan=1,sticky='nswe')
        self.RunFinalCode = False
        
    def Check_Single_Multi_File(self):
        if len(self.SelFiles.get(0,'end')) == 0:
            self.VideosLoaded = 'None'
          
        elif len(self.SelFiles.get(0,'end')) == 1:
            self.VideosLoaded = 'Single'
                 
        elif len(self.SelFiles.get(0,'end')) >1:
            self.VideosLoaded = 'Multi'
        
        self.NumFiles =  len(self.SelFiles.get(0,'end'))
   
    def Preserve_Aspect_H(self,event):
        if self.VideosLoaded != 'None':
            if self.Var_PreserveAspect.get() == True:
                NewHeight = self.VideoInfo['h_aspect']*int(ceil(float(self.Var_Height.get()))/self.VideoInfo['h_aspect'])
                NewWidth  = int(NewHeight*self.VideoInfo['aspect ratio'])
                self.Var_Width.set(str(NewWidth))
                self.Var_Height.set(str(NewHeight))
    def Preserve_Aspect_W(self,event):
        if self.VideosLoaded != 'None':
            if self.Var_PreserveAspect.get() == True:
                NewWidth = self.VideoInfo['w_aspect']*int(ceil(float(self.Var_Width.get()))/self.VideoInfo['w_aspect'])
                NewHeight  = int(NewWidth/self.VideoInfo['aspect ratio'])
                self.Var_Width.set(str(NewWidth))
                self.Var_Height.set(str(NewHeight))

    def Check_Format(self):
        VSAV['Output Type'] = FOPOUT[int(FGUI.FFSel.get()[0])]
        self.Edit_Format.destroy()
        self.DD_Format_Gen()
        if self.VideosLoaded != 'None':
            if VSAV['Output Type'] == 'Video' and self.VideoInfo['format-in'][0] in VidFormat:
                self.VideoInfo['format-out'] = self.VideoInfo['format-in'][0]
                self.Var_Format.set(self.VideoInfo['format-out'])
            elif VSAV['Output Type'] == 'Video' and self.VideoInfo['format-in'][0] not in VidFormat:
                self.VideoInfo['format-out'] = '.mp4'
                self.Var_Format.set(self.VideoInfo['format-out'])
            elif VSAV['Output Type'] == 'Gif':
                self.VideoInfo['format-out'] = '.gif'
                self.Var_Format.set(self.VideoInfo['format-out'])
            elif VSAV['Output Type'] == 'Image':
                self.VideoInfo['format-out'] = '.png'
                self.Var_Format.set(self.VideoInfo['format-out'])
                
                
                self.Print_Console('Output format = '+self.VideoInfo['format-out'],'VideoInfo')
        if self.VideosLoaded == 'None':
            self.VideoInfo = {'format-out':''}
    def Select_Files(self):
        self.FirstFrameLoad = False   
        if self.VideosLoaded != 'None':
            self.SelFiles.delete(0,tk.END)
        self.file_paths = fd.askopenfilenames()
        file_paths = [str(self.file_paths[n]) for n in range(len(self.file_paths))]
        self.file_paths = [path.abspath(file_paths[n]) for n in range(len(file_paths))]
        self.save_location = [path.dirname(path.abspath(file_paths[n])) for n in range(len(file_paths))]
        self.Print_Console(self.file_paths,'VideoInfo')
        self.Print_Console(self.save_location,'VideoInfo')
        self.Print_Console('Loaded in:\n'+''.join(self.file_paths),'VideoInfo')
        for n in range(len(self.file_paths)):    
            self.SelFiles.insert(n,self.file_paths[n])
        self.Check_Single_Multi_File()
        self.Get_Video_Info() 
        self.Read_Frame(self)
          

    def Add_Files(self):
        self.FirstFrameLoad = False
        if self.VideosLoaded != 'None':
            self.file_paths = fd.askopenfilenames()
            file_paths = [str(self.file_paths[n]) for n in range(len(self.file_paths))]
            self.file_paths = [path.abspath(file_paths[n]) for n in range(len(file_paths))]
            self.save_location = [path.dirname(path.abspath(file_paths[n])) for n in range(len(file_paths))]
            self.Print_Console(self.file_paths,'VideoInfo')
            self.Print_Console(self.save_location,'VideoInfo')
            self.Print_Console('Loaded in:\n'+''.join(self.file_paths),'VideoInfo')
            
            for n in range(len(self.file_paths)):    
                self.SelFiles.insert(n,self.file_paths[n])
                self.Check_Single_Multi_File()
                self.Get_Video_Info() 
                self.Read_Frame(self)
                
        else:
            self.Select_Files()
   
    
    def Print_Console(self,text,TxtType):
        
        if type(text) == list:
            PRINT = [str(text[n]) for n in range(len(text))]
            PRINT = "\n".join(PRINT)
        else:
            PRINT = str(text)
        self.ConsoleOUT.insert('end','\n'+PRINT,TxtType)
        self.ConsoleOUT.see('end')
        #AspectRatio= self.VideoInfo['height']/self.VideoInfo['width']
        #self.VideoPreview.config(width = self.XDIM , height = self.XDIM*AspectRatio )

    def TimeEditToSlider(self,*args):
        self.master.focus()   
        OGT = GetTime(float(self.VCSlider.get()))[0]
        TIN = self.CurrentTime.get()
        if TIN.count(':') == 2 and TIN.count('.') == 1:
                TO = SetTime(TIN)
                print(TO)
                if round(TO,3) in arange(round(0.0,3),round(self.VideoInfo['duration'][0],3),0.001):
                    self.VCSlider.set(TO) 
                    
                else:
                    self.CurrentTime.set(OGT)
                    self.Print_Console('Please select a time in the correct range','warning')
        else:
            self.CurrentTime.set(OGT)
            self.Print_Console('Use a valid format please','warning')
        
    def SliderTime_Update(self,event):
        print('Event Called')
        self.CurrentTime.set(GetTime(float(self.VCSlider.get()))[0])
        self.Timestamp = GetTime(float(self.VCSlider.get()))[0]
        self.Read_Frame(self)

        
    def Read_Frame(self,event):
        if self.FirstFrameLoad == False:
              mpimage = zeros([self.VideoInfo['height'][0],self.VideoInfo['width'][0],3], dtype=uint8)
              self.FPrev = plt.imshow(mpimage,aspect='auto') 
              self.FirstFrameLoad = True
        if self.VideosLoaded == 'Single':
            self.Timestamp = GetTime(float(self.VCSlider.get()))[0]
            RFConmm = ['ffmpeg',
                        '-ss', self.Timestamp,
                        '-i','\"'+self.file_paths[0]+'\"',
                        '-ss', '0.01',
                        '-f', 'image2pipe',
                        '-pix_fmt', 'rgb24',
                        '-vcodec','rawvideo', '-']
            BuffSz = self.VideoInfo['height'][0]*self.VideoInfo['width'][0]*3 + 500
            self.pipe = Popen(" ".join(RFConmm), stdout=PIPE,stderr=PIPE, bufsize=BuffSz)
            # read width*height*3 bytes (= 1 frame)
            raw_image = self.pipe.stdout.read(self.VideoInfo['height'][0]*self.VideoInfo['width'][0]*3)
            # transform the byte read into a numpy array 
            mpimage =  frombuffer(raw_image, dtype='uint8')
            mpimage = mpimage.reshape((self.VideoInfo['height'][0],self.VideoInfo['width'][0],3))
            self.FPrev.set_data(mpimage)
            """
            Right now, FPCanv.draw() is the reason why the image preview is incredibly slow. Is there a way for us to do this faster?
            """
            self.FPCanv.draw()
            self.pipe.kill()
            
        elif self.VideosLoaded == 'Multi':
            VID = int(self.VCSlider.get())
            RFConmm = ['ffmpeg',
                        '-ss', '0',
                        '-i','\"'+self.file_paths[VID]+'\"',
                        '-ss', '0.01',
                        '-f', 'image2pipe',
                        '-pix_fmt', 'rgb24',
                        '-vcodec','rawvideo', '-']
            if self.VideoInfo['format-in'][VID] == '.jpg' :
                   self.Print_Console('ERROR: image2pipe does not support .jpg files - try to use .png\'s instead if you need the file preview (Note that you can still use all the fuctionality of the software without this preview)','warning')
            BuffSz = self.VideoInfo['height'][VID]*self.VideoInfo['width'][VID]*3 + 500
            self.pipe = Popen(" ".join(RFConmm), stdout=PIPE,stderr=PIPE, bufsize=BuffSz)
            # read width*height*3 bytes (= 1 frame)
            raw_image = self.pipe.stdout.read(self.VideoInfo['height'][VID]*self.VideoInfo['width'][VID]*3)
            self.TempStorage = raw_image
            # transform the byte read into a numpy array 
            mpimage =  frombuffer(raw_image, dtype='uint8')
            mpimage = mpimage.reshape((self.VideoInfo['height'][VID],self.VideoInfo['width'][VID],3))
            self.FPrev.set_data(mpimage)
            self.FPCanv.draw()
            self.pipe.kill()
            
        
    def Get_Video_Info(self):
        self.ProbeStream = ['width','height','duration','bit_rate','r_frame_rate','display_aspect_ratio','pix_fmt']
        self.VinfoFields = self.ProbeStream+['format-in','format-out','audio streams','name','w_aspect','h_aspect','aspect ratio']
        self.VideoInfo = dict((key, []) for key in self.VinfoFields)
        
        for i in range(len(self.file_paths)):
            VINFOPROBE = ['ffprobe',
                         '-v error -select_streams v:0 -show_entries',
                         'stream='+','.join(self.ProbeStream)+ ' -of default=noprint_wrappers=1',
                         '\"'+self.file_paths[i]+'\"']
            AINFOPROBE = ['ffprobe -v error -show_entries stream=codec_type -of default=noprint_wrappers=1 ',
                          '\"'+self.file_paths[i]+'\"']
            print(" ".join(AINFOPROBE))
            print(" ".join(VINFOPROBE))
            if self.surpress_verbose == False:
                self.Print_Console(" ".join(VINFOPROBE),'normal')
                self.Print_Console(" ".join(AINFOPROBE),'normal')
            elif i == 0:
                self.Print_Console(" ".join(VINFOPROBE),'normal')
                self.Print_Console(" ".join(AINFOPROBE),'normal')
                print(" ".join(AINFOPROBE))
                print(" ".join(VINFOPROBE))
                
            resultv = Popen(" ".join(VINFOPROBE), shell=False,stdout=PIPE, stderr=PIPE)
            resulta = Popen(" ".join(AINFOPROBE), shell=False,stdout=PIPE, stderr=PIPE)
            RAW = list(filter(None,resultv.communicate()[0].decode().split('\r\n')))
            INFO = [RAW[n].split('=') for n in range(len(RAW))]

            self.VideoInfo['format-in'].append('.'+self.file_paths[i].rsplit('.',1)[-1])
            print(INFO)
            for j in range(len(INFO)):
                try:
                    self.VideoInfo[INFO[j][0]].append(eval(INFO[j][1]))
                except NameError:
                    self.VideoInfo[INFO[j][0]].append(INFO[j][1])
                except SyntaxError:
                    self.VideoInfo['w_aspect'].append(int(INFO[j][1].split(':')[0]))
                    self.VideoInfo['h_aspect'].append(int(INFO[j][1].split(':')[1]))
            try:
                if self.VideoInfo['display_aspect_ratio'][-1] == 'N/A':
                    NearestRatio =  self.gcd(self.VideoInfo['width'][i],self.VideoInfo['height'][i])
                    self.VideoInfo['w_aspect'].append(self.VideoInfo['width'][i]/NearestRatio)
                    self.VideoInfo['h_aspect'].append(self.VideoInfo['height'][i]/NearestRatio)
            except IndexError:
                NearestRatio =  self.gcd(self.VideoInfo['width'][i],self.VideoInfo['height'][i])
                self.VideoInfo['w_aspect'].append(self.VideoInfo['width'][i]/NearestRatio)
                self.VideoInfo['h_aspect'].append(self.VideoInfo['height'][i]/NearestRatio)
            self.VideoInfo['audio streams'].append(resulta.communicate()[0].decode().count('audio'))
            #self.VideoInfo['video streams'] = resultv.communicate()[0].decode().count('video')
            VideoName = self.file_paths[i].rsplit('.',1)[0]
            self.VideoInfo['name'].append(VideoName.rsplit('\\',1)[-1])
            self.VideoInfo['aspect ratio'].append(self.VideoInfo['width'][i]/self.VideoInfo['height'][i])
                    
        if self.VideosLoaded == 'Single':
            if type(self.VideoInfo['duration'][0]) == int  :
                self.VideoInfo['duration'][0] = 1
                self.VCSlider.config(from_=0, to=self.VideoInfo['duration'][0] - 2/self.VideoInfo['r_frame_rate'][0] ,resolution = 1/self.VideoInfo['r_frame_rate'][0])
            else:
                self.VCSlider.config(from_=0, to=self.VideoInfo['duration'][0] - 2/self.VideoInfo['r_frame_rate'][0] ,resolution = 1/self.VideoInfo['r_frame_rate'][0])
        elif self.VideosLoaded == 'Multi':
            for i in range(len(self.SelFiles.get(0,'end'))):
                self.VideoInfo['duration'][i] = len(self.SelFiles.get(0,'end'))
            self.VCSlider.config(from_=0, to=self.VideoInfo['duration'][0] - 1,resolution = 1)
        self.StartTime.set(GetTime(0)[0])
        self.Timestamp = GetTime(self.VideoInfo['duration'][0])[0]
        self.EndTime.set(GetTime(self.VideoInfo['duration'][0])[0])
        self.CurrentTime.set(GetTime(0)[0])
        self.Check_Format()
        
        #for key, value in self.VideoInfo.items():
        #    if self.VideoInfo[key][i] == 'N/A':
        #       self.VideoInfo[key][i] = 0
        
        self.Print_Console(self.VideoInfo,'VideoInfo')
        print(self.VideoInfo)
        self.Convert_Button.config(state='normal')
        self.Edit_FileName.config(state='normal')
        self.Var_Outputname.set(self.VideoInfo['name'][0]+'-'+FOPN[self.FFSel.get()])
        
        self.Var_FPS.set(    self.VideoInfo['r_frame_rate'][0])
        self.Var_Bitrate.set(self.VideoInfo['bit_rate'][0])
        self.Var_Width.set(  self.VideoInfo['width'][0])
        self.Var_Height.set( self.VideoInfo['height'][0])
        self.Var_Format.set(OUTFORMAT[VSAV['Output Type']][OUTFORMAT[VSAV['Output Type']].index(self.VideoInfo['format-out'].lower())])
        
        self.Default_FPS.config(    text = self.VideoInfo['r_frame_rate'][0])
        self.Default_Bitrate.config(text = self.VideoInfo['bit_rate'][0])
        self.Default_Width.config(  text = self.VideoInfo['width'][0])
        self.Default_Height.config( text = self.VideoInfo['height'][0])
        self.Default_Format.config( text = self.VideoInfo['format-out'])
        
    def MaintainAspect(self,event):
        if AspectRatioMaintain == True:
            self.XDIM = int(root.winfo_width() - root.winfo_width() % 32)
            self.YDIM = int(self.XDIM*9/32)
            root.geometry('{}x{}'.format(self.XDIM,self.YDIM))

    def Check_Filename_Available(self,*args):
        self.FileExist = path.isfile( self.save_location[0]+'\\'+self.Var_Outputname.get()+self.VideoInfo['format-out']) 
        if self.FileExist == False and self.Var_Outputname.get() !='':
            self.Edit_FileName.config(bg='lightgreen')
        if self.FileExist == True:
            self.Edit_FileName.config(bg='coral')
        if self.VideosLoaded == 'None':
            self.Edit_FileName.config(bg='white',state='disabled')
            self.Convert_Button.config(state='disabled')
        
    def Rename_Or_Overwrite(self):
        self.RunFinalCode = True
        self.OUTPUTNAME = tk.StringVar(root); self.OUTPUTNAME.set(self.Var_Outputname.get())
        self.OUTPUTNAME.trace_add('write',self.CheckNameAvailable)
        self.FileExist = path.isfile( self.save_location[0]+'\\'+self.OUTPUTNAME.get()+self.VideoInfo['format-out'])
        self.Print_Console('File Exist = '+str(self.FileExist),'normal')
        if self.FileExist == True:
            self.QuestFrame = tk.Toplevel(root)
            self.QuestFrame.focus()
            self.QuestFrame.grab_set()
            self.NameEntry   = tk.Entry(self.QuestFrame,textvariable=self.OUTPUTNAME,bg='coral',width=(10+len(self.OUTPUTNAME.get())))
            self.NameEntry.grid(row=0,column=0,columnspan=3,sticky='nsew')
            self.Overwrite   = tk.Button(self.QuestFrame,text='Overwrite',command=self.convert).grid(row=1,column=0,sticky='nsew',padx=5,pady=5)
            self.NameChange  = tk.Button(self.QuestFrame,text='Use New Name',state='disabled',command=self.CheckIfConvert)
            self.NameChange.grid(row=1,column=1,sticky='nsew',padx=5,pady=5)
            self.Cancel      = tk.Button(self.QuestFrame,text='Cancel',command=self.PopupDestroy).grid(row=1,column=2,padx=5,pady=5,sticky='nsew')
          
        else:
            self.FileExist = False
            self.convert()
            
    def PopupDestroy(self): 
        try:
            
            self.QuestFrame.destroy()
        except:
            None 
        
    def Allow_Text_Copy(self,event):
        if(event.state==12 and event.keysym=='c' ):
            return
        else:
            return "break"        
    def CheckNameAvailable(self,*args):
        self.FileExist = path.isfile( self.save_location[0]+'\\'+self.OUTPUTNAME.get()+self.VideoInfo['format-in'])
        if self.FileExist == False:
            self.NameEntry.config(bg='lightgreen')
            self.NameChange.config(state='normal')
        if self.FileExist == True:
            self.NameEntry.config(bg='coral')
            self.NameChange.config(state='disabled')
        
    def CheckIfConvert(self):
        self.FileExist = path.isfile( self.save_location[0]+'\\'+self.OUTPUTNAME.get()+self.VideoInfo['format-in'])
        if self.FileExist == False:
            self.RunFinalCode = True   
            self.convert()
        
    def Toggle_Complex_Filter(self,*args):
        if self.Var_Complex.get() == True:
            self.Edit_Bitrate.config(state='normal')
            self.Edit_Format.config( state='normal')
            self.Edit_FPS.config(    state='normal')
            self.Edit_Width.config(  state='normal')
            self.Edit_Height.config( state='normal')
            #self.Edit_Scale.config(  state='normal')
                
        elif self.Var_Complex.get() == False:
            self.Edit_Bitrate.config(state='disabled')
            self.Edit_Format.config( state='disabled')
            self.Edit_FPS.config(    state='disabled')
            self.Edit_Width.config(  state='disabled')
            self.Edit_Height.config( state='disabled')
            #self.Edit_Scale.config(  state='disabled')
            
    def gcd(self,a, b):
        """The GCD (greatest common divisor) is the highest number that evenly divides both width and height."""
        return a if b == 0 else self.gcd(b, a % b)
                
    def convert(self):

        self.PopupDestroy()
        self.Var_Outputname.set(self.OUTPUTNAME.get())
        self.OUTPUT =  '\"'+self.save_location[0]+'\\'+self.OUTPUTNAME.get()+self.VideoInfo['format-in'][0]+'\"'
        
        if self.FFSel.get() in [FOP[4],FOP[10]]:
            self.OUTPUT =  '\"'+self.save_location[0]+'\\'+self.OUTPUTNAME.get()+'.gif'+'\"'
        if self.FFSel.get() in [FOP[6],FOP[9]]:
            self.OUTPUT =  '\"'+self.save_location[0]+'\\'+self.OUTPUTNAME.get()+'.mp4'+'\"'
        if len(self.file_paths) == 1:
            if self.FFSel.get() == FOP[0]: #Remove Video Footage Before Timetamp
                FFASTCMD = ['ffmpeg -y -i',
                            '\"'   + self.file_paths[0]  + '\"',
                            '-ss '+ self.Timestamp,
                            '-map 0 -vcodec copy -acodec copy',
                            self.OUTPUT]
                FFASTMSG = ['Removing the footage before the timestamp']
                REMOVELIST = None
            
            if self.FFSel.get() == FOP[1]: #Remove Video Footage After Timetamp
                FFASTCMD = ['ffmpeg -y -i',
                            '\"'   + self.file_paths[0]  + '\"',
                            '-ss '+ self.StartTime.get(),
                            '-map 0 -vcodec copy -acodec copy',
                            '-t '+ self.Timestamp,
                            self.OUTPUT]
                FFASTMSG = ['Removing the footage after the timestamp']
                REMOVELIST = None
            if self.FFSel.get() == FOP[2]: #Split Video at Timestamp
                OUTPUT1 = '\"'  + self.save_location[0]+'\\'+self.VideoInfo['name'][0]+'-A'+self.VideoInfo['format-in'][0]+'\"' 
                OUTPUT2 = '\"'  + self.save_location[0]+'\\'+self.VideoInfo['name'][0]+'-B'+self.VideoInfo['format-in'][0]+'\"'
                FFASTCMD = ['ffmpeg -y -i',
                            '\"'   + self.file_paths[0]  + '\"',
                            '-t ' + self.Timestamp,
                            '-map 0 -c copy ' +OUTPUT1,
                            '-ss ' + self.Timestamp, 
                            '-map 0 -c copy ' +OUTPUT2]
                FFASTMSG = ['Splitting the footage at the timestamp']
                REMOVELIST = None
            
            if self.FFSel.get() == FOP[3]: #Merge Multichannel Audio of Video
                if self.VideoInfo['audio streams'][0] > 1:
                    FFASTCMD = ['ffmpeg -y -i',
                                '\"'   + self.file_paths[0]  + '\"',
                                '-filter_complex \"[0:a:1]volume=0.8[l];[0:a:0][l]amerge=inputs='+str(self.VideoInfo['audio streams'][0])+'[a]\"',
                                '-map \"0:v:0\" -map \"[a]\" -c:v copy -c:a libmp3lame -q:a 3 -ac 2',
                                self.OUTPUT]
                    FFASTMSG = ['Merging Multichannel Audio']
                    REMOVELIST = None
               
                else:
                    self.Print_Console('You only have one audio channel, ya numpty - I mean, uh, I did it - Audio channel has been merged','warning')
                    E = Popen('echo You only have one audio channel, ya numpty - I mean, uh, I did it - Audio channel has been merged')
                    E.kill()
            
            if self.FFSel.get() == FOP[4]: #Convert Video to Gif
                #This is a two step process - First, we generate a palette:
                OUTPUT1 = '\"'  + self.save_location[0]+'\\'+'Palette.png'+'\"' 
                FFASTCMD = ([    'ffmpeg -y -i',
                                '\"'   + self.file_paths[0]  + '\"',
                                '-filter_complex \"fps=15,scale=720:-1:flags=lanczos,palettegen=stats_mode=diff:reserve_transparent=1\"',
                                OUTPUT1],
                             [    'ffmpeg -y -i',
                                '\"'   + self.file_paths[0]  + '\"',
                                '-i',OUTPUT1,'-filter_complex \"[0]fps=15,scale=720:-1:flags=lanczos,setsar=1[x];[x][1:v]paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle\"', 
                                self.OUTPUT])
                
                FFASTMSG   = ['Palette is being generated',
                              'Gif is being generated']
                REMOVELIST = [self.save_location[0]+'\\'+'Palette.png'] 
                
            if self.FFSel.get() == FOP[5]: #Convert Video to Image Sequence
                FFASTCMD = ['ffmpeg -y -i',
                            '\"'   + self.file_paths[0]  + '\"',
                            '\"'+self.save_location[0]+'\\'+self.OUTPUTNAME.get()+'%04d.png'+'\"' ]
                #'-vf \"select=eq(pict_type\,I)\" -vsync vfr',
                FFASTMSG   = ['Generating Image Sequence']
                REMOVELIST = None            
            if self.FFSel.get() == FOP[6]: #Convert Gif to Video
                FFASTCMD = ['ffmpeg -y -f gif -i',
                            '\"'   + self.file_paths[0]  + '\"',
                            self.OUTPUT]
                FFASTMSG   = ['Generating Video from Gif']
                REMOVELIST = None
            
            if self.FFSel.get() == FOP[7]: #Convert Gif to Image Sequence
                FFASTCMD = ['ffmpeg -y -i',
                            '\"'   + self.file_paths[0]  + '\"',
                            '-vsync 0',
                            '\"'+self.save_location[0]+'\\'+self.OUTPUTNAME.get()+'%04d.png'+'\"' ]
                FFASTMSG   = ['Converting Gif to Image Sequence']
                REMOVELIST = None
        if len(self.file_paths) > 1:
            if self.FFSel.get() == FOP[8]: #Merge Videos
                self.MergeList()
                FFASTCMD = ['ffmpeg -y -f',
                            'concat -safe 0 -i',
                            '\"'+self.MListOUT+'\"', #Note: Mergelist CANNOT use these kinds of speech marks \"\"
                            '-c copy', 
                            self.OUTPUT]
                FFASTMSG   = ['Merging Video From Mergelist']
                REMOVELIST = [self.MListOUT]
     
            if self.FFSel.get() == FOP[9]: #Convert Image Sequence to Video
                self.MergeList()
                FFASTCMD = ['ffmpeg -y -f concat -safe 0 -i',
                            '\"'+self.MListOUT+'\"', #Note: Mergelist CANNOT use these kinds of speech marks \"\"
                            '-vcodec libx264 -b:v 800k', 
                            self.OUTPUT]
                FFASTMSG   = ['Merging Video from Image Mergelist']
                REMOVELIST = [self.MListOUT]
                
            if self.FFSel.get() == FOP[10]: #Convert Image Sequence to Gif
                self.MergeList()
                #ffmpeg -i cropped/%02d.png -vf palettegen palette.png
                OUTPUT1 = '\"'  + self.save_location[0]+'\\'+'Palettevid.mp4'+'\"' 
                OUTPUT2 = '\"'  + self.save_location[0]+'\\'+'Palette.png'+'\"'  
                #This is incredibly stupid, we have to generate a palette from a converted video - AND THEN generate the gif using said palette
                FFASTCMD = (['ffmpeg -y -f concat -safe 0 -i',
                              '\"'+self.MListOUT+'\"',
                              '-vcodec libx264 -b:v 800k', 
                              OUTPUT1], #make palettevid
                             ['ffmpeg -y -i',
                              OUTPUT1,
                              '-filter_complex \"fps=24,scale=-1:640,crop=ih:ih,setsar=1,palettegen=stats_mode=diff:reserve_transparent=1\"',
                              OUTPUT2], #make palette from palette video
                             ['ffmpeg -y -f concat -safe 0 -i',
                              '\"'  + self.MListOUT  + '\"',
                              '-i',OUTPUT2,'-filter_complex \"[0]fps=24,setsar=1[x];[x][1:v]paletteuse\"', 
                              self.OUTPUT]) #use palette to make gif
                
                FFASTMSG   = ['Palette video is being generated',
                              'Palette is being generated',
                              'Gif is being generated']
                REMOVELIST = [self.save_location[0]+'\\'+'Palette.png',
                              self.save_location[0]+'\\'+'Palettevideo.mp4',
                              self.MListOUT]
                
        if self.RunFinalCode == True:
               print(FFASTCMD)
               print(FFASTMSG)
               self.RunFFMPEG(FFASTCMD,FFASTMSG,REMOVELIST)
               self.RunFinalCode = False
                
    def RunFFMPEG(self,CMD,MSG,REMOVELIST):
           if type(CMD[0]) == list:
                  Cmdmsg = []
                  for txt in CMD:
                         Cmdmsg.append(" ".join(txt)+'/n')
           elif type(CMD[0]) == str:
                  Cmdmsg = [" ".join(CMD)]
                  CMD = [CMD]       
           if len(Cmdmsg) != len(MSG):
                  self.Print_Console('Something is wrong, number of commands and messages are not equal...','warning')
                  pass
           elif len(Cmdmsg) == len(MSG):
                  for i in range(len(CMD)):
                        print(" ".join(CMD[i]))
                        self.H = Popen(" ".join(CMD[i]), shell=False)
                        self.PollKill(self.H,MSG[i])
                  self.Print_Console('Executed code:\n'+" ".join(Cmdmsg),'SettingsChange')
                  
                  if REMOVELIST == None:
                         self.Print_Console('Removed No Files','VideoInfo')
                  elif type(REMOVELIST) !=list:
                         self.Print_Console('REMOVELIST was not a list, so I guess I removed no files...','warning')
                  elif type(REMOVELIST) == list:
                         for File in REMOVELIST:
                                remove(File)
                         self.Print_Console('Removed the following Files:'+", ".join(REMOVELIST),'VideoInfo')
                         
                                              
                  
           
    def close(self):
        self.Print_Console('Bye!','normal')
        root.destroy()
    #%% REPLACE FORMAT IN WITH IMGLIST HERE!!!
    def MergeList(self):
        self.MListOUT = self.save_location[0]+'\\'+'MergeList.txt'
        if self.VideoInfo['format-in'][0].lower() in ImgFormat:
            FList    = ['file \''+self.SelFiles.get(0,'end')[n]+'\' \n duration 0.03333333333 \n' for n in range(len(self.SelFiles.get(0,'end')))] 
        else:
            FList    = ['file \''+self.SelFiles.get(0,'end')[n]+'\' \n' for n in range(len(self.SelFiles.get(0,'end')))]
        MergeList = open(self.MListOUT, "w")
        MergeList.write("".join(FList))
        MergeList.close()
    
    def PollKill(self,Process,Message):
        while Process.poll() is None:
            self.Print_Console(Message,'normal')
            sleep(1)
        Process.kill()
   
    def DD_Format_Gen(self):
        #Defining StringVar for Options Menu
        self.Var_Format = tk.StringVar(root);  self.Var_Format.set(OUTFORMAT[VSAV['Output Type']][0])
        #Generating Dropdown Menu
        self.Edit_Format = tk.OptionMenu(self.AddCanv, self.Var_Format, *OUTFORMAT[VSAV['Output Type']])
        self.Edit_Format.grid(row = 6, column =3,sticky='nswe')
        self.Edit_Format.config(width = 6, bg=ButtonBG,activebackground =ButtonABG)
        self.Edit_Format["menu"].config(bg=ButtonABG)
        if self.Var_Complex.get() == False:
            self.Edit_Format.config(state = 'disabled')
   
    def Window_Exit_Event(self):
        #if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
        json.dump(VSAV, open("SessionRestore.dat",'w'))
        root.destroy()
        sys.exit()
    
        
    def FF_Maker(self):
        if self.VideosLoaded != 'None':
            self.OUTPUT =  '\"'+self.save_location[0]+'\\'+self.Var_Outputname.get()+self.VideoInfo['format-in'][0]+'\"'
            if self.FFSel.get() in [FOP[4],FOP[10]]:
                self.OUTPUT =  '\"'+self.save_location[0]+'\\'+self.Var_Outputname.get()+'.gif'+'\"'
            if self.FFSel.get() in [FOP[9]]:
                self.OUTPUT =  '\"'+self.save_location[0]+'\\'+self.Var_Outputname.get()+'.mp4'+'\"'
         
            ENTRY = 'ffmpeg -y'
       
       
            if self.Var_FPS.get() != '' and self.Var_Format == '.gif':
                PARAM = '-r'+self.Var_FPS
            else:
                PARAM = ''
         
         
            #Single or Multi-File operation selector
            if self.VideosLoaded == 'Single':
                INFILE = '-i ' + '\"'   + self.file_paths[0]  + '\"'
            elif self.VideosLoaded != 'Multi':
                self.MergeList()
                INFILE = '-f concat -safe 0 i ' + '\"'  + self.MListOUT  + '\"'
         
            #We need to consider: 1 - Video in -> Video Out, 2 - Video in -> Multiple Videos Out
            #                   3 - Video in -> Gif Out,   4 - Gif in -> Video Out
            
            if self.VideoInfo['format-out'].lower() in ['.gif','.apng']:
                if self.VideoInfo['format-in'][0].lower() in VidFormat:
                    PALFILT = '-filter_complex \"fps=24,scale=-1:640,crop=ih:ih,setsar=1,palettegen=stats_mode=diff:reserve_transparent=1\"'
                    PALOUT  = '\"'  + self.save_location[0]+'\\'+'Palette.png'+'\"'                  
                    self.FF_PaletteGen  = " ".join([ENTRY,PARAM,INFILE,PALFILT,PALOUT]) 
                    GIFFILT = '-filter_complex \"[0]fps=24,setsar=1[x];[x][1:v]paletteuse\"'
                    GIFOUT  = self.OUTPUT
                    self.FF_Palette2Gif = " ".join([ENTRY,PARAM,INFILE,'i',PALOUT,GIFFILT,GIFOUT])    
                    print(self.FF_PaletteGen)
                    print(self.FF_Palette2Gif)

                elif self.VideoInfo['format-in'][0].lower() in ImgFormat:
                
                    gfps      = 'fps='   + self.Var_FPS.get()
                    gscale    = 'scale=' + self.Var_Width.get()+':'+self.Var_Height.get()
                    gaspect   = 'setsar=1'
                    gpalgen   = 'palettegen='
                    gstatmode = 'stats_mode='
                    PALFILT   = '-filter_complex \"fps=24,scale=-1:640,crop=ih:ih,setsar=1,palettegen=stats_mode=diff:reserve_transparent=1\"'
                    PALOUT    = '\"'  + self.save_location[0]+'\\'+'Palette.png'+'\"'                  
                    self.FF_PaletteGen  = " ".join([ENTRY,PARAM,INFILE,PALFILT,PALOUT]) 
                    GIFFILT = '-filter_complex \"[0]fps=24,setsar=1[x];[x][1:v]paletteuse\"'
                    GIFOUT  = self.OUTPUT
                    self.FF_Palette2Gif = " ".join([ENTRY,PARAM,INFILE,'i',PALOUT,GIFFILT,GIFOUT])
                    print(self.FF_PaletteGen)
                    print(self.FF_Palette2Gif)
                elif self.VideoInfo['format-out'] in VidFormat:
                    if self.VideoInfo['format-in'][0].lower() in VidFormat:
                        vidfilt  = ''
                        audfilt  = ''
                        #Audio merge and vol filter "[0:a:1]volume=0.8[l];[0:a:0][l]amerge=inputs='+str(self.VideoInfo['audio streams'])+'[a]\"'
                        FILTER   = vidfilt+audfilt
                        
                        allmap   = '-map 0'
                        vidmap   = '' 
                        audmap   = ''
                        MAP      = allmap+vidmap+audmap
                
                        COPYALL = True
                        if COPYALL == True:
                            allcopy  =  '-c copy'
                            videoenc = ''
                            audenc   = ''
                        if COPYALL == False:
                            allcopy  =  ''
                            vidcodec =  '-vcodec libx264'
                            videoenc =  '-c:v'+vidcodec
                            audenc   =  ''
                        COPYENC  = allcopy+videoenc+audenc
                        OUTPUT   = self.OUTPUT
                        self.FF_IN2VID = " ".join([ENTRY,PARAM,INFILE,FILTER,MAP,COPYENC,OUTPUT])
                        print(self.FF_IN2VID)
#Entry+PARAM+SingleFile+FILTER+MAP+CopyEnc+Output
"""
    GENERAL:
    All begin with:
    Entry     = 'ffmpeg -y'
    If GIF, then optionally we can add:
    PARAM  = '-r FPS'
    Then we can have: single file = 2 only, path is target | 1+2 is multi-file, where path = mergelist
    SingleFile   = 'i',path
    FileConcat   = {'-f concat -safe 0 '}   +   'i',path
    1: ---concat----    | 2: --- input ---    |  
    Then, we have some rules:
    it goes:
    for video out from path or mergelist
    1)FILTER  = filter_complex+"Options" # No palette - Video Files
      MAP     = {-map 0} "for all"  or {-map ":video:"  -map ":audio:"} "for selective"
      Copyenc = {-c copy} "for all" or {-c:v copy c:a copy} "for selective"
      ->output
    gif with mergelist
    2) ->filter_complex+"Options" #Generating Palette
->outputpalette.png
    3) ->'-i palette.png filter_complex+"Options"'
->output
    
    We build up components based on OUTPUT:
    If Video Output:
    
    Entry+PARAM+SingleFile+FILTER+MAP+CopyEnc+Output
    PARAM and FILTER can be empty
    FILTER  = 'filter_complex'+FLTROPT
    FLTROPT = filter1+filter2+filter3+filter4+filter5
    if palettegen: 
    FLTROPT = \"fps=15,scale=720:-1:flags=lanczos,palettegen=stats_mode=diff:reserve_transparent=1\"'
     = FPS+':'+SCALE+':'+FLAGS+','+'palettegen'+PTStatmode+':'PTTransp
     
    MAP = allmap + vidmap + audmap
    where allmap  = '-map 0' if vidmap and audmap are empty
    audmap must be set automatically if complex filter for multichannel is used
    CopyEnc = allenc + venc + aenc
    allenc = '-c copy' if venc and aenc are empty
    venc = '-c:v ' + outformatenc #based on output format
    aenc = '-c:a ' + audioenc     #based on some stuff 
    
    NOTE: '-map 0 -vcodec copy -acodec copy' = 'map 0 -c copy' i.e. map all, codec all copy
    => any case where you are explicitly copying ALL channels, you can just use '-map 0 -c copy'
    When you want to convert/reencode the video/audio channel, you can specify:
     -c:v videncoder and -c:a audencoder 
     if you want to select specific streams, or merge streams, you can use:
     -map "0:v:0" -map "[a]"
    """    
        
root = tk.Tk()

FGUI = FFAST_MPEGUI(root)
root.protocol("WM_DELETE_WINDOW", FGUI.Window_Exit_Event)
root.mainloop()

