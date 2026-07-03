You are a performance engineer tasked with creating an optimized PDE solver API for heat diffusion, driven by initial conditions extracted from experimental video footage. 

Your task has four main stages:

**1. Video Processing (Data Extraction)**
There is an experimental video at `/app/thermal_experiment.mp4`. 
- Extract exactly the 20th frame (0-indexed, or around 0.66 seconds assuming 30fps) using `ffmpeg` or any suitable tool.
- Convert this frame to grayscale. Calculate the average pixel intensity (0-255). Let this integer value be `T_init`. You may use a short Python or bash script to compute this, but the downstream simulation engine must be written in C.

**2. Simulation Engine (C Implementation)**
Write a C application that simulates 1D heat diffusion using an implicit finite difference method, which requires solving a tridiagonal matrix system (LU decomposition / Thomas algorithm).
- The spatial domain has 100 points, `dx = 0.1`, `dt = 0.01`, thermal diffusivity `alpha = 0.5`.
- Initial condition: The center 20 points (index 40 to 59 inclusive) start at `T_init` (from the video). All other points start at 0.0. Boundary conditions are fixed at 0.0.
- Ensure your code is optimized for performance, as we will be profiling it.

**3. API Service**
The C application must act as an HTTP web server listening on `127.0.0.1:8000`. You may use raw POSIX sockets or install a lightweight library like `libmicrohttpd`.
- **`GET /health`**: Must return HTTP 200 OK with the exact body `OK`.
- **`GET /simulate?steps=<N>`**: Must run the PDE solver from the initial state for `N` time steps, and return a JSON array of the final temperatures of the 100 points, formatted to 2 decimal places. Example: `[0.00, 0.01, ..., 0.00]`

**4. Performance Profiling**
Profile your C server processing a heavy load (e.g., simulating 10,000 steps). You can use `gprof`, `perf`, or custom timing hooks.
Write a file named `/home/user/profiling_report.txt` containing exactly two lines:
1. `T_INIT=<your_calculated_T_init>`
2. `BOTTLENECK=<name_of_the_c_function_taking_the_most_time>`

Compile your C code and run it in the background so the server is actively listening on port 8000 when you complete the task.