You are acting as a data scientist troubleshooting a matrix fitting pipeline. 

In `/home/user/pipeline/`, there is a C++ script named `mc_det.cpp` and an HDF5 data file named `matrix.h5`. The HDF5 file contains a single 3x3 near-singular covariance matrix under the dataset path `/model/covariance`.

The `mc_det.cpp` program is designed to take exactly 9 matrix elements as command-line arguments, run a 1000-iteration Monte Carlo simulation (injecting uniform noise to simulate measurement uncertainty), and print the determinant of the perturbed matrix for each iteration.

However, the pipeline is failing because:
1. The `mc_det.cpp` program suffers from numerical instability due to inadequate precision types used for the matrix elements and determinant calculations. It currently outputs `0.0000000000` or highly inaccurate values for the near-singular matrix.
2. The pipeline currently lacks the code to extract the data from the HDF5 file and process the Monte Carlo output.

Your task is to:
1. Fix `mc_det.cpp` so that it uses double-precision floating-point numbers (`double`) instead of single-precision (`float`) to avoid catastrophic cancellation. Do not change the random seed or the noise generation logic.
2. Compile the fixed C++ program.
3. Extract the 9 matrix values from `/home/user/pipeline/matrix.h5` (read them row by row).
4. Run the compiled C++ program using the extracted values as command-line arguments.
5. Compute the 95% bootstrap confidence interval of the determinant from the 1000 standard outputs (this means finding the 2.5th percentile and the 97.5th percentile of the sampled determinants. For 1000 samples, these are the 25th and 975th values when sorted in ascending order).
6. Save this confidence interval to `/home/user/pipeline/ci.txt` exactly in the format: `lower_bound,upper_bound`.

You may use standard CLI tools (like `h5dump`, `sort`, `sed`, `awk`, etc.) to extract the data and compute the percentiles.