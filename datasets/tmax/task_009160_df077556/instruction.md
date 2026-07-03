You are acting as a data scientist tasked with fitting a Lotka-Volterra predator-prey model to a reference dataset of population measurements.

The Lotka-Volterra equations are:
dx/dt = α*x - β*x*y
dy/dt = δ*x*y - γ*y

Where:
- x is the prey population
- y is the predator population
- α (alpha), β (beta), γ (gamma), and δ (delta) are model parameters.

You have been provided with a reference dataset at `/home/user/reference_data.csv`. This file has the header `t,x,y` and contains population measurements from t=0.0 to t=50.0 in increments of dt=0.1.

Your task is to build a reproducible pipeline to find the best-fitting parameters using a grid search:
1. Write a C++ program named `/home/user/lv_fit.cpp` that takes exactly 5 command-line arguments: `alpha`, `beta`, `gamma`, `delta`, and `path_to_reference_csv`.
2. The C++ program must solve the Lotka-Volterra ODEs using the standard 4th-order Runge-Kutta (RK4) method with a time step of dt=0.1 from t=0.0 to t=50.0 (501 points including t=0).
3. The initial conditions are x(0) = 40.0 and y(0) = 9.0.
4. The C++ program must compute the Mean Squared Error (MSE) between the simulated populations and the reference populations. The MSE is defined as the average of ((x_sim - x_ref)^2 + (y_sim - y_ref)^2) across all 501 time steps.
5. The C++ program should print ONLY the calculated MSE to standard output as a floating-point number.
6. Compile the C++ program using g++.
7. Write a Bash script `/home/user/grid_search.sh` that iterates over the following parameter grid:
   - α (alpha): 1.0, 1.5, 2.0
   - β (beta): 0.5, 1.0, 1.5
   - γ (gamma): 2.0, 3.0, 4.0
   - δ (delta): 0.5, 1.0, 1.5
8. The bash script must execute the C++ program for all 81 combinations and identify the parameter set that minimizes the MSE.
9. Finally, write the best parameters to a file named `/home/user/best_params.txt`. The file must contain exactly one line with the four parameters and the minimum MSE, separated by commas, in this format: `alpha,beta,gamma,delta,MSE`

Do not use any external libraries in C++ other than the standard library (e.g., `<iostream>`, `<fstream>`, `<vector>`, `<cmath>`, `<string>`).