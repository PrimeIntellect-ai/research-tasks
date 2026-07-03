You are acting as a bioinformatics analyst studying the population dynamics of sequence variants in a bioreactor. You need to accomplish two tasks: extract the duration of a specific reaction phase from an experimental video, and write a numerical ODE solver in C to simulate the sequence's growth.

**Part 1: Video Analysis**
We have recorded a bioreactor experiment, available at `/app/cell_timelapse.mp4`. 
During the "reaction phase", a distinct pure green square (RGB: 0, 255, 0) of size 10x10 pixels appears in the absolute top-left corner of the video.
Use tools like `ffmpeg` to extract the frames and determine exactly how many frames contain this green indicator. This count of frames will be the total time `T` (in arbitrary time units) for your simulation.

**Part 2: ODE Simulation in C**
Write a C program in `/home/user/simulate_growth.c` and compile it to `/home/user/simulate_growth`.
The program must take exactly two command-line arguments:
1. `sequence_length` (integer, `L`)
2. `initial_concentration` (double, `y0`)

It must simulate the population concentration `y` over time `t` using the logistic growth equation modified by sequence length penalty:
`dy/dt = a * y * (1.0 - y / K) - b * L * y`

Where:
- `a = 0.5` (growth rate)
- `K = 100.0` (carrying capacity)
- `b = 0.001` (length penalty factor)
- `L` is the `sequence_length` from the first argument.

Simulation Requirements:
- Initial condition: `y(0) = y0`
- Use the classic 4th-order Runge-Kutta (RK4) method.
- Use a strictly fixed step size `dt = 0.01`.
- Simulate from `t = 0` to `t = T`, where `T` is exactly the integer number of frames you found in Part 1 (treated as a double precision time, e.g., if you found 50 frames, simulate to `t = 50.0`). Ensure the number of steps is exactly `T / 0.01`.
- Output ONLY the final concentration `y(T)` to standard output, formatted to exactly 6 decimal places (e.g., using `printf("%.6f\n", y_final)`). No other text.

Ensure your C program is robust and compiles correctly without warnings. Your program's output must match our reference implementation bit-for-bit for a variety of inputs.