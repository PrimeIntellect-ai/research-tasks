You are a data scientist tasked with modeling a discrete dynamical system from experimental observations.

We have recorded the horizontal movement of a high-temperature particle in a 1D containment field. The recording is available at `/app/experiment.mp4`. The video is exactly 50 frames long (at 10 fps). Each frame is 100x10 pixels. In each frame, there is exactly one white pixel (value 255) representing the particle, while the rest of the background is black (0). The x-coordinate of this white pixel (0-indexed, from the left) represents the particle's position $x_t$ at frame $t$ (where $t=0, 1, \dots, 49$).

Your objectives are:

1. **Data Extraction:** Extract the $x_t$ positions from `/app/experiment.mp4` for all 50 frames. You may use `ffmpeg` and `imagemagick` (e.g., converting to `.txt` format) to script the extraction.

2. **Model Fitting:** The system is known to be governed by a discrete, modular second-order recurrence relation (due to the wrapping nature of the containment field):
   $$x_{t} = (A \cdot x_{t-1} + B \cdot x_{t-2} + C) \pmod{101}$$
   You must formulate and solve the linear/nonlinear equations to find the exact integer parameters $A$, $B$, and $C$. You can write a small C program to test combinations, perform a discrete optimization (like a genetic algorithm or brute-force gradient), or solve the system of equations directly using the first few frames of data.

3. **Predictor Implementation:** Write a C program in `/home/user/predictor.c` and compile it to an executable at `/home/user/predictor`. 
   The program must take exactly three command-line arguments: $x_0$, $x_1$, and the number of steps $N$.
   It must compute and print the predicted position $x_N$ using the parameters $A, B, C$ you found.
   
   Usage example:
   `./predictor <x_0> <x_1> <N>`
   Output: Just the integer $x_N$ followed by a newline.

Your compiled `/home/user/predictor` will be rigorously fuzzed against a hidden reference oracle to ensure absolute mathematical equivalence. Ensure your recurrence handles integer arithmetic precisely.