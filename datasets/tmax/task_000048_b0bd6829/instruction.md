You are an AI assistant helping a computational researcher set up an automated simulation workflow. The researcher is performing a convergence study (mesh refinement) for a 1D Poisson equation solver, validating it against an analytical solution, and orchestrating the runs using parameterized Jupyter notebooks.

Here is your task:

1. **Environment Setup**:
   Create a Python virtual environment at `/home/user/sim_env`.
   Install the necessary packages: `numpy`, `scipy`, `jupyter`, and `papermill`.

2. **Numerical Solver (`/home/user/solver.py`)**:
   Write a Python module that solves the 1D Poisson equation: $u''(x) = -4\pi^2 \sin(2\pi x)$ on the domain $x \in [0, 1]$ with Dirichlet boundary conditions $u(0) = 0$ and $u(1) = 0$.
   - The analytical solution is $u_{exact}(x) = \sin(2\pi x)$.
   - Implement a standard second-order central finite difference scheme.
   - Discretize the domain into $N$ equal intervals (i.e., $N+1$ points including boundaries, so step size $h = 1/N$).
   - Create a function `get_l2_error(N)` that builds the $(N-1) \times (N-1)$ system for the interior points, solves it, and returns the discrete $L_2$ error.
   - Calculate the discrete $L_2$ error using the formula: $E = \sqrt{ h \sum_{i=1}^{N-1} (u^{num}_i - u^{exact}(x_i))^2 }$.

3. **Notebook Template (`/home/user/template.ipynb`)**:
   Create a Jupyter notebook programmatically (you can write a short Python script to generate this `.ipynb` file using the `nbformat` library, or create it manually as a valid JSON struct).
   - The notebook must have a cell tagged with `parameters` that defines a single variable: `N = 10`.
   - The notebook must import `solver`, call `solver.get_l2_error(N)`, and write the resulting float value to a file located at `/home/user/results/error_{N}.txt`.

4. **Workflow Orchestration (`/home/user/run_study.sh`)**:
   Write a bash script that:
   - Activates the virtual environment.
   - Creates the `/home/user/results/` directory.
   - Uses `papermill` to execute `template.ipynb` for $N \in \{16, 32, 64, 128\}$. Save the output notebooks in `/home/user/results/` as `out_{N}.ipynb`.
   - After all `papermill` runs complete, reads all the generated `error_{N}.txt` files and compiles them into a single CSV file at `/home/user/results/convergence.csv`.
   - The CSV must have exactly this format:
     ```csv
     N,L2_error
     16,<error_for_16>
     32,<error_for_32>
     64,<error_for_64>
     128,<error_for_128>
     ```

Run your setup and ensure `/home/user/run_study.sh` executes successfully from start to finish and produces the correct `convergence.csv` file.