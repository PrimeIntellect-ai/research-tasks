You are a data scientist working on an ETL pipeline for a machine learning model. Our system logs feature vectors in a highly optimized binary format, but we've realized the data isn't properly normalized before being stored.

I have a raw dataset located at `/home/user/raw_data.bin`. This file contains exactly 4,000 32-bit floating-point numbers (little-endian format), which represents 1,000 contiguous vectors of dimension 4.

Your task is to write a C program at `/home/user/etl_clean.c` that performs the following data cleaning operations:
1. Opens `/home/user/raw_data.bin` and reads the vectors.
2. Calculates the global mean of all 4,000 raw floating-point numbers.
3. Writes this global mean to a text file at `/home/user/global_mean.txt`, formatted to exactly 4 decimal places with a trailing newline (e.g., `1.2345\n`).
4. Performs vector-level mean centering for each of the 1,000 vectors. Specifically, for each vector $v$ of length 4, compute the mean of its 4 elements ($\mu_v$), and subtract $\mu_v$ from each of its elements ($v_i' = v_i - \mu_v$).
5. Writes the resulting 4,000 transformed 32-bit floats to a new binary file at `/home/user/cleaned_data.bin` (also little-endian).

Once you have written the code, compile it using `gcc` into an executable named `/home/user/etl_clean`, and execute it to generate the requested output files. 

Ensure the paths are strictly followed and the binary output precisely matches the expected 16,000-byte structure.