You are acting as a performance engineer optimizing a bottleneck in our scientific data processing pipeline. Our team analyzes 3D spatial probability density functions (PDFs) of particle distributions. 

Currently, our legacy code takes too long to compute the marginal distribution due to heavily nested `for` loops. Your task is to write a highly optimized, fully vectorized Python script to perform this operation.

You are provided with an input file at `/home/user/input_pdf.h5`. This HDF5 file contains a single dataset named `density` which is a 3D array of shape `(50, 50, 50)`. This array represents a probability density evaluated on a uniform spatial grid where $x, y, z \in [0, 1]$.

Your Python script must perform the following pipeline:
1. **Mesh Refinement (Interpolation):** Refine the grid resolution strictly along the Z-axis (the 3rd dimension, index 2). The original Z-axis has 50 uniformly spaced points from 0 to 1. You must linearly interpolate the data along the Z-axis to a new uniform grid of 99 points from 0 to 1. Do not loop over the X and Y axes; use multi-dimensional array operations (e.g., `scipy.interpolate` or `numpy` vectorization).
2. **Numerical Integration:** Compute the marginal probability distribution over the X-Y plane by integrating the refined 3D density array along the new Z-axis using the composite Trapezoidal rule.
3. **Output:** Save the resulting 2D array (which should have the shape `(50, 50)`) into a new HDF5 file located at `/home/user/marginal_xy.h5` under the dataset name `marginal`.

Requirements:
- Ensure you use `h5py` for scientific data I/O.
- The entire process must be vectorized. Explicitly looping over the 50x50 spatial grid in Python is forbidden for performance reasons.
- The output file must be written accurately as automated tests will assert the floating-point values in `/home/user/marginal_xy.h5`.