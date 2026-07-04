You are acting as a data science assistant for a researcher organizing microscopy datasets. 

We have a video of a droplet experiment where a microscope records at 10 frames per second. Unfortunately, the sensor occasionally drops data, resulting in corrupted frames (which have missing values represented by large patches of pure black/0-value pixels) or laser failures (which are abnormally dark outliers).

You need to create a C program to act as a classifier that rejects these corrupted/outlier frames, verify it against our labeled corpora, and then apply it to a new raw video.

Here are your instructions:

1. **Write a C-based Detector**
   Write a C program at `/home/user/detector.c` and compile it to `/home/user/detector`.
   - The program should accept a single command-line argument: the path to a grayscale PGM (Portable Gray Map) image file.
   - It must read the PGM file and implement a statistical thresholding model (e.g., checking for excessive pure black pixels or very low average brightness) to classify the frame.
   - It must exit with code `0` if the frame is "clean" (usable).
   - It must exit with code `1` if the frame is "evil" (corrupted/outlier).

2. **Verify Against the Corpora**
   We have provided a set of known good and bad frames to test your detector:
   - Clean frames: `/app/corpus/clean/` (contains `.pgm` files)
   - Evil frames: `/app/corpus/evil/` (contains `.pgm` files)
   Your `/home/user/detector` must correctly return exit code 0 for *all* files in the clean directory, and exit code 1 for *all* files in the evil directory. Adjust your logic until you achieve 100% accuracy on these corpora.

3. **Process the New Video**
   Once your detector is verified:
   - Extract the frames from the video located at `/app/droplet_experiment.mp4` as grayscale PGM files at a rate of 1 frame per second (`fps=1`).
   - Run your `/home/user/detector` on every extracted frame.
   - Count the total number of **clean** frames in the video.
   - Write this single integer count to `/home/user/clean_count.txt`.

Ensure your C code handles the PGM format parsing correctly (P5 binary or P2 plain text, depending on what ffmpeg outputs by default, but typically `ffmpeg -i ... %04d.pgm` produces P5). The tools `ffmpeg` and `gcc` are already installed.