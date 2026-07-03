You are acting as a data scientist working on a spectroscopy analysis pipeline. 

In your home directory (`/home/user`), you will find two files:
1. `spectra.h5`: An HDF5 file containing a dataset named `dataset` with dimensions 1000x500 (1000 samples of 500-bin spectral signals).
2. `analyze_spectra.cpp`: A C++ program that reads the HDF5 file, computes the mean spectrum across all 1000 samples, subtracts this mean from the data, and performs a Singular Value Decomposition (SVD) using the Eigen3 library to extract the principal components.

**The Problem:**
The pipeline is exhibiting non-reproducible results. Every time we compile and run `analyze_spectra.cpp`, the leading singular value changes slightly in the 5th or 6th decimal place. This flaky behavior is wreaking havoc on our downstream density estimation and distribution fitting tests. 

We suspect the issue lies in how the mean spectrum is being computed. The previous developer used OpenMP atomic additions on floating-point numbers, which introduces non-deterministic floating-point reduction order, leading to non-associative rounding errors.

**Your Objectives:**
1. Identify and fix the non-determinism in `/home/user/analyze_spectra.cpp`. You must ensure the mean spectrum is calculated in a strictly deterministic manner (e.g., by removing the atomic operation and performing a stable, sequential sum, or a deterministic parallel reduction).
2. The compilation requires Eigen3 and HDF5. You can compile it using:
   `g++ -O3 -fopenmp -I/usr/include/eigen3 -I/usr/include/hdf5/serial analyze_spectra.cpp -L/usr/lib/x86_64-linux-gnu/hdf5/serial -lhdf5 -o analyze_spectra`
3. Run the compiled program.
4. Extract the deterministic leading (first) singular value printed by the program, and save it to a file at `/home/user/svd_result.txt`. The file should contain *only* this numeric value, rounded to exactly 5 decimal places (e.g., `123.45678`).

*Note: You may need to install standard development libraries (`libhdf5-dev`, `libeigen3-dev`) if they are not already present in your environment, using `sudo apt-get` if necessary, though assume the system administrator has pre-installed them for this task context.*