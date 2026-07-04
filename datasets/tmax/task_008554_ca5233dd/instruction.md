I am a researcher running data processing simulations, and I need to extract the dominant principal component from a multi-dimensional experimental dataset. The dataset is represented as a 2D matrix. 

I have a raw text file containing a 4x3 matrix of floating-point numbers located at `/home/user/sim_data/matrix.txt`.

Please write a C program at `/home/user/sim_data/process_svd.c` that does the following:
1. Reads the 4x3 matrix from `/home/user/sim_data/matrix.txt`.
2. Uses the GNU Scientific Library (GSL) to perform a Singular Value Decomposition (SVD) on this matrix. (The `libgsl-dev` package is already installed on the system).
3. Extracts the largest singular value.
4. Writes this single largest singular value, formatted to exactly 4 decimal places (e.g., `12.3456`), to a file named `/home/user/sim_data/result.txt`.

You must compile your C program linking against the GSL libraries (`-lgsl -lgslcblas -lm`) and run it to produce the `result.txt` file.