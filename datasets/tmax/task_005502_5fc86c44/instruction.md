You are acting as a data scientist evaluating a new data pipeline.

I have provided a C source file at `/home/user/generate_data.c` which generates an HDF5 dataset when compiled and run. 

Please perform the following steps:
1. Compile the `/home/user/generate_data.c` file into an executable named `/home/user/generate_data`. You will need to link it against the HDF5 library (e.g., using `h5cc` or by passing the correct flags to `gcc`).
2. Run the compiled executable to produce the HDF5 file `/home/user/data.h5`.
3. Write a Python script to read the `/home/user/data.h5` file. The file contains two datasets: `dist_A` and `dist_B`.
4. Using Python, compute the 1st Wasserstein distance between these two empirical distributions.
5. Write the computed distance to a text file at `/home/user/result.txt`. The file should contain only the floating-point value rounded to exactly 4 decimal places.

Ensure you install any necessary Python or system packages if they are not already present (you can assume `sudo` is not needed if you use standard user-level pip installs, but system packages like `libhdf5-dev` are already installed).