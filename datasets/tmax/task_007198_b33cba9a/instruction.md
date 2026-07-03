You are a Machine Learning Engineer preparing synthetic training data for a Physics-Informed Neural Network (PINN). The network will learn to solve the 1D Poisson equation. Before training, you need to generate a high-quality reference dataset using a traditional numerical method.

Your task is to write and execute a Python script at `/home/user/generate_data.py` that solves the 1D Poisson equation $u''(x) = -\pi^2 \sin(\pi x)$ on the domain $x \in [0, 1]$ with Dirichlet boundary conditions $u(0) = 0$ and $u(1) = 0$. The exact analytical solution is $u_{exact}(x) = \sin(\pi x)$.

The script must perform the following steps:
1. **Mesh Refinement & Convergence Testing:** 
   - Implement a standard second-order central finite difference scheme to solve the PDE.
   - Start with $N = 10$ intervals ($x_0 = 0, x_1, \dots, x_{10} = 1$, where $h = 1/N$).
   - Compute the numerical solution $u_{num}$ and compare it against the reference exact solution $u_{exact}$ at the grid points.
   - Calculate the maximum absolute error across all grid points.
   - If the maximum absolute error is greater than or equal to $1.0 \times 10^{-3}$, double the number of intervals $N$ (i.e., $N=20, 40, \dots$) and solve again. Repeat this until the maximum absolute error is strictly less than $1.0 \times 10^{-3}$.

2. **Experimental Data Visualization:**
   - Once convergence is reached, generate a line plot comparing your converged numerical solution and the exact solution. 
   - Save this plot to `/home/user/solution.png`.

3. **Output Generation:**
   - Save the converged numerical data to a CSV file at `/home/user/converged_data.csv`.
   - The CSV must contain exactly the following columns, with headers: `x`, `u_num`, `u_exact`, `error` (where `error` is the absolute difference between `u_num` and `u_exact`).
   - The CSV must include all grid points from the converged mesh, including the boundaries at $x=0$ and $x=1$.

You may need to install standard scientific Python libraries (like `numpy`, `scipy`, `matplotlib`, or `pandas`) via pip if they are not already installed. Create the script, run it to generate the files, and verify the outputs are correct.