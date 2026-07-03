You are an AI assistant helping a computational researcher simulate a coupled nonlinear dynamical system. You need to build a reproducible pipeline in **Go** that finds the initial conditions by solving a nonlinear algebraic system, simulates the system's time evolution, and validates it against the analytical steady state.

Your final goal is to generate a reproducible JSON report. 

**Phase 1: Initial Condition Finding (Nonlinear System)**
The system's initial state $(x_0, y_0)$ is defined as the positive root (where $x > y > 0$) of the following system of nonlinear equations:
1) $x^2 + y^2 - 10 = 0$
2) $x \cdot y - 3 = 0$

Write a 2D Newton-Raphson solver from scratch in Go to find this root. Use $(x, y) = (4.0, 0.5)$ as your initial guess. Iterate until the magnitude of the step is less than $10^{-6}$.

**Phase 2: ODE Numerical Simulation**
Using the root $(x_0, y_0)$ found in Phase 1 as the initial condition at $t = 0$, simulate the following system of Ordinary Differential Equations (ODEs):
* $\frac{dx}{dt} = -0.5x + 0.1y^2$
* $\frac{dy}{dt} = 0.2xy - 0.6y$

Implement the classic **Runge-Kutta 4th order (RK4)** method in Go to integrate this system from $t = 0$ to $t = 50.0$ using a fixed time step of $\Delta t = 0.01$.

**Phase 3: Analytical Validation**
The ODE system above has a non-trivial, strictly positive steady state (fixed point) where $\frac{dx}{dt} = 0$ and $\frac{dy}{dt} = 0$ (and $x > 0, y > 0$). Calculate this analytical steady state $(x_{ss}, y_{ss})$ directly in your code using algebraic substitution.

**Phase 4: Output Generation**
Your Go program should output a JSON file at `/home/user/simulation_results.json` containing the precise results of these phases. The file must strictly follow this format (example values shown):

```json
{
  "initial_root_x": 0.0000,
  "initial_root_y": 0.0000,
  "simulated_final_x": 0.0000,
  "simulated_final_y": 0.0000,
  "analytical_ss_x": 0.0000,
  "analytical_ss_y": 0.0000
}
```

**Constraints & Rules:**
* Use **Go** as your primary language for the computation. Create a directory `/home/user/sim` and write your Go code there (e.g., `main.go`).
* Use only the standard library (`math`, `encoding/json`, `os`, etc.). No external mathematics or scientific computing libraries (like gonum) are permitted.
* Write a `Makefile` or `run.sh` script in `/home/user/sim` that builds and runs the Go code to produce the JSON file.