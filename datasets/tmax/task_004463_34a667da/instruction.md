You are an ML engineer preparing training data from a simulated 2D acoustic sensor array. 
The raw data is stored in `/home/user/raw_mesh_data/` as 100 CSV files named `sensor_X_Y.csv`, where `X` and `Y` range from 0 to 9, representing a 10x10 mesh grid.

Each CSV file contains simulated spectroscopic data with two columns: `frequency` (in Hz) and `intensity`. 

Your task is to write and execute a Bash script that downsamples this 10x10 spatial mesh into a 2x2 grid (domain decomposition) by extracting specific spectral features.

Specifically, you must:
1. For every sensor, find the maximum `intensity` value within the frequency range 1000 Hz to 1500 Hz (inclusive).
2. Decompose the 10x10 mesh into four 5x5 quadrants:
   - `Q0_0`: X in 0..4, Y in 0..4
   - `Q1_0`: X in 5..9, Y in 0..4
   - `Q0_1`: X in 0..4, Y in 5..9
   - `Q1_1`: X in 5..9, Y in 5..9
3. Compute the average of the maximum intensities (found in step 1) for the 25 sensors within each quadrant.
4. Output these four averages to a log file at `/home/user/training_mesh_features.txt` with exactly this format (rounded to 2 decimal places):
   ```
   Q0_0: [value]
   Q1_0: [value]
   Q0_1: [value]
   Q1_1: [value]
   ```
5. To help quickly inspect the data, generate a simple ASCII visualization of the pooled features in `/home/user/mesh_vis.txt`. For each quadrant, print its identifier, a colon, a space, and a number of `*` characters equal to the integer part of `(average / 5)`. For example, if the average is 26.10, print 5 asterisks. The format must be:
   ```
   Q0_0: *
   Q1_0: ***
   Q0_1: *****
   Q1_1: *******
   ```

Do not use external Python libraries like `pandas` or `numpy` to solve the entire task; you should orchestrate the processing primarily using Bash and standard UNIX utilities (like `awk`, `grep`, `bc`, etc.), though standard Python can be used for math if needed.