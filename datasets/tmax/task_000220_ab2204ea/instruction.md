You are a performance engineer analyzing a new spectroscopy signal processing application. The application processes noisy spectral data, and its execution time varies significantly depending on the input signal's noise profile. 

We have a simulator for this application located at `/home/user/spectroscopy_sim.py`. It takes a single argument `--seed <INT>` to simulate the noise profile for a specific run.

Your task is to write a Bash script `/home/user/profiler.sh` that acts as a performance profiling harness. The script must combine Monte Carlo simulation principles and Bootstrap confidence intervals to estimate the true average execution time.

Requirements for `/home/user/profiler.sh`:
1. It must accept exactly two arguments: `N` (number of runs) and `B` (number of bootstrap resamples).
2. **Data Collection (Monte Carlo Simulation):** The script should loop `i` from 1 to `N` (inclusive). In each iteration, it must run `python3 /home/user/spectroscopy_sim.py --seed <i>` and extract the execution time (which is printed in the format `Time: <value> ms`).
3. **Bootstrap Analysis:** Using pure Bash and/or standard command-line tools (like `awk`, `sort`, etc. - do NOT write a separate Python/Perl script for this step), perform `B` bootstrap resamples of the collected execution times. 
   - A single bootstrap resample consists of drawing `N` samples from your collected data *with replacement*, and calculating the mean of those `N` samples.
   - Repeat this `B` times to generate `B` bootstrap means.
4. **Confidence Interval:** Sort the `B` bootstrap means and find the 95% confidence interval (i.e., the 2.5th percentile and the 97.5th percentile). You can approximate the index by rounding to the nearest integer (e.g., if B=1000, the 2.5th percentile is the 25th value in the sorted list).
5. **Output:** The script must write the final result to `/home/user/profile_results.txt` in exactly the following format:
   `N=<N>, B=<B>, CI=[<lower_bound>, <upper_bound>]`
   (Round the bounds to 2 decimal places).

Finally, after creating the script, execute it with `N=50` and `B=5000` so that `/home/user/profile_results.txt` is populated. 

Ensure the script is executable. You may create temporary files in `/home/user/` if needed during the execution of your script.