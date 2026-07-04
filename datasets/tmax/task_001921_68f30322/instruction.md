You are a scientific researcher analyzing a legacy simulation of a stellar core. You have been given a stripped, undocumented binary executable located at `/app/stellar_core_sim`. 

Your goal is to orchestrate a data collection and analysis pipeline entirely using Bash and standard Unix tools (like `awk`, `bc`, `sed`) to compute the total mass of the stellar core and its uncertainty. You must write a script at `/home/user/analyze_core.sh`.

Here is what you need to do:
1. **Understand the Binary:** The binary represents a stochastic simulation. Through trial and error, you will find it takes a single floating-point argument representing the radius ($r$ in megameters, valid from $0.0$ to $10.0$) and outputs the expected plasma density at that radius. The output is noisy.
2. **Data Collection:** In your script, sample the radius from $0.1$ to $10.0$ in increments of $0.1$ (i.e., 100 spatial points). Because the simulation is stochastic, you must query the binary 50 times for *each* radial point to get a reliable sample distribution.
3. **Numerical Integration:** The mass of the stellar core is given by the spherical volume integral of the density: $M = \int_{0}^{10} 4 \pi r^2 D(r) dr$. Use the Trapezoidal rule to numerically integrate the mean density at each point to estimate the total mass.
4. **Bootstrap Confidence Interval:** To estimate the uncertainty of your mass calculation, implement a bootstrap resampling procedure (with at least 500 iterations). In each iteration, resample with replacement from your 50 observations at each radial point, compute the mean density for that point, and then re-calculate the numerical integral. Determine the 90% confidence interval (5th and 95th percentiles) of the total mass.
5. **Output Format:** Your script `/home/user/analyze_core.sh` must be executable and output exactly three lines to `stdout` in the following format:
   `MEAN_MASS: <calculated_mean_mass>`
   `CI_LOWER: <5th_percentile_mass>`
   `CI_UPPER: <95th_percentile_mass>`

Constraints:
- You must use Bash, `awk`, `bc`, or other POSIX shell utilities for the implementation. Do not write the core logic in Python, R, or C. 
- You must handle the black-box binary execution and parsing within the script.