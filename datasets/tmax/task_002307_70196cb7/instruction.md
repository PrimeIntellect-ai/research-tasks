You are acting as a computational research assistant. We are conducting regression testing on our physics simulation engine, but we lost the configuration file for a specific benchmark run. All we have is the rendered output video of the simulation.

We need to recover the simulation parameters: the aerodynamic drag coefficient ($C_d$) and the initial velocity vector ($v_{x0}$, $v_{y0}$) of the projectile.

**Available Resources:**
- A video of the simulation: `/app/experiment_video.mp4`.
- The video is exactly 60 FPS, 1920x1080 resolution.
- The object is a bright red circle (RGB: ~255, 0, 0) on a solid black background.
- Spatial Scale: 100 pixels = 1 meter. The origin (0,0) in the simulation corresponds to the starting position of the object's center at frame 0. Standard screen coordinates apply (Y increases downwards, but gravity points down).
- The physics model is a 2D point mass with quadratic drag: 
  $\frac{d\vec{v}}{dt} = \vec{g} - C_d |\vec{v}| \vec{v}$
  where $\vec{g} = (0, 9.81) \text{ m/s}^2$ (assuming Y is down).

**Your Task:**
1. **Data Extraction:** Extract the trajectory (X, Y pixel coordinates of the center of the red circle) for every frame of the video. You may use shell commands and Python/OpenCV for this data processing step.
2. **C++ Optimization Pipeline:** Write a C++ program (`/home/user/optimizer.cpp`) that takes this extracted trajectory data and implements an optimization algorithm (e.g., Gradient Descent, Nelder-Mead Simplex, or Genetic Algorithm) to find the best-fitting $C_d$, $v_{x0}$ (in m/s), and $v_{y0}$ (in m/s).
    - Your C++ code must include a forward ODE integrator (Euler or RK4) to simulate trajectories during optimization.
3. **Execution:** Compile and run your C++ optimizer.
4. **Output:** Save the final optimized parameters to `/home/user/optimized_params.txt`. The file must contain exactly three comma-separated floating-point numbers on a single line:
   `Cd, vx0, vy0`

*Note: The automated evaluation suite will read `/home/user/optimized_params.txt` and run a forward simulation with your parameters. Your parameters must produce a trajectory that closely matches the video.*