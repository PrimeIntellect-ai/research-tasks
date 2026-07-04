You are a performance engineer tasked with profiling and optimizing a mechanical deformation simulation pipeline. We have a tracking system that analyzes high-speed video footage of a deforming elastic mesh, constructs a linear system representing the stress-strain relationships, and solves for the internal forces.

Currently, the pipeline is far too slow for real-time analysis.

You have been provided with:
1. A video fixture at `/app/deformation.mp4` showing the 2D mesh deforming over time.
2. The baseline C source code in `/home/user/sim/` which contains:
   - `extract.sh`: A shell script that uses `ffmpeg` to extract frames from the video.
   - `main.c`: The entry point that processes the frames, tracks the mesh nodes, and sets up the system $Ax = b$ where $A$ is a symmetric positive-definite stiffness matrix.
   - `solver.c`: A heavily unoptimized matrix solver using a naive $O(N^3)$ Gaussian elimination to solve the system.
   - `Makefile`: To compile the executable `mesh_sim`.

Your objective is to:
1. Run `extract.sh` to prepare the frame data.
2. Profile the `mesh_sim` application to confirm the bottleneck (you will find it is in `solver.c`).
3. Optimize the matrix solver in `solver.c`. Since the matrix $A$ is Symmetric Positive Definite (SPD) and strictly diagonally dominant, you must implement a more efficient matrix decomposition (such as Cholesky decomposition) or a block-based domain decomposition solver to replace the naive Gaussian elimination.
4. Compile your optimized version.
5. Run your optimized `./mesh_sim`. It reads the frames and outputs a file `/home/user/sim/forces.txt`.

Requirements for success:
- The output `/home/user/sim/forces.txt` must remain mathematically equivalent to the baseline output (Mean Squared Error < 1e-4).
- The execution time of `./mesh_sim` must be reduced significantly. The automated verifier will measure the runtime of `./mesh_sim`. You must achieve a speedup of at least **5.0x** compared to the naive implementation.

Do not modify the tracking logic or the matrix generation in `main.c`; focus your optimizations entirely on the equation solving step in `solver.c`.