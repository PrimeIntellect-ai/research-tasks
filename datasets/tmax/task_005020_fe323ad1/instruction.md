You are a performance engineer analyzing the power characteristics of a new high-frequency trading server. You have two main objectives: analyzing a diagnostic video to find when the system achieves thermal and computational stability, and writing a fast data stream processor in Bash for live profiling.

**Part 1: Video Signal Analysis**
You have been provided with a high-speed video of the server's diagnostic LED matrix during a stress test: `/app/led_strobe.mp4`. 
The brightness of the LED corresponds to the CPU's power draw. The application goes through an initial noisy initialization phase (rapid flashing), followed by a sudden convergence to a stable state (low, steady power draw).

Using tools like `ffmpeg` and any image processing utilities you prefer (e.g., Python scripts, ImageMagick), analyze the video frame by frame.
1. Extract the frames and compute the average grayscale pixel intensity for each frame.
2. Determine the *first frame index* (0-indexed, where the first frame of the video is 0) where the system stabilizes. We define "stabilization" as the first frame where the average pixel intensity drops below 10.0 and remains strictly below 10.0 for at least 15 consecutive frames.
3. Write this single integer frame index to `/home/user/stable_frame.txt`.

**Part 2: Bash Stream Integrator**
To profile the system live without deploying heavy frameworks, you must write a pure Bash script (using standard CLI tools like `awk`, `bc`, etc.) to filter and integrate live power readings.

Create a script at `/home/user/stream_integrator.sh` that reads floating-point numbers from standard input (one per line) and prints processed values to standard output. 
For each incoming value $x_t$ (where $t = 1, 2, 3, \dots$ represents the line number):
1. Apply a 3-point simple moving average to calculate the smoothed signal $S_t$. 
   * $S_t = (x_t + x_{t-1} + x_{t-2}) / 3$
   * For the first point, $S_1 = x_1$.
   * For the second point, $S_2 = (x_1 + x_2) / 2$.
2. Compute the cumulative numerical integral $I_t$ using the trapezoidal rule, assuming a time step $\Delta t = 0.1$.
   * $I_1 = 0.0000$
   * For $t > 1$: $I_t = I_{t-1} + \Delta t \times \frac{S_t + S_{t-1}}{2}$
3. Print $I_t$ to stdout immediately after processing each line, formatted to exactly 4 decimal places (e.g., `0.0000`, `0.1500`, `-0.0421`).

Your script will be tested against a compiled oracle for exact output equivalence using randomly generated streams of floats. Your script must be executable (`chmod +x`).