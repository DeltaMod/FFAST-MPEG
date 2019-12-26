# FFAST-MPEG: Beta v1.0 - THE EXPANSION
 A really "inefficient" (Just the frame preview, really), but non-commandline, quick-fix tool for editing videos in simple ways. **A list of currently supported FFMPEG operations, and what I am currently working on, can be found at the end of the readme.** Most video->video operations are not going to require re-encoding (making it lightning fast to use) but some (like making gifs, and creating image sequences) will require some.

Right now, FFMPEG is used to dump an image buffer into a numpy array, which is then fed into... Matplotlib's imshow. I know it's not a very elegant solution, but it is the only solution that I could think of. It works, at least.
Addendum: I know that you can call ffplay to get full playback of the video,  but I cannot think of a way to get that to emb inside of tkinter. Perhaps I will add a feature that sets playback to the selected region

Please keep in mind that this is a really early WIP. But feel free to contribute, and make changes. I'll likely be accepting any pull requests - no matter how small the feature. Just give me a good summary :)

Requirements:
You will need to install FFMPEG https://www.ffmpeg.org/download.html and add it to your PATH environment variable!

![The appearance of the Editor in version v0.1](https://raw.githubusercontent.com/DeltaMod/FFAST-MPEG/master/FFAST-MPEG.PNG)
![The planned appearance of the Editor for version whatever.](https://raw.githubusercontent.com/DeltaMod/FFAST-MPEG/master/FFAST-MPEG-Layout.png)

**Currently doing - The Expansion Pack**
  * This version has rewritten the file loading process, and allows for multi-file-first-frame previews, and thus will also allow for gif order previews when you intend to make a gif from image files. I had to rewrite the loading system, because I wanted to keep using ffmpeg to view the first frame, instead of using matplotlib's imshow, since this would have too much overhead, and would require switching from using ffmpeg to preview, and using imshow, which would be different for video files and image files.  
  

  
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
 
        - Automatic Naming for Image Sequences  [Done?]
        
        - Display first frame of each image/video imported instead of just from the first video/image when moving preview [DONE]
 
        - Automatically deleting original videos after performing an operation
        
        - Dynamically adding complex filters?    [Started]
        
        - Automatically importing volume control for multi-channel video, based on total number of channels available (to be incorporated into the automatic complex filter builder)
        
        - Set video range using overlapped sliders that hide/show when you toggle "start" and "end" points. Alternatively, add an end slider that can be interacted with at the same time? Note that the operation for trimming would actually be: Trim from end, then trim the newly trimmed video from start. Otherwise, you can lose sound sync.
        
        - Adding gif conversion parameters when that option is selected (e.g. encoding quality, framerate, interpolation quality, etc) [Started]
        
        - Adding image sequence to gif/video parameters (like encoding quality, framerate, interpolation quality, etc. [Started]
        
        - Adding overwrite/rename/cancel options when an automatically generated name is matching one in the same directory [DONE]
       
