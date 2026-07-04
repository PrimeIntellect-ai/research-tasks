You are a machine learning engineer preparing synthetic training data for a noisy sensor model. You need to implement a Monte Carlo simulation, verify its numerical stability, and visualize the data using only Bash and standard CLI tools (like `awk`, `bc`, etc.). 

Write a bash script at `/home/user/mc_sensor.sh` that performs the following steps:

1. **Monte Carlo Simulation**:
   Use `awk` to simulate 1000 sensor readings. Each reading is the sum of 100 independent random steps.
   - Each step must be a uniformly distributed random float in the range `[-1.0, 1.0)`.
   - You **must** set the random seed to `42` using `srand(42)` in your `awk` script to ensure reproducibility.
   - Save the 1000 final readings (one float per line) to `/home/user/mc_results.txt`.

2. **Numerical Stability Testing**:
   - Calculate the sample variance of the 1000 readings.
   - Save the variance, rounded to exactly 2 decimal places, to `/home/user/variance.txt`.
   - If the variance is strictly between 25.00 and 40.00, write the string `STABLE` to `/home/user/stability.log`. Otherwise, write `UNSTABLE` to the same file.

3. **Experimental Data Visualization**:
   - Process `/home/user/mc_results.txt` to create a text-based histogram in `/home/user/histogram.txt`.
   - Use 8 bins with the following ranges:
     `[-20, -15)`, `[-15, -10)`, `[-10, -5)`, `[-5, 0)`, `[0, 5)`, `[5, 10)`, `[10, 15)`, `[15, 20)` (The last bin includes 20.0).
   - For each bin, format the output exactly as: `[Center] |[Stars]`
     where `[Center]` is the bin's center value (e.g., `-17.5`, `-12.5`, etc.) printed with 1 decimal place.
     `[Stars]` is a sequence of `*` characters, one for every **10** readings in that bin (rounded down. e.g., 25 readings = `**`).
     Example line: `-2.5 |****`

Make sure to mark `/home/user/mc_sensor.sh` as executable and run it so the output files are generated.