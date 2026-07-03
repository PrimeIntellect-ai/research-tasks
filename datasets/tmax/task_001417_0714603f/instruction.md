You are acting as a data scientist working on a spectroscopy project. You have been given a codebase that processes spectroscopic data, computes the power spectrum using FFT, and calculates a specialized metric. However, the automated regression tests are failing unpredictably.

Your workspace is located at `/home/user/project`.

Here are your tasks:

1. **Fix the Floating-Point Reduction Issue**:
   The script `/home/user/project/fit.py` contains a function `compute_metric` that computes a sum over FFT values with alternating signs. To simulate parallel accumulation, the indices are shuffled before summation. Because standard floating-point addition is not strictly associative, this random order leads to non-reproducible results and causes `/home/user/project/test_fit.py` to fail.
   Modify `compute_metric` in `fit.py` to use a numerically stable summation method (e.g., `math.fsum`) so that the function returns the exact same result regardless of the shuffle order. Do not remove the alternating sign logic or the shuffling logic—just change how the final sum is accumulated to guarantee strict reproducibility.

2. **Implement NetCDF Export**:
   Complete the `save_to_netcdf(input_h5, output_nc)` function in `fit.py`. This function should:
   - Read the 2D dataset named `spectra` from the provided HDF5 file (`input_h5`).
   - Compute the absolute values of the real FFT (`np.abs(np.fft.rfft(row))`) for each row.
   - Save this resulting 2D array to a new NetCDF4 file at `output_nc`.
   - The NetCDF file must contain dimensions `row` and `freq`, and a 2D variable named `power_spectrum` (of type `f8` / float64) containing the computed data.

3. **Verify**:
   - Run the test suite: `pytest /home/user/project/test_fit.py` to ensure your fix works.
   - Execute your completed `save_to_netcdf` function to process `/home/user/project/data.h5` and output the result to `/home/user/project/output.nc`. You can do this by running `python -c "from fit import save_to_netcdf; save_to_netcdf('data.h5', 'output.nc')"` in the project directory.

Ensure that `/home/user/project/output.nc` is created correctly and the tests pass.