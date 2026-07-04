You are an expert bioinformatician and C programmer. We need to perform a Monte Carlo simulation of DNA sequence mutations to build a null distribution of GC-content, save it using a scientific data format, and summarize the results.

Here is the step-by-step task:

1. **Input Sequence Data:**
   There is a starting sequence of 1,000 'A' bases located at `/home/user/sequence.txt`. 

2. **Write a Monte Carlo Simulator in C (`/home/user/sim.c`):**
   Write a C program that reads the starting sequence from `/home/user/sequence.txt`.
   The program must run exactly 10,000 independent Monte Carlo trials. For each trial:
   - Start with a fresh copy of the original sequence.
   - Iterate through the 1,000 bases in order.
   - For each base, draw a random float using `drand48()`. If the value is strictly less than `0.05` (5% mutation rate), the base mutates.
   - If it mutates, pick one of the other 3 possible DNA bases (C, G, T) uniformly. To do this, use `lrand48() % 3`. If the original base was A, the mapping is: 0 -> C, 1 -> G, 2 -> T. (Note: Only 'A' will be encountered in the original sequence, so you only need to handle mutating from 'A').
   - Count the total number of 'G' and 'C' bases in the resulting mutated sequence for this trial.
   
   *Crucial PRNG rule:* You must initialize the random number generator exactly once at the very beginning of `main()` using `srand48(42);`.

3. **Save Output to HDF5:**
   The C program must store the 10,000 integer GC-counts as a 1D array into an HDF5 file located at `/home/user/gc_data.h5`.
   - The dataset must be named `/gc_distribution`.
   - The HDF5 datatype must be `H5T_NATIVE_INT`.
   
   Compile your program to `/home/user/sim` using `gcc` and the `-lhdf5` flag, then run it.

4. **Data Visualization / Summary Script:**
   Finally, use standard bash CLI tools (like `h5dump` and `awk`) to read `/home/user/gc_data.h5`, calculate the mean of the GC counts, and save it to a text file `/home/user/summary.txt`.
   The format of `summary.txt` must be exactly:
   `Mean GC: <average>` (rounded to 2 decimal places, e.g., `Mean GC: 33.35`).

Note: Assume `libhdf5-dev` and `hdf5-tools` are already installed on the system.