# FFAST-MPEG
 A really inefficient, but non-commandline, quick-fix tool for editing videos in simple ways. Currently, it supports only trimming away the start of a video - but I intend to expand it to be capable of handling more tasks (many that are already listed in the software)

Currently, FFMPEG is used to dump an image buffer into a numpy array, which is then fed into... Matplotlib's imshow. I know it's not a very elegant solution, but it is the only solution that I could think of. It works, at least.

Please keep in mind that this is a really early WIP. But feel free to contribute, and make changes. I'll likely be accepting any pull requests - no matter how small the feature. Just give me a good summary :)

![The appearance of the Editor in version v0.1](https://raw.githubusercontent.com/DeltaMod/FFAST-MPEG/master/FFAST-MPEG.PNG)
![The planned appearance of the Editor for version whatever.](https://raw.githubusercontent.com/DeltaMod/FFAST-MPEG/master/FFAST-MPEG-Layout.png)

Planned Features Include:
-Single Video Operations

       "Remove Video Footage Before Timetamp" [DONE]
       
       "Remove Video Footage After Timetamp", [DONE]
       
       "Split Video at Timestamp",            [DONE]
       
       "Merge Multichannel Audio of Video",   [DONE]
       
       "Convert Video to Gif",
       
       "Convert Video to Image Sequence",
       
       "Convert Gif to Video",
       
       "Convert Gif to Image Sequence", 

-Multi Video Operation

        "Merge Videos",
        
        "Convert Image Sequence to Video",
        
        "Convert Image Sequence to Gif"
        
 -General Operations:
 
        Automatic Naming for Image Sequences
 
        Automatically deleting original videos after trimming
 
        Automatically deleting original videos after merging
        
        Dynamically adding complex filters?
  
