You are a bioinformatics analyst working with a microfluidic assay that measures the diffusion of a novel fluorescently-tagged oligonucleotide. 

We have recorded a time-lapse video of the experiment, located at `/app/biosensor_timelapse.mp4`. The video shows the oligonucleotide diffusing along a 1D capillary channel over 10 seconds. The width of the video frame corresponds exactly to the physical channel length, which is $x \in [0, 1]$ cm.

Your goal is to extract the empirical concentration data from the video and fit it to a 1D diffusion Partial Differential Equation (PDE) to estimate the diffusion coefficient, $D$.

Write a Bash orchestrator script at `/home/user/run_analysis.sh` that performs the entire workflow. The script can call helper Python scripts that you also create. Your pipeline must accomplish the following:

1. **Observational Data Reshaping:** Use `ffmpeg` to extract exactly 11 frames corresponding to $t = 0, 1, 2, \dots, 10$ seconds. 
2. **Density Estimation:** For each extracted frame, convert the image to grayscale and compute the average intensity of each column (averaging over the y-axis). Normalize this 1D profile so that its spatial integral (or sum, appropriately scaled by $dx$) equals 1.0. This represents the empirical concentration density $C_{obs}(x, t)$.
3. **PDE Numerical Solving & Mesh Refinement:** Write a numerical solver for the 1D diffusion equation:
   $$\frac{\partial C}{\partial t} = D \frac{\partial^2 C}{\partial x^2}$$
   Assume no-flux (Neumann) boundary conditions at $x=0$ and $x=1$. Use the empirical density at $t=0$ as the initial condition $C(x, 0)$. 
   Implement a **spatial mesh refinement** strategy: start solving the PDE with a coarse spatial grid (e.g., $N=20$ points) and iteratively refine the mesh (e.g., double the points) until the predicted concentrations stabilize (the difference in solutions between mesh levels is negligible).
4. **Curve Fitting:** Find the optimal diffusion coefficient $D$ that minimizes the Mean Squared Error (MSE) between your converged PDE numerical solutions $C_{model}(x, t)$ and the empirical densities $C_{obs}(x, t)$ across all extracted timepoints $t \in \{1, 2, \dots, 10\}$.
5. **Output:** The script must write the final estimated optimal diffusion coefficient (a single float value) to `/home/user/diffusion_result.txt`.

Ensure your Bash script is executable and runs the entire pipeline from end-to-end without interactive prompts. Use standard Linux tools, `ffmpeg`, and Python (with `numpy`, `scipy`, `cv2`/`PIL`) as needed.