You are a performance engineer tasked with debugging a numerical simulation written in Rust. 

The application in `/home/user/ode_sim` is a custom numerical integrator that solves a system of Ordinary Differential Equations (ODEs) of the form dy/dt = -M * y. 
The initial state y(0) is determined by solving L * y(0) = b, where L is the lower triangular matrix from the Cholesky decomposition of the symmetric positive-definite matrix M.

Currently, the application is failing. When you run it, the step-size adaptation diverges, causing the simulation to either panic or produce `NaN` values. The original author attempted to implement an adaptive Heun-Euler scheme (an embedded Runge-Kutta method), but made a critical algorithmic error in how the new step size is calculated based on the local truncation error estimate.

Your task:
1. Navigate to `/home/user/ode_sim`.
2. Analyze `src/main.rs` and identify the logical flaw in the step-size adaptation formula.
3. Fix the step-size controller so that the step size *decreases* when the error is too high, and *increases* when the error is very low. (Assume standard RK error control logic: `h_new = h_old * (TOL / err)^(0.5)`).
4. Run the fixed simulation.
5. The program prints the final state vector at `t = 0.5`. Save this exact console output to `/home/user/result.txt`.

Ensure the final result file contains only the space-separated output of the vector (e.g., `0.123 -0.456 0.789`).