You are a performance engineer profiling a particle physics simulation. The simulation has been exhibiting non-reproducible results and sudden numerical explosions due to floating-point reduction order issues when calculating system variance.

We have a video recording of the simulation's visual output during a crash run, located at `/app/particle_sim.mp4`. 

Your task consists of two parts:

Part 1: Isolate the Instability
The simulation visualizer maps particle density to pixel intensity. When the numerical explosion occurs, a large portion of the screen flashes pure white (RGB: 255, 255, 255). 
1. Extract the frames of `/app/particle_sim.mp4` (you may use `ffmpeg`, which is preinstalled).
2. Analyze the frames to find the 0-indexed frame number where the simulation first "explodes". We define an explosion as the first frame where strictly more than 5% of the total pixels are pure white `[255, 255, 255]`.
3. Write this exact integer (the frame index) to `/home/user/explosion_frame.txt`.

Part 2: Implement a Stable Reduction Utility
To fix the simulation's core numerical stability testing routines, we need a robust, order-independent way to compute the sample variance of particle energies. Standard naive variance formulas suffer from catastrophic cancellation.
1. Write a Python script at `/home/user/stable_var.py`.
2. The script must accept an arbitrary number of floating-point values passed as command-line arguments (e.g., `python3 stable_var.py 1.5 2.3 0.9 -1.2`).
3. The script must compute the sample variance (using Bessel's correction, N-1) of these numbers using exactly **Welford's online algorithm**.
4. The script should print only the final sample variance formatted to exactly 6 decimal places (e.g., `1.234567`). If fewer than 2 arguments are provided, it should print `0.000000`.
5. Your script must be strictly functionally equivalent to our internal oracle, handling positive and negative floats accurately without intermediate precision loss.