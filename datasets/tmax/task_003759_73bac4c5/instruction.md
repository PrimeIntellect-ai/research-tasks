You are tasked with helping a data scientist fit an analytical 1D diffusion model to experimental data using a grid search. 

The experimental data is stored in an HDF5 file at `/home/user/experimental_data.h5`. This file contains three datasets:
- `/x`: A 1D array of spatial coordinates (float64).
- `/t`: A 1D array of time values (float64).
- `/u`: A 2D array of the observed concentrations (float64), with shape `(len(t), len(x))`.

The analytical model for the concentration is given by:
`u_model(x, t) = (A / sqrt(t)) * exp(-(x^2) / (4 * D * t))`

Your goal is to find the parameters `A` (amplitude) and `D` (diffusion coefficient) that minimize the Mean Squared Error (MSE) between the analytical model and the observed data `u` over all provided `(x, t)` pairs.

Requirements:
1. Write a C++ program (`/home/user/fit_model.cpp`) that reads the HDF5 data. You may need to install the appropriate HDF5 C++ development libraries using `apt`.
2. Implement a grid search over the parameters:
   - `A` ranges from `1.0` to `5.0` inclusive, with exactly 101 evenly spaced points (i.e., step size 0.04).
   - `D` ranges from `0.1` to `1.0` inclusive, with exactly 91 evenly spaced points (i.e., step size 0.01).
3. Use **OpenMP** to parallelize the evaluation of the grid search so it runs efficiently.
4. The program should compile and execute correctly.
5. Finally, write the best-fitting parameters and the minimum MSE to a file named `/home/user/best_parameters.txt`. The file must contain exactly one line with three space-separated numbers: `A D MSE`, formatted to exactly 4 decimal places.

Compile and run your code, then ensure `/home/user/best_parameters.txt` is created with the correct format.