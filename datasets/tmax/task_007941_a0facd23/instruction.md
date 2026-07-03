You are acting as a bioinformatics analyst working with raw signal data from a nanopore sequencing device. Your task is to build a small data-processing pipeline that compiles a signal-smoothing tool, applies it to the raw data, and performs a matrix decomposition (SVD) to extract the principal signal components.

Here are the specific requirements:

1. **Scientific Environment Management**:
   - Create a Python virtual environment at `/home/user/bio_env`.
   - Install `numpy` in this virtual environment.

2. **Scientific Software Compilation**:
   - You have been provided with the source code for a C-based signal smoother at `/home/user/src/smooth.c`.
   - Create a directory `/home/user/bin`.
   - Compile `smooth.c` using `gcc` into an executable named `smooth` inside `/home/user/bin/`.

3. **Spectroscopy / Signal Processing**:
   - The raw signal data is located at `/home/user/raw_data.txt`. It contains 5000 floating-point numbers, one per line.
   - Run the compiled `smooth` executable. It reads from standard input and writes to standard output. 
   - Feed `/home/user/raw_data.txt` into the executable and redirect the output to `/home/user/smoothed.txt`.

4. **Matrix Decomposition**:
   - Write a Python script (using the virtual environment you created) that reads `/home/user/smoothed.txt`.
   - Reshape the 5000 smoothed values into a 2D numpy array with 100 rows and 50 columns (in row-major / C-style order).
   - Perform Singular Value Decomposition (SVD) on this matrix.
   - Extract the top 5 singular values (the 5 largest values from the `S` array).

5. **Logging / Verification**:
   - Write the top 5 singular values to a log file at `/home/user/svd_results.log`.
   - Format the file so that each singular value is on its own line, rounded to exactly 4 decimal places (e.g., `1234.5678`).

Ensure all files are created in the exact locations specified. Do not modify the original `raw_data.txt` or `smooth.c` files.