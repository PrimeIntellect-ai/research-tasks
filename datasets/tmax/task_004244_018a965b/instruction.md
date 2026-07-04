I am a performance engineer responsible for profiling our new C++ network analysis pipeline. We are building a tool to find the dominant structural component (principal eigenvalue) of observational network data using the Power Iteration method. 

I need you to build a reproducible, profiled pipeline. You will be provided with observational network data in `/home/user/edges.csv`. You must write a C++ program, a `Makefile`, and a bash script to execute and profile the workflow.

Here are your requirements:

1. **C++ Program (`/home/user/analyze_network.cpp`)**:
   - Read the network data from `/home/user/edges.csv`. The file has the format `source_node,target_node,weight` on each line (0-indexed integers for nodes, float for weight).
   - Reshape this edge list into a dense Adjacency Matrix $A$. You can assume the maximum node ID dynamically dictates the size of the $N \times N$ matrix.
   - Implement the **Power Iteration** method to find the dominant eigenvalue. 
     - Initialize a vector $v$ of size $N$ with all $1.0$s.
     - Iteration step: $v_{new} = A v$.
     - Normalize: $v_{new} = v_{new} / ||v_{new}||_2$ (using Euclidean norm).
     - Calculate the Rayleigh quotient for the eigenvalue approximation: $\lambda = v_{new}^T A v_{new}$ (since $v_{new}$ is normalized).
     - Stop when $|\lambda_{new} - \lambda_{old}| < 10^{-6}$ or after 1000 iterations.
   - Write the final dominant eigenvalue $\lambda$ to `/home/user/eigenvalue.log`, formatted exactly to 4 decimal places (e.g., `12.3456`).

2. **Makefile (`/home/user/Makefile`)**:
   - Must compile `analyze_network.cpp` into an executable named `analyze_network`.
   - Must include compiler flags `-O3` (for optimization) and `-pg` (to enable `gprof` profiling).

3. **Pipeline Script (`/home/user/run_pipeline.sh`)**:
   - Must be an executable bash script.
   - Must call `make` to build the executable.
   - Must run `./analyze_network`.
   - Must run `gprof ./analyze_network gmon.out` and redirect the profiling output to `/home/user/profile_results.txt`.

Ensure all files are created exactly at the specified paths. Do not install external C++ matrix libraries; implement the matrix-vector multiplication and norm calculations using standard C++ library components (like `std::vector`).