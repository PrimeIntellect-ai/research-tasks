You are a data scientist analyzing the volumetric properties of proteins using a Monte Carlo integration approach. 

I have a C++ program at `/home/user/mc_volume.cpp` that reads a simplified PDB file (`/home/user/protein.pdb`) and estimates the total volume occupied by the atoms using Monte Carlo simulation. It uses OpenMP to parallelize the points.

However, I am facing a reproducibility issue. Every time I run the compiled program, it outputs a slightly different floating-point value. I have traced the issue to the floating-point reduction order in the OpenMP parallel loop (`total_volume += vol_per_sample;`). Because floating-point addition is not strictly associative, the different thread completion orders cause slightly different round-off accumulations.

Your task:
1. Modify `/home/user/mc_volume.cpp` to make the result perfectly reproducible and deterministic across multiple runs without removing OpenMP parallelism. 
   *Hint: Think about how you can accumulate the results without floating-point reduction errors, and only convert to float at the very end.*
2. Compile your modified C++ code using `g++ -O3 -fopenmp mc_volume.cpp -o mc_volume`.
3. Run the program and save the final, deterministic volume output (which will be a single float value) to `/home/user/result.txt`.

Ensure your fix doesn't alter the core logic, random seeds, or the number of Monte Carlo samples—only the way the successful samples are accumulated.