You are tasked with cleaning and preparing a dataset extracted from a video experiment.

We have recorded the motion of a highly fluorescent red object (RGB: 255, 0, 0) on a purely black background. The video is located at `/app/data/experiment.mp4`. 

Your objectives are:
1. **Trajectory Extraction**: Parse the video frame by frame. In each frame, locate the centroid `(x, y)` of the red object in pixels (where `(0,0)` is the top-left corner). Save these coordinates as a JSON array of `[x, y]` pairs to `/home/user/trajectory.json` in the exact order of the frames.

2. **Data Cleaning & Tokenization Script**: We need a reusable script to process this kind of trajectory data. Create a script at `/home/user/transform.py` that accepts two command-line arguments: an input JSON file path and an output text file path.
   The script must perform the following operations sequentially on the input array of `[x, y]` coordinates:
   - **Smoothing**: Apply a causal moving average with a window size of 3. Specifically, for a point at index `i`, its smoothed value is the average of the points at indices from `max(0, i-2)` to `i` (inclusive).
   - **Centering**: Calculate the global mean `(mean_x, mean_y)` of the *smoothed* points. Subtract this mean from every smoothed point.
   - **Tokenization**: Map each centered point `(x, y)` to a discrete state token:
     - `A` if $x \ge 0$ and $y \ge 0$
     - `B` if $x < 0$ and $y \ge 0$
     - `C` if $x < 0$ and $y < 0$
     - `D` if $x \ge 0$ and $y < 0$
   - Write the resulting tokens as a continuous string (e.g., `AABBCDA...`) to the specified output file.

3. **Execution & Visualization**: 
   - Run your `/home/user/transform.py` script on `/home/user/trajectory.json` and save the output to `/home/user/video_tokens.txt`.
   - Create a plot of the centered points (after smoothing and centering, but before tokenization) from the video data, and save it as `/home/user/centered_plot.png`. *Note: Our headless server often produces blank or failing plots if the plotting library's backend is not configured properly for a headless environment.*

Make sure your `transform.py` strictly follows the mathematical rules described, as it will be rigorously tested against an automated oracle with random input vectors to ensure absolute behavioral equivalence.