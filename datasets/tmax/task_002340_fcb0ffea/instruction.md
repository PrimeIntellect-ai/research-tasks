You are a Machine Learning Engineer preparing training data pipelines. We have a video asset `/app/raw_footage.mp4` and we need to extract statistical features from its frames to train a lightweight classification model.

Your task is to write a standalone C program that computes a reduced-dimensionality embedding of a frame and applies a bootstrap sampling method to estimate the robust mean and variance bounds of the embedding features. 

**Step 1: The C Feature Extractor**
Write a C program at `/home/user/process_frame.c` and compile it to `/home/user/process_frame` (use `gcc -O3`).
The program must read exactly 4096 bytes from `stdin`, which represents a 64x64 raw grayscale image (8-bit pixels). 

The program must perform the following:
1. **Dimensionality Reduction (Pooling):** Divide the 64x64 image into 64 non-overlapping blocks of 8x8 pixels. The blocks should be processed in standard row-major order (i.e., the top 8 rows of the image contain the first 8 blocks from left to right, followed by the next 8 rows, etc.). Compute the average pixel value for each block as a `float`. You now have an embedding of 64 float values.
2. **Bootstrap Sampling:** We want to estimate the stability of this embedding. 
   - Calculate the sum of all 4096 byte values in the input image. Use this integer sum as the initial seed for a linear congruential generator (LCG). `unsigned int seed = total_sum;`
   - Generate 100 bootstrap samples. Each bootstrap sample consists of 64 values drawn *with replacement* from the 64 block averages.
   - To draw a single value, update the seed using the POSIX standard LCG formula: `seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF;`, then select the block index `seed % 64`.
   - Calculate the mean of the 64 drawn values for each bootstrap sample. You will have 100 bootstrap means.
3. **Output:** Calculate the minimum, maximum, and overall average of those 100 bootstrap means. 
   Print the result to `stdout` strictly in this format (using `%.4f`):
   `Min: [value], Max: [value], Avg: [value]\n`

**Step 2: Processing the Video**
Use standard bash CLI tools (like `ffmpeg`) to extract the video frame at exactly `00:00:02` from `/app/raw_footage.mp4`. 
Scale it to 64x64 pixels, convert it to raw grayscale (`gray` format, 8-bit), and pipe that raw binary data into your compiled `/home/user/process_frame` executable.
Redirect the standard output of your program to `/home/user/frame2_stats.txt`.

Ensure your C program robustly handles the standard input stream and calculates the indices correctly.