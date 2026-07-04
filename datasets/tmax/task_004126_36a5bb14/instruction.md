You are a performance engineer profiling a scientific simulation. We recently parallelized the simulation, but due to floating-point reduction order variations in the multi-threaded implementation, the final energy state outputs are no longer perfectly deterministic. 

I have provided two files in your home directory containing the final state values across 1000 runs:
1. `/home/user/single_thread.csv` (The stable, single-threaded baseline)
2. `/home/user/multi_thread.csv` (The multi-threaded results with floating-point drift)

Both files contain a single column of floating-point numbers with no header.

Your task is to build a reproducible Python analysis script to quantify and visualize this drift:
1. Write a Python script at `/home/user/analyze_sim.py` that reads these two files.
2. The script must compute the 1D Wasserstein distance (Earth Mover's Distance) between the two sets of results. 
3. The script must write the computed Wasserstein distance to `/home/user/wasserstein.txt`, rounded to exactly 4 decimal places.
4. The script must also generate an overlaid histogram visualization of the two distributions (using 50 bins, alpha=0.5 transparency, and appropriate labels) and save the plot to `/home/user/distributions.png`.
5. Run your script to produce the output files.

Ensure your script is fully self-contained and reproducible.