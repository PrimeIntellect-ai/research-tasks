You are acting as a computational physics assistant for a researcher studying atmospheric entry. We have experimental trajectory data of a probe falling through the atmosphere, and we need to determine the aerodynamic drag coefficient $c$ of the probe.

The probe's vertical motion is governed by the following system of Ordinary Differential Equations (ODEs):
$dy/dt = v$
$dv/dt = -g - (c/m) \cdot v \cdot |v|$

Where:
- $y$ is the height (meters)
- $v$ is the velocity (meters/second, negative for falling)
- $g = 9.81$ m/s$^2$ (acceleration due to gravity)
- $m = 10.0$ kg (mass of the probe)
- $c$ is the unknown drag coefficient.

We have a reference dataset located at `/home/user/trajectory_data.csv` containing two columns: `time` (in seconds) and `height` (in meters).

Your task is to:
1. Write a C++ program (e.g., `optimize_drag.cpp`) that numerically integrates the ODEs using the **Forward Euler method** with a fixed time step of $dt = 0.01$ seconds.
2. The initial conditions at $t=0$ are $y = 1000.0$ m and $v = 0.0$ m/s.
3. The program should read the reference dataset and implement an optimization algorithm (like grid search or gradient descent) to find the optimal drag coefficient $c$ (accurate to at least two decimal places) that minimizes the Mean Squared Error (MSE) between the simulated heights and the reference heights at the corresponding timestamps.
4. The true value of $c$ is known to be between 0.10 and 1.00.
5. Compile your C++ code from source using `g++` and run the simulation.
6. Write the single optimal value of the drag coefficient $c$ (formatted to two decimal places, e.g., `0.XX`) to `/home/user/optimal_c.txt`.

Do not use any external libraries other than the standard C++ library (e.g., `<iostream>`, `<fstream>`, `<vector>`, `<cmath>`).