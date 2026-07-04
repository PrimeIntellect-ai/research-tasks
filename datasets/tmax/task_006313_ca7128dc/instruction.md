You are a performance engineer profiling a numerical simulation engine. We need to evaluate the accuracy, stability, and performance of two different Ordinary Differential Equation (ODE) solvers (Forward Euler vs. Runge-Kutta 4) for a specific physical system before deploying it to production.

Your task is to write a C program that simulates an ensemble of systems, compares the probability distributions of their final states, and logs the profiling results.

**System Definition:**
The system is modeled by the following ODE:
`dy/dt = -20 * (y - t^2) + 2 * t`

**Simulation Requirements:**
1. **Ensemble:** You must simulate an ensemble of 1,000 independent runs.
2. **Initial Conditions:** The initial condition for the $i$-th run (where $i \in \{0, 1, \dots, 999\}$) is exactly `y(0) = 0.0 + (i * 0.001)`.
3. **Integration:** Integrate each system from `t = 0.0` to `t = 1.0` using a fixed step size of `h = 0.04` (which means exactly 25 integration steps per run).
4. **Solvers:** You must implement both the **Forward Euler** method and the standard 4th-order **Runge-Kutta (RK4)** method. Run the full ensemble of 1,000 initial conditions through *both* solvers independently. 

**Analysis Requirements:**
1. **Numerical Stability:** Analyze if the Forward Euler method is numerically stable for this specific ODE at the given step size `h = 0.04`. (Use standard linear stability analysis for the homogeneous part of the ODE).
2. **Distribution Distance:** We want to measure the divergence between the results of the two solvers. Let $Y_{Euler}$ be the set of the 1,000 final values `y(1.0)` produced by the Euler method, and $Y_{RK4}$ be the set of final values produced by RK4. Calculate the 1-Wasserstein distance (Earth Mover's Distance) between these two empirical 1D distributions. 
   *(Hint: Because the initial conditions are uniformly spaced and the ODE preserves ordering, both arrays of final values will naturally be sorted. For two sorted arrays of equal size $N$, the 1-Wasserstein distance is simply the average of the absolute differences between corresponding elements: $\frac{1}{N} \sum_{i} |a_i - b_i|$).*

**Deliverables:**
1. Write your C program to `/home/user/profile_ode.c`.
2. The program must use double-precision floating-point numbers (`double`) for all calculations.
3. Compile and execute the program.
4. Your program must create an output file at `/home/user/profile_results.txt` with exactly the following format:
```
Euler_stable: [yes/no]
W1_distance: [value rounded to 6 decimal places]
```

Example of the output format:
```
Euler_stable: yes
W1_distance: 0.001234
```

Ensure your C code compiles cleanly with standard GCC and does not require any external libraries other than the standard C library (and `-lm` for math if needed).