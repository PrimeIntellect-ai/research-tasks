You are acting as a machine learning engineer preparing training data for an anomaly detection model. You have a raw telemetry log from various sensors, but the data is sparse for a specific critical sensor. You need to extract its observational data, fit a normal distribution to it, and use Monte Carlo sampling to generate synthetic training data.

The raw data is located at `/home/user/raw_telemetry.csv`.
The file has a header and four comma-separated columns: `timestamp,sensor_id,status,reading`

Write a Bash script (using standard GNU tools like `awk`, `grep`, `sed`, etc.) saved to `/home/user/generate_synthetic.sh` that does the following when executed:

1. **Observational Data Reshaping**: Parse `/home/user/raw_telemetry.csv`, filtering only the rows where `sensor_id` is exactly `T-800` and `status` is exactly `VALID`. Extract the `reading` values.
2. **Distribution Fitting**: Calculate the sample mean ($\mu$) and the population standard deviation ($\sigma$) of these extracted readings.
3. **Monte Carlo Simulation**: Generate exactly 5000 synthetic readings drawn from a Normal distribution $N(\mu, \sigma^2)$ using the Box-Muller transform. 
   - You must use `awk` for the generation. 
   - Initialize the random number generator in `awk` with the exact seed `42` (`srand(42)`) immediately before the loop that generates the 5000 points.
   - For the Box-Muller transform, use $\pi \approx 3.14159265359$.
   - The equations for Box-Muller are:
     $U_1 \sim Uniform(0,1)$
     $U_2 \sim Uniform(0,1)$
     $Z_0 = \sqrt{-2 \ln U_1} \cos(2 \pi U_2)$
     $X = \mu + Z_0 \sigma$
   - Generate exactly one value ($X$) per iteration for 5000 iterations.
4. **Output**: Save the 5000 synthetic readings (one per line) to `/home/user/synthetic_T800.csv`. Format each number to exactly 4 decimal places (e.g., using `printf "%.4f\n"`).

Ensure the script `/home/user/generate_synthetic.sh` has executable permissions.