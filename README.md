# FFAST-MPEG
 A really "inefficient" (Just the frame preview, really), but non-commandline, quick-fix tool for editing videos in simple ways. **A list of currently supported FFMPEG operations, and what I am currently working on, can be found at the end of the readme.** Most video->video operations are not going to require re-encoding (making it lightning fast to use) but some (like making gifs, and creating image sequences) will require some.

Right now, FFMPEG is used to dump an image buffer into a numpy array, which is then fed into... Matplotlib's imshow. I know it's not a very elegant solution, but it is the only solution that I could think of. It works, at least.

Please keep in mind that this is a really early WIP. But feel free to contribute, and make changes. I'll likely be accepting any pull requests - no matter how small the feature. Just give me a good summary :)

![The appearance of the Editor in version v0.1](https://raw.githubusercontent.com/DeltaMod/FFAST-MPEG/master/FFAST-MPEG.PNG)
![The planned appearance of the Editor for version whatever.](https://raw.githubusercontent.com/DeltaMod/FFAST-MPEG/master/FFAST-MPEG-Layout.png)

**Currently doing**
  * Implementnig Video to Gif conversion. Since we need to create a palette before we create the gif, this is a two step operation. Thus, I will need to figure out how to check if a subprocess has completed before moving onto the next step.
  
  **I was unable to find a good method to intercept the CMD output, since using H.communicate() will kill the command. Thus, I will instead have python intercept when the program automatically names the "OUTPUT", and see if it matches a file. If it does, the user will be given the option to either manually rename the file, overwrite the current one or stop the process.** 
  
**Planned Features**

 * Single Video Operations

       - "Remove Video Footage Before Timetamp" [DONE]
       
       - "Remove Video Footage After Timetamp", [DONE]
       
       - "Split Video at Timestamp",            [DONE]
       
       - "Merge Multichannel Audio of Video",   [DONE]
       
       - "Convert Video to Gif", [1/2Done] (needs to wait for subprocess to complete)
       
       - "Convert Video to Image Sequence",
       
       - "Convert Gif to Video",
       
       - "Convert Gif to Image Sequence", 

* Multi Video Operation

        - "Merge Videos",
        
        - "Convert Image Sequence to Video",
        
        - "Convert Image Sequence to Gif"
        
* General Operations:
 
        - Automatic Naming for Image Sequences
 
        - Automatically deleting original videos after trimming
 
        - Automatically deleting original videos after merging
        
        - Dynamically adding complex filters?
        
        - Adding gif conversion parameters when that option is selected (e.g. encoding quality, framerate, interpolation quality, etc)
        
        - Adding image sequence to gif/video parameters (like encoding quality, framerate, interpolation quality, etc.
  
