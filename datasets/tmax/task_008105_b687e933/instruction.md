You are a data scientist performing a preliminary model fit using basic shell tools. We have an experimental parameter stored in a NetCDF file, and we need to simulate a stochastic process based on this parameter and visualize the resulting distribution.

Your task is to write and execute a Bash script at `/home/user/run_mc.sh` that performs the following steps:

1. **Scientific Data Extraction**: Use `ncdump` to extract the integer value of the variable `base_offset` from the NetCDF file located at `/home/user/experiment.nc`.
2. **Monte Carlo Simulation**: In your Bash script, set the random seed exactly by assigning `RANDOM=12345`. Then, simulate 10,000 independent samples. For each sample, generate a random value `X = base_offset + (RANDOM % 7)`. 
3. **Experimental Data Visualization**: Calculate the frequency of each possible value of `X`. Generate an ASCII histogram and save it to `/home/user/histogram.txt`.
   - The file must contain one line for each possible value of `X` (in ascending order).
   - Format each line exactly as: `VALUE: STARS`
   - `STARS` should be a sequence of asterisk `*` characters, where each `*` represents exactly 50 occurrences in the simulation (use integer floor division, e.g., 149 occurrences = 2 stars, 150 occurrences = 3 stars). No trailing spaces.

Make sure your script executes successfully and generates the correct `/home/user/histogram.txt` file.