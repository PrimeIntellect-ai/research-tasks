You are assisting a computational physics researcher. They have a C++ simulation script located at `/home/user/sim/equilibrium_sim.cpp` that calculates the thermal equilibrium state of a system using a Newton-Raphson nonlinear equation solver.

The simulation computes an aggregate system density over millions of micro-states. However, the researcher is pulling their hair out: every time they run the simulation, it converges to a slightly different equilibrium root! They suspect that the variations are due to floating-point reduction order during parallel execution, causing non-reproducible summation rounding errors that compound during the Newton-Raphson iterations. 

Your task is to:
1. Identify and fix the non-deterministic parallel reduction bug in `/home/user/sim/equilibrium_sim.cpp` so that the results are exactly reproducible across multiple runs (i.e., strict sequential ordering or an order-independent exact summation). 
2. Compile the fixed code. Note: The codebase relies on standard C++17 parallel algorithms, so you may need to link against TBB (`-ltbb`).
3. Perform a convergence test: run the compiled simulation 50 times. Calculate the variance of the 50 outputted equilibrium values to ensure it is exactly `0.0` (indicating a perfectly reproducible Dirac delta distribution of results).
4. Save the single, reproducible equilibrium value to `/home/user/sim/converged_result.txt`, formatted to exactly 6 decimal places.

Do not alter the mathematical formula of the density or the Newton-Raphson update logic—only fix the non-reproducibility of the summations.