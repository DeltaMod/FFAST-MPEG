# FFAST-MPEG
 A really inefficient, but non-commandline, quick-fix tool for editing videos in simple ways. Currently, it supports only trimming away the start of a video - but I intend to expand it to be capable of handling more tasks (many that are already listed in the software)

Currently, FFMPEG is used to dump an image buffer into a numpy array, which is then fed into... Matplotlib's imshow. I know it's not a very elegant solution, but it is the only solution that I could think of. It works, at least.
