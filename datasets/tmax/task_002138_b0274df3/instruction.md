I am a data scientist trying to fit a dynamical model to some experimental data, but my parameter estimation step keeps failing because the design matrix is near-singular. I need you to write a complete Rust program from scratch that implements the fix, solves the resulting Ordinary Differential Equation (ODE), and visualizes the results.

Please create a Rust project in `/home/user/ode_fitter`.

**Phase 1: Parameter Estimation (Linear Equation Solving)**
We have a system governed by the parameters $\theta = [\theta_0, \theta_1, \theta_2]^T$.
Usually, we find $\theta$ using Ordinary Least Squares: $\theta = (X^T X)^{-1} X^T y$.
However, our $X$ matrix is near-singular. I need you to use Ridge Regression to regularize the inversion:
$\theta = (X^T X + \lambda I)^{-1} X^T y$

Use $\lambda = 0.05$.
Construct $X$ (a 5x3 matrix) and $y$ (a 5x1 vector) with the following hardcoded data:
$X = \begin{bmatrix} 1.0 & 2.0 & 2.001 \\ 1.0 & 3.0 & 3.002 \\ 1.0 & 4.0 & 4.001 \\ 1.0 & 5.0 & 5.003 \\ 1.0 & 6.0 & 6.002 \end{bmatrix}$
$y = \begin{bmatrix} 4.1 \\ 6.2 \\ 8.0 \\ 10.1 \\ 11.9 \end{bmatrix}$

Write Rust code to compute the regularized $\theta$. (You can use `ndarray` and `ndarray-linalg`).

**Phase 2: ODE Numerical Solving**
Once you have $\theta$, use it to solve the following ODE:
$\frac{du}{dt} = \theta_0 \cdot u + \theta_1 \cdot \sin(t) + \theta_2 \cdot \cos(t)$

Initial condition: $u(0) = 1.0$.
Time span: $t = 0.0$ to $t = 10.0$.
Use the forward Euler method with a step size of $\Delta t = 0.001$.

**Phase 3: Data Visualization and Output**
1. Save the final value of $u$ at $t = 10.0$ to a text file at `/home/user/ode_fitter/final_u.txt`. The file should contain only the floating-point number formatted to 4 decimal places (e.g., `12.3456`).
2. Plot the trajectory of $u(t)$ over time using the `plotters` crate. Save the plot as a PNG image at `/home/user/ode_fitter/trajectory.png` with dimensions 800x600. The plot should have a line series representing $u(t)$.

**Constraints & Requirements:**
- Everything must be written in Rust. You should initialize the cargo project and add the necessary dependencies.
- You must handle the `ndarray-linalg` dependencies correctly (e.g., using the `openblas` or `netlib` feature if necessary for LAPACK backend on Linux).
- Ensure the Rust code builds and runs successfully, producing the required files.