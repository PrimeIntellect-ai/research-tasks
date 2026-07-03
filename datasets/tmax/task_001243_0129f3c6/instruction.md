You are a performance engineer working on a spectroscopic data processing pipeline. A critical component of the pipeline is a C++ program that inverts a 2x2 matrix representing overlapping spectroscopic peaks. We have noticed that when the peaks are nearly identical (simulated by a small perturbation parameter `epsilon`), the matrix becomes near-singular and the computed inverse values explode, leading to numerical instability in downstream Monte Carlo simulations.

I have written a basic C++ program at `/home/user/inv.cpp` that takes `epsilon` as a command-line argument, computes the inverse of the matrix, and prints the top-left element of the inverted matrix to standard output.

Your task is to:
1. Write a bash script at `/home/user/run_mc.sh` that first compiles `/home/user/inv.cpp` to an executable named `/home/user/inv`.
2. The script should then iterate through the following `epsilon` values in decreasing order: `1`, `0.1`, `0.01`, `0.001`, `0.0001`.
3. For each `epsilon`, run the compiled `/home/user/inv` executable.
4. Find the largest `epsilon` from the provided list that causes the output (the top-left element of the inverse) to be strictly greater than `1000.0`.
5. Write ONLY this exact `epsilon` value (as written in the list above) to a file named `/home/user/result.txt`.
6. Make sure your script `/home/user/run_mc.sh` is executable and run it to produce the result file.

Constraints:
- Use standard bash and CLI tools.
- The C++ source is already provided at `/home/user/inv.cpp`. Do not modify it.