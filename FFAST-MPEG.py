# -*- coding: utf-8 -*-
"""
FFAST-MPEG - A quicker than usual way to make gifs, trim videos, split videos and so on!

Current Version: pre-alpha v0.6  
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
        "Convert Image Sequence to Gif"]
FOP = [str(n)+' - '+FOP[n] for n in range(len(FOP))]
FOPWidth = len(max(FOP, key=len))
VSAV = {'FFMPEG Mode':0}
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
        self.Convert_Button = tk.Button(self.AddCanv, text='Convert', command=self.Check_File_Exist)
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
        VINFOPROBE = ['ffprobe',
                     '-v error -select_streams v:0 -show_entries',
                     'stream=width,height,duration,bit_rate,r_frame_rate,channels -of default=noprint_wrappers=1',
                     '\"'+self.file_paths[0]+'\"']
        AINFOPROBE = ['ffprobe -v error -show_entries stream=codec_type -of default=noprint_wrappers=1 ',
                      '\"'+self.file_paths[0]+'\"']
        print(" ".join(AINFOPROBE))
        resultv = subprocess.Popen(" ".join(VINFOPROBE), shell=False,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        resulta = subprocess.Popen(" ".join(AINFOPROBE), shell=False,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        RAW = list(filter(None,resultv.communicate()[0].decode().split('\r\n')))
        print(RAW)
        INFO = [RAW[n].split('=') for n in range(len(RAW))]
        self.VideoInfo ={'format':'.'+self.file_paths[0].rsplit('.',1)[-1]}
        for i in range(len(INFO)):
            try:
                self.VideoInfo[INFO[i][0]] = eval(INFO[i][1])
                print(eval(INFO[i][1]))
            except NameError:
                self.VideoInfo[INFO[i][0]] = INFO[i][1]
        self.VideoInfo['audio streams'] = resulta.communicate()[0].decode().count('audio')
        #self.VideoInfo['video streams'] = resultv.communicate()[0].decode().count('video')
        print(self.VideoInfo['format'] ) #we add this for convenience, so we can construct names and file-extensions separately
        print(self.VideoInfo)
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
     
    def Check_File_Exist(self):
        self.OUTPUTNAME = tk.StringVar(root); self.OUTPUTNAME.set(self.VideoInfo['name']+'-'+FOPN[self.FFSel.get()])
        self.OUTPUTNAME.trace_add('write',self.CheckNameAvailable)
        self.FileExist = os.path.isfile( self.save_location[0]+'\\'+self.OUTPUTNAME.get()+self.VideoInfo['format'])
        print( self.FileExist)
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
    def CheckNameAvailable(self,*args):
        self.FileExist = os.path.isfile( self.save_location[0]+'\\'+self.OUTPUTNAME.get()+self.VideoInfo['format'])
        if self.FileExist == False:
            self.NameEntry.config(bg='lightgreen')
            self.NameChange.config(state='normal')
        if self.FileExist == True:
            self.NameEntry.config(bg='coral')
            self.NameChange.config(state='disabled')
    def CheckIfConvert(self):
        self.FileExist = os.path.isfile( self.save_location[0]+'\\'+self.OUTPUTNAME.get()+self.VideoInfo['format'])
        if self.FileExist == False:
            self.convert()
            
     #   YorRename = tk.simpledialog.askstring()
    def convert(self):
        self.PopupDestroy()
        self.OUTPUT =  '\"'+self.save_location[0]+'\\'+self.OUTPUTNAME.get()+self.VideoInfo['format']+'\"'
        if self.FFSel.get() in [FOP[4],FOP[10]]:
            self.OUTPUT =  '\"'+self.save_location[0]+'\\'+self.OUTPUTNAME.get()+'.gif'+'\"'
        if self.FFSel.get() in [FOP[9]]:
            self.OUTPUT =  '\"'+self.save_location[0]+'\\'+self.OUTPUTNAME.get()+'.mp4'+'\"'
        if len(self.file_paths) == 1:
            if self.FFSel.get() == FOP[0]: #Remove Video Footage Before Timetamp
                FFASTCMD = ['ffmpeg -y -i',
                            '\"'   + self.file_paths[0]  + '\"',
                            '-ss '+ self.Timestamp,
                            '-map 0 -vcodec copy -acodec copy',
                            self.OUTPUT]
                self.H = subprocess.Popen(" ".join(FFASTCMD),stdin = subprocess.PIPE,bufsize=-1, shell=False)
                print('oi, this is the output you want:')
                print(self.H.stderr)
                
            if self.FFSel.get() == FOP[1]: #Remove Video Footage After Timetamp
                FFASTCMD = ['ffmpeg -y -i',
                            '\"'   + self.file_paths[0]  + '\"',
                            '-ss '+ self.StartTime.get(),
                            '-map 0 -vcodec copy -acodec copy',
                            '-t '+ self.Timestamp,
                            self.OUTPUT]
                self.H = subprocess.Popen(" ".join(FFASTCMD), shell=False)
            if self.FFSel.get() == FOP[2]: #Split Video at Timestamp
                OUTPUT1 = '\"'  + self.save_location[0]+'\\'+self.VideoInfo['name']+'-A'+self.VideoInfo['format']+'\"' 
                OUTPUT2 = '\"'  + self.save_location[0]+'\\'+self.VideoInfo['name']+'-B'+self.VideoInfo['format']+'\"'
                FFASTCMD = ['ffmpeg -y -i',
                            '\"'   + self.file_paths[0]  + '\"',
                            '-t ' + self.Timestamp,
                            '-map 0 -c copy ' +OUTPUT1,
                            '-ss ' + self.Timestamp, 
                            '-map 0 -c copy ' +OUTPUT2]
                self.H = subprocess.Popen(" ".join(FFASTCMD), shell=False)
                
            if self.FFSel.get() == FOP[3]: #Merge Multichannel Audio of Video
               if self.VideoInfo['audio streams'] > 1:
                   FFASTCMD = ['ffmpeg -y -i',
                                '\"'   + self.file_paths[0]  + '\"',
                                '-filter_complex \"[0:a:1]volume=0.8[l];[0:a:0][l]amerge=inputs='+str(self.VideoInfo['audio streams'])+'[a]\"',
                                '-map \"0:v:0\" -map \"[a]\" -c:v copy -c:a libmp3lame -q:a 3 -ac 2',
                                self.OUTPUT]
                   self.H = subprocess.Popen(" ".join(FFASTCMD), shell=False)
                   
               else:
                   print('You only have one audio channel, ya numpty - I mean, uh, I did it - Audio channel has been merged')
                   E = subprocess.Popen('echo You only have one audio channel, ya numpty - I mean, uh, I did it - Audio channel has been merged')
                   E.kill()
            if self.FFSel.get() == FOP[4]: #Convert Video to Gif
                #This is a two step process - First, we generate a palette:
                OUTPUT1 = '\"'  + self.save_location[0]+'\\'+'Palette.png'+'\"' 
                FFASTCMDT = (['ffmpeg -y -i',
                            '\"'   + self.file_paths[0]  + '\"',
                            '-filter_complex \"fps=24,scale=-1:640,crop=ih:ih,setsar=1,palettegen\"',
                             OUTPUT1],
                            ['ffmpeg -y -i',
                             '\"'   + self.file_paths[0]  + '\"',
                             '-i',OUTPUT1,'-filter_complex \"[0]fps=24,setsar=1[x];[x][1:v]paletteuse\"', 
                             self.OUTPUT])
                
                self.H = subprocess.Popen(" ".join(FFASTCMDT[0]), shell=False)
                self.PollKill(self.H,'Palette is being generated')
                self.H = subprocess.Popen(" ".join(FFASTCMDT[1]), shell=False)
                self.PollKill(self.H,'Gif is being generated')
                os.remove(self.save_location[0]+'\\'+'Palette.png')
                
                FFASTCMD = FFASTCMDT[0]+FFASTCMDT[1]
            if self.FFSel.get() == FOP[5]: #Convert Video to Image Sequence
                FFASTCMD = ['ffmpeg -y -i',
                            '\"'   + self.file_paths[0]  + '\"',
                            '\"'+self.save_location[0]+'\\'+self.OUTPUTNAME.get()+'%04d.png'+'\"' ]
                #'-vf \"select=eq(pict_type\,I)\" -vsync vfr',
                self.H = subprocess.Popen(" ".join(FFASTCMD), shell=False)
                self.PollKill(self.H,'Generating Image Sequence')
                
            if self.FFSel.get() == FOP[6]: #Convert Gif to Video
                FFASTCMD = ['ffmpeg -y -f gif -i',
                            '\"'   + self.file_paths[0]  + '\"',
                            self.OUTPUT]
                self.H = subprocess.Popen(" ".join(FFASTCMD), shell=False)
                self.PollKill(self.H,'Generating Video From Gif')
                
            if self.FFSel.get() == FOP[7]: #Convert Gif to Image Sequence
                FFASTCMD = ['ffmpeg -y -i',
                            '\"'   + self.file_paths[0]  + '\"',
                            '-vsync 0',
                            '\"'+self.save_location[0]+'\\'+self.OUTPUTNAME.get()+'%04d.png'+'\"' ]
                self.H = subprocess.Popen(" ".join(FFASTCMD), shell=False)
                self.PollKill(self.H,'Converting Gif to Image Sequence')
                
        if len(self.file_paths) > 1:
            if self.FFSel.get() == FOP[8]: #Merge Videos
                self.MergeList()
                FFASTCMD = ['ffmpeg -y -f',
                            'concat -safe 0 -i',
                            '\"'+self.MListOUT+'\"', #Note: Mergelist CANNOT use these kinds of speech marks \"\"
                            '-c copy', 
                            self.OUTPUT]
                self.H = subprocess.Popen(" ".join(FFASTCMD), shell=False)
                self.PollKill(self.H,'Merging Videos From Mergelist')
                os.remove(self.MListOUT)
                
            if self.FFSel.get() == FOP[9]: #Convert Image Sequence to Video
                self.MergeList()
                FFASTCMD = ['ffmpeg -y -r 1/30 -f concat -safe 0 -i',
                            '\"'+self.MListOUT+'\"', #Note: Mergelist CANNOT use these kinds of speech marks \"\"
                            '-c:v libx264 -r 25 -pix_fmt yuv420p -t 15', 
                            self.OUTPUT]
                self.H = subprocess.Popen(" ".join(FFASTCMD), shell=False)
                self.PollKill(self.H,'Merging Videos From Mergelist')
               # os.remove(self.MListOUT)
            if self.FFSel.get() == FOP[10]: #Convert Image Sequence to Gif
                print('Not Available Yet')
    
            
                        
            print('Executed code:\n'+" ".join(FFASTCMD))
    
    def close(self):
        print('Bye!')
        root.destroy()
        
    def MergeList(self):
        self.MListOUT = self.save_location[0]+'\\'+'MergeList.txt'
        FList    = ['file \''+self.SelFiles.get(0,'end')[n]+'\' \n' for n in range(len(self.SelFiles.get(0,'end')))] 
        MergeList = open(self.MListOUT, "w")
        MergeList.write("".join(FList))
        MergeList.close()
        
    def PollKill(self,Process,Message):
        while Process.poll() is None:
                    print(Message)
                    time.sleep(1)
        Process.kill()

root = tk.Tk()

FFASTGUI = FFAST_MPEGUI(root)
root.mainloop()

