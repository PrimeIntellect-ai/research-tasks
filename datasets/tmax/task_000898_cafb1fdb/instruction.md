You are a data scientist working mostly in a Linux terminal. You have been given a raw dataset of 3D sensor coordinates and need to clean it using purely Bash and standard POSIX utilities (like `awk`, `sed`, `grep`, `bc`, etc.). Do not use Python, R, or Perl.

The raw data is located at `/home/user/raw_sensors.csv` and has the following columns (with a header row):
`id,x,y,z,timestamp`

Your objective is to write a Bash script at `/home/user/clean_data.sh` that performs the following steps when executed:

1. **Feature Engineering**: For every row (excluding the header), calculate a new feature `magnitude` which is the Euclidean distance from the origin: `sqrt(x^2 + y^2 + z^2)`.

2. **Deterministic Sampling**: To estimate the population statistics without processing the entire dataset (simulating a sampling technique), extract a systematic sample consisting of every 7th data row (i.e., the 7th, 14th, 21st... data rows after the header). 

3. **Statistical Modeling**: Calculate the `mean` and `standard deviation` (population standard deviation) of the `magnitude` feature strictly from this systematic sample. Round both the mean and standard deviation to 4 decimal places.

4. **Filtering**: Filter the *entire original dataset* (all rows). Keep only the rows where the calculated `magnitude` falls strictly within 1.5 standard deviations of the mean (calculated from the sample). 

5. **Reporting**: Create a new file at `/home/user/cleaned_sensors.csv` containing the surviving rows. 
   - The output must include the original header row, modified to include the new feature: `id,x,y,z,timestamp,magnitude`.
   - The data rows must append the calculated `magnitude` (rounded to 4 decimal places) as the final column.
   - Also, append a final line to the bottom of the file in this exact format: `# STATS: mean=<mean>, std=<std>` using the exact values calculated in step 3.

Ensure your script `/home/user/clean_data.sh` is executable and performs this entire pipeline autonomously when run.