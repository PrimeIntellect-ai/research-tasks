I am a researcher running simulations of a 2D diffusion process (like heat transfer). I have an experimental recording in a video file located at `/app/diffusion.mp4`.

My current workflow is broken. I wrote a C program to simulate the 2D Heat Equation ($\frac{\partial u}{\partial t} = \alpha \nabla^2 u$), but it diverges and produces NaNs (similar to how some matrix factorizations fail on near-singular input, my explicit finite difference method is numerically unstable given the parameters). 

I need you to build a reliable workflow that extracts the initial conditions from the video, correctly simulates the PDE in C, and exposes the simulation via a web service so my Jupyter notebooks can query it.

Here are the specific requirements:

1. **Video Processing**:
   - Extract the very first frame of `/app/diffusion.mp4`.
   - Convert it to a 64x64 grayscale matrix. The video frames are exactly 64x64 pixels.
   - Map the pixel values (0-255) to a floating-point matrix (0.0 to 1.0). This represents the initial state $u(x,y,0)$.
   - Save this initial state to a plain text file `/home/user/initial_state.txt` (64 lines, 64 space-separated floats per line).

2. **C Simulation Fixing**:
   - Write a C program at `/home/user/simulate.c` that reads `/home/user/initial_state.txt`.
   - It must simulate the 2D heat equation using the explicit finite difference method.
   - Parameters: $\alpha = 0.2$, $\Delta x = 1.0$, $\Delta y = 1.0$.
   - **Crucial**: You must choose a stable time step $\Delta t$ that satisfies the Courant-Friedrichs-Lewy (CFL) condition for this 2D explicit method to prevent divergence.
   - The program should take the target time $T$ as a command-line argument (e.g., `./simulate 5.0`), run the simulation from $t=0$ to $t=T$, and print the *sum* of all values in the 64x64 grid at the final time to standard output as a single float.
   - Assume zero-flux (Neumann) or zero-value (Dirichlet) boundary conditions - actually, to keep it simple, assume periodic boundary conditions.

3. **Service Orchestration**:
   - Create and run an HTTP server (e.g., using Python's Flask or FastAPI, which can wrap your compiled C binary) listening on `0.0.0.0:8080`.
   - The service must expose a `POST /simulate` endpoint.
   - It should accept JSON: `{"t_end": <float>}`.
   - It must execute your compiled C simulation with the given `t_end`, capture the resulting sum, and return JSON: `{"sum": <float>}`.

Ensure your service is running in the background and is fully bound to port 8080 before you finish. Do not use an auth token.