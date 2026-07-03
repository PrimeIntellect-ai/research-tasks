I am researching thermal diffusion on a 2D plate. I have an experimental recording of a heat test captured in a video at `/app/thermal_diffusion.mp4`. 

I need you to perform a data-driven simulation matching process to find the correct diffusion coefficient for my model:

1. **Experimental Data Processing (Python):**
   - Extract the frames from `/app/thermal_diffusion.mp4`.
   - Convert them to grayscale (0-255, then normalize to 0.0-1.0). Each frame represents a 64x64 spatial grid of temperatures.
   - Flatten each frame into a 4096-element vector and assemble them into a matrix $X$ of size $4096 \times T$, where $T$ is the number of frames.
   - Perform Singular Value Decomposition (SVD) on this matrix: $X = U \Sigma V^T$.
   - Extract the primary spatial mode (the first column of $U$). Normalize it so its L2 norm is 1.0. This is the `reference_mode`.

2. **Simulation Compilation (C++):**
   - In `/home/user/sim_src/`, there is a C++ solver `heat_solver.cpp` and a `Makefile`.
   - The solver currently has a hardcoded coarse mesh size (`#define N 16`). Edit the source code to perform mesh refinement: update it to `#define N 64` so it matches the video's spatial domain.
   - Compile the solver from source using `make`.

3. **Simulation Alignment (Multi-language):**
   - The compiled solver `./heat_solver <D>` takes a single command-line argument: the diffusion coefficient $D$ (a float).
   - It outputs a CSV file `sim_output.csv` containing the simulated frames (each row is a flattened 64x64 frame across time).
   - Write a script to wrap the simulation. Search for the best diffusion coefficient $D \in [0.01, 0.20]$ (with a precision of at least 0.01) that maximizes the absolute dot product (cosine similarity) between the simulated primary spatial mode (obtained via the same SVD process on `sim_output.csv`) and the experimental `reference_mode`.

4. **Outputs:**
   - Save the best simulated primary spatial mode (a 64x64 numpy array, L2 norm = 1.0) to `/home/user/best_sim_mode.npy`.
   - Write the corresponding best $D$ value to `/home/user/best_D.txt`.

Ensure your methods are mathematically sound.