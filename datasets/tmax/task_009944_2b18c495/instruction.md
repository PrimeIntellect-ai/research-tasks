You are a data scientist fitting statistical models to astronomical spectroscopy data. 

You have been given a spectrogram stored in an HDF5 file located at `/home/user/spectrogram.h5`. The file contains a single 2D dataset named `/signal` of 64-bit floating point numbers. The dataset dimensions are 100 rows (representing distinct wavelengths) by 50 columns (representing observational time steps).

Your task is to build a reproducible C++ data processing tool to extract summary statistics from this signal. 

Write a C++ program (e.g., `process_spectrogram.cpp`) that:
1. Reads the `/signal` dataset from `/home/user/spectrogram.h5`.
2. Computes the time-averaged spectrum: for each of the 100 wavelengths (rows), calculate the mean value across all 50 time steps (columns). This yields a 1D array of 100 time-averaged values.
3. Computes the global mean and the population variance of these 100 time-averaged values.
4. Writes these two final statistics to `/home/user/statistics.txt`.

The output file `/home/user/statistics.txt` must contain exactly two lines formatted to 2 decimal places:
Global Mean: <value>
Global Variance: <value>

You may use standard HDF5 C or C++ libraries (e.g., compile with `h5c++` or link against `-lhdf5`). Do not use any external analytical libraries (like Eigen or Armadillo) for the mathematical operations; write the standard algorithms yourself.