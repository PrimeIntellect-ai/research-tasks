You are a data scientist tasked with fitting a linear model to experimental data. 

We have collected data from a recent experiment, stored in an HDF5 file at `/home/user/experiment.h5`. 
This file contains two datasets:
- `/design_matrix`: A 2D array of size 50x4 representing the input features $X$.
- `/observations`: A 1D array of size 50 representing the target values $y$.

Your task is to:
1. Extract the data from the HDF5 file. You may use a short Python script to extract the data into a more accessible format if you prefer, or read it directly in C++.
2. Write a C++ program named `/home/user/solve.cpp` that uses the Eigen library to compute the Ordinary Least Squares (OLS) solution $\hat{\beta}$ for the model $y = X\beta$. You must use QR decomposition to solve this system.
3. Compile and run your C++ program to produce a file `/home/user/beta.txt` containing the 4 estimated coefficients (one per line, in the order of the features, formatted to 4 decimal places).
4. Compute the residuals $r = y - X\hat{\beta}$ (this can be done in your C++ program or a subsequent script) and save them to `/home/user/residuals.txt` (one per line, 50 lines).
5. Create a visualization of the residuals by writing and executing a script that generates a scatter plot or histogram of the residuals. Save the plot as `/home/user/residuals.png`.

The system has `python3`, `h5py`, `matplotlib`, and `libeigen-dev` installed. Include the path `/usr/include/eigen3` when compiling your C++ code.