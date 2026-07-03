You are a performance engineer working on a bioinformatics project. The team has developed a Python script that processes a set of DNA sequences, calculates the thermodynamic melting temperature ($T_m$) for potential primers using a nonlinear equation, and computes a binding efficiency score via numerical integration.

The current script, located at `/home/user/bio_profiling/primer_sim.py`, produces the correct scientific results but is incredibly slow. Your task is to profile the script, identify the performance bottlenecks in the numerical routines, and create an optimized version.

Here are your specific requirements:
1. Profile `/home/user/bio_profiling/primer_sim.py`. Identify the slowest functions. Create a plain text file at `/home/user/bio_profiling/profile_notes.txt` where the first line contains the exact name of the slowest function (e.g., `calculate_tm` or `integrate_efficiency`).
2. Create an optimized script at `/home/user/bio_profiling/optimized_primer_sim.py`. 
3. Your optimized script must produce the exact same output file (`/home/user/bio_profiling/results.json`) as the original script. All numerical values in the JSON must match the original output to within a relative tolerance of $10^{-4}$.
4. The optimized script must run in under 2 seconds. (The original script purposefully uses naive, unoptimized pure-Python loops for numerical integration and a grossly inefficient nonlinear root-finding method. You should replace these bottlenecks with efficient vectorized `numpy` operations or `scipy` functions like `scipy.optimize.fsolve` and `scipy.integrate.quad` or `numpy.trapz`).
5. Ensure that the new script can be run simply with `python3 /home/user/bio_profiling/optimized_primer_sim.py`.

You may use standard scientific libraries (`numpy`, `scipy`). Do not change the underlying mathematical formulas, only *how* they are computed.