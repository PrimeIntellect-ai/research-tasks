Hello! I need your help building a numerical integration tool in Go to analyze some recent physics simulation results. 

We are researching the behavior of potential fields around point sources, particularly focusing on how to stably integrate near-singular potentials over a spatial domain. 

Here is what I need you to do:

**1. Video Analysis**
We have recorded a short simulation run of our diffusion experiment, located at `/app/experiment.mp4`. 
Please analyze this video and determine the exact number of frames it contains. You can use standard tools like `ffmpeg` or `ffprobe`. This frame count, let's call it $N$, represents the mesh resolution constraint mandated by our experimental setup.

**2. Numerical Integrator Implementation in Go**
Write a Go program at `/home/user/mesh_solver.go` and compile it to an executable at `/home/user/mesh_solver`.

This program must compute the 2D surface integral of a near-singular potential function over a square domain using the Midpoint Riemann Sum method.

The potential function is defined as:
$$ P(x,y) = \frac{1}{\sqrt{(x - cx)^2 + (y - cy)^2 + 10^{-8}}} $$
where $(cx, cy)$ is the center of the point source. Note the $10^{-8}$ term added to the denominator to prevent division by zero (a common issue when the point source lies exactly on a mesh evaluation node).

The integration domain is a square from $[-R, R]$ in both the X and Y axes. 

Your program must subdivide this domain into an $N \times N$ uniform mesh (where $N$ is the exact frame count you extracted from the video). 
- $\Delta x = \frac{2R}{N}$
- $\Delta y = \frac{2R}{N}$
- The evaluation point for each cell should be its geometric center (the midpoint). For example, the x-coordinate of the $i$-th column midpoint ($i$ from $0$ to $N-1$) is $-R + (i + 0.5) \times \Delta x$.

**3. CLI Specifications**
The compiled binary `/home/user/mesh_solver` must accept exactly three positional command-line arguments (all float64):
1. `cx` (the x-coordinate of the source)
2. `cy` (the y-coordinate of the source)
3. `R` (the half-width of the square integration domain)

Example invocation:
`./mesh_solver 0.5 -0.2 2.0`

The program must calculate the total integral sum across the $N \times N$ cells and print ONLY the final floating-point result to standard output, formatted to exactly 6 decimal places (e.g., using `fmt.Printf("%.6f\n", result)`).

I need this to be highly accurate and follow the exact mesh generation rules specified, as we will be testing your compiled binary against a reference oracle across thousands of random near-singular inputs. Good luck!