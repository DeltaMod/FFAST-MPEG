# FFAST-MPEG: Alpha v1.1
 A really "inefficient" (Just the frame preview, really), but non-commandline, quick-fix tool for editing videos in simple ways. **A list of currently supported FFMPEG operations, and what I am currently working on, can be found at the end of the readme.** Most video->video operations are not going to require re-encoding (making it lightning fast to use) but some (like making gifs, and creating image sequences) will require some.

Right now, FFMPEG is used to dump an image buffer into a numpy array, which is then fed into... Matplotlib's imshow. I know it's not a very elegant solution, but it is the only solution that I could think of. It works, at least.

Please keep in mind that this is a really early WIP. But feel free to contribute, and make changes. I'll likely be accepting any pull requests - no matter how small the feature. Just give me a good summary :)

Requirements:
You will need to install FFMPEG https://www.ffmpeg.org/download.html and add it to your PATH environment variable!

![The appearance of the Editor in version v0.1](https://raw.githubusercontent.com/DeltaMod/FFAST-MPEG/master/FFAST-MPEG.PNG)
![The planned appearance of the Editor for version whatever.](https://raw.githubusercontent.com/DeltaMod/FFAST-MPEG/master/FFAST-MPEG-Layout.png)

**Currently doing**
  * Taking a break - The current version does most tasks well enough, I just need to learn how to compile the software into something that isn't 800 MB
  

  
**Planned Features**

 * Single Video Operations

       - "Remove Video Footage Before Timetamp" [DONE]
       
       - "Remove Video Footage After Timetamp", [DONE]
       
       - "Split Video at Timestamp",            [DONE]
       
       - "Merge Multichannel Audio of Video",   [DONE]
       
       - "Convert Video to Gif",                [DONE]      
       
       - "Convert Video to Image Sequence",     [DONE]
       
       - "Convert Gif to Video",                [DONE] 
       
       - "Convert Gif to Image Sequence",       [DONE]

* Multi Video Operation

        - "Merge Videos",                       [DONE]
        
        - "Convert Image Sequence to Video",    [DONE]
        
        - "Convert Image Sequence to Gif"       [DONE]
        
* General Operations:
 
        - Automatic Naming for Image Sequences
 
        - Automatically deleting original videos after trimming
 
        - Automatically deleting original videos after merging
        
        - Dynamically adding complex filters?
        
        - Adding gif conversion parameters when that option is selected (e.g. encoding quality, framerate, interpolation quality, etc)
        
        - Adding image sequence to gif/video parameters (like encoding quality, framerate, interpolation quality, etc.
        
        - Adding overwrite/rename/cancel options when an automatically generated name is matching one in the same directory [DONE]
  
