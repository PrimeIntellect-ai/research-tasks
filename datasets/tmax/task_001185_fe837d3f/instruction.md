You are a machine learning engineer preparing training data from a video of a physical experiment. You need to extract a specific signal from the video and write an analysis tool in C to process it. 

Your tasks are:

1. **Extract Signal from Video**
You have a grayscale video at `/app/experiment.mp4`. The video is strictly 64x64 pixels. Extract the mean pixel luminance (grayscale value) for each frame in chronological order. 
Save these values as text (one decimal value per line) to `/home/user/frame_means.txt`. (Hint: you can use `ffmpeg` to output raw video bytes and process them, or use `ffprobe`/`ffmpeg` filters).

2. **Implement Analysis Tool in C**
Write a C program at `/home/user/analyze.c` that reads a sequence of `double` precision floating-point numbers from standard input (separated by whitespace, up to 10000 values) until EOF. These represent the `y` values. The `x` values are their 0-based indices (0, 1, 2, ..., N-1).

The program must:
a. Compute the standard linear regression slope `m` and intercept `c` to fit `y = m*x + c`.
b. Estimate the 95% bootstrap confidence interval for the slope `m`. 
   - Perform exactly 1000 bootstrap iterations.
   - For each iteration, draw `N` samples from the `(x, y)` pairs *with replacement*. 
   - To draw a random index, use this exact pseudo-random number generator to ensure reproducibility:
     ```c
     uint32_t state = 42;
     uint32_t next_rand() {
         state = (state * 1103515245 + 12345) & 0x7FFFFFFF;
         return state;
     }
     ```
     The random index should be `next_rand() % N`. Draw the `N` samples in order (i=0 to N-1).
   - Compute the slope `m_boot` for this resampled dataset. (If all drawn `x` values are identical, set `m_boot = 0.0`).
   - Store the 1000 `m_boot` values and sort them in ascending order (e.g., using `qsort`).
   - The lower bound `m_lower` is the value at index 24 (the 25th smallest).
   - The upper bound `m_upper` is the value at index 974 (the 975th smallest).

c. Print the final results to standard output in exactly this format:
`m: %.4f, c: %.4f, m_lower: %.4f, m_upper: %.4f\n`

3. **Run the Pipeline**
Compile your program to `/home/user/analyze`.
Run your program with `/home/user/frame_means.txt` as input, and redirect the output to `/home/user/video_analysis.txt`.

**Verification Constraints:**
- Your C program's output must perfectly match an undisclosed reference implementation.
- We will fuzz-test your compiled `/home/user/analyze` executable with various hidden inputs to verify exact equivalence.