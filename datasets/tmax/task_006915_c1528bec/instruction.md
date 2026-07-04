You are a machine learning engineer preparing training data for a surrogate model that predicts the end-state of a chemical reaction based on its reaction rate. You need to simulate the reaction using a simple Ordinary Differential Equation (ODE) solver and compute a summary statistic of the resulting distribution.

Write a C++ program at `/home/user/generate.cpp` that does the following:
1. Simulates the ODE $dy/dt = -k \cdot y$ over the time interval $t \in [0, 10]$ with a time step of $dt = 0.01$ using the forward Euler method.
2. The initial condition is always $y(0) = 1.0$.
3. You need to run this simulation for $N = 1000$ different reaction rates $k$. The rates $k_i$ should be linearly spaced from $0.1$ to $1.0$ inclusive (i.e., $k_0 = 0.1$, $k_{999} = 1.0$).
4. Store the final value $y(10)$ for each simulation in a 1D array/vector.
5. You MUST parallelize the simulation loop over the $N$ reaction rates using OpenMP.
6. After all simulations complete, compute the sum of all the final $y(10)$ values.
7. Write ONLY this final sum to a file named `/home/user/result.txt`, formatted to exactly 4 decimal places.

Compile your program with OpenMP support (e.g., `g++ -O3 -fopenmp generate.cpp -o generate`) and run it to produce the `result.txt` file.