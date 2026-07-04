You are a performance engineer working on a simulation code that computes an integral over a 1D mesh using domain decomposition. The code divides the mesh into subdomains, computes the integral on each in parallel, and sums the results.

However, we are experiencing non-reproducible results. Every time we run the simulation, the final aggregated value changes slightly at the 12th-15th decimal place. This is unacceptable for our validation tests. We suspect the issue is caused by the floating-point reduction order: the partial results from the worker processes are being summed in the non-deterministic order they complete, rather than the sequential order of the mesh subdomains.

Your tasks are as follows:
1. Compile the provided Cython extension for the mesh calculation. The files `/home/user/calc_chunk.pyx` and `/home/user/setup.py` are already provided. You will need to build the extension in-place so it can be imported by Python.
2. Analyze and fix the main simulation script at `/home/user/sim.py`. Modify it so that the partial results are summed strictly in the increasing order of their subdomain index (from `0` to `num_chunks - 1`).
3. Run the fixed simulation.
4. Compare your output to the known deterministic result located in `/home/user/reference.txt`.
5. Write your final, deterministic floating-point result (just the number) to `/home/user/result.txt`.

Make sure your final result matches the reference exactly. You must not change the mathematical logic inside the Cython module, the number of chunks, or the mesh bounds. Only fix the reduction order in `sim.py`.