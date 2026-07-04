As a data scientist, you are analyzing a set of observations and need to fit a linear model to the data. 

An HDF5 file is located at `/home/user/observation.h5`. It contains two 1D datasets of 64-bit floats (`f64`) at the root level: `x` and `y`.

Write and execute a Rust program that performs the following:
1. Reads the `x` and `y` datasets from the HDF5 file.
2. Fits a simple linear regression model $y = mx + c$ using the ordinary least squares method.
3. Calculates the slope ($m$) and intercept ($c$).
4. Saves the results to `/home/user/fit_result.txt` on a single line, formatted as `m,c` where both values are rounded to exactly 4 decimal places (for example: `2.1234,0.5678`).

Create your Rust project in `/home/user/fit_model` and use the `hdf5` crate to read the data.