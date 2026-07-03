You are a bioinformatics analyst troubleshooting a digital PCR (dPCR) simulation pipeline. 

We model the amplification of DNA across 100,000 micro-droplets using a set of Ordinary Differential Equations (ODEs). A C++ program simulates this and then calculates the distance between the resulting aggregate concentration distribution and an expected baseline.

However, there is a problem: the simulation produces slightly non-reproducible results. Running the exact same simulation multiple times yields slightly different final distance metrics. This is due to a floating-point reduction order issue caused by the way OpenMP atomic additions are used to sum the results from different droplets.

Your tasks are:

1. **Calculate the Primer GC Ratio**: 
   Read `/home/user/target.fasta`. The first 20 nucleotides of the sequence constitute our forward primer. Calculate its GC content ratio (number of G or C bases divided by 20).

2. **Fix the Non-Determinism in `/home/user/pcr_sim.cpp`**:
   Modify the code to eliminate the floating-point non-determinism. You must ensure that the reduction (summation) of droplet concentrations is strictly deterministic. You must retain the OpenMP parallelism for the `simulate_droplet` function since the actual model will be computationally heavy, but you should rewrite the accumulation logic (e.g., store parallel results in an array and perform a single-threaded sequential sum, or use another strictly deterministic reduction method).

3. **Compile and Verify**:
   Compile your fixed code to `/home/user/simulate_fixed`:
   `g++ -O2 -fopenmp /home/user/pcr_sim.cpp -o /home/user/simulate_fixed`

   Run `/home/user/simulate_fixed` exactly 5 times. Pass the GC content ratio you calculated in step 1 as the single command-line argument.
   
   Append the output of each run to `/home/user/stability.log`. If you fixed the issue correctly, all 5 lines in `stability.log` will be perfectly identical.