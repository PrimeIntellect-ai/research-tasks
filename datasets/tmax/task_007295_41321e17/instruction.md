You are an automation specialist setting up a data processing pipeline for 3D sensor coordinates. 

There is an input file located at `/home/user/sensors.csv` containing raw uncalibrated sensor readings. Each line has three comma-separated float values representing X, Y, and Z coordinates.

Your task is to build a multi-stage pipeline that computes mathematical properties, deduplicates entries using a custom hash, and stratifies the sample.

Step 1: Write a C program `/home/user/process.c` that reads lines of `X,Y,Z` coordinates from standard input until EOF.
For each line, the program must:
1. Calculate the Euclidean distance `D` from the origin (0.0, 0.0, 0.0).
2. Cast the distance to an integer (`int`).
3. Calculate the Stratum: `Stratum = D % 3` (using the integer distance).
4. Calculate a simple Hash for deduplication by XORing the integer-casted coordinates: `Hash = ((int)X) ^ ((int)Y) ^ ((int)Z)`
5. Print the result to standard output in the format: `Stratum,Hash,X,Y,Z` (format X, Y, and Z to exactly 2 decimal places).

Step 2: Write a Bash script `/home/user/pipeline.sh` that orchestrates the workflow. The script must:
1. Compile `/home/user/process.c` into an executable named `process` in the same directory (remember to link the math library).
2. Pipe the contents of `/home/user/sensors.csv` into `./process`.
3. Deduplicate the stream based *only* on the `Hash` column (Column 2). If multiple rows have the same Hash, keep the *first* one encountered.
4. From the deduplicated stream, sample exactly 2 records for each Stratum (or all available if fewer than 2 exist). Prioritize records that appeared earliest in the stream.
5. Sort the final sampled records numerically by Stratum (Column 1) in ascending order.
6. Write the final output to `/home/user/sampled_output.csv`.

Make sure `/home/user/pipeline.sh` has executable permissions and run it so that `/home/user/sampled_output.csv` is created.