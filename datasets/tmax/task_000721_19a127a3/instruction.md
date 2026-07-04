You are acting as a Machine Learning Engineer preparing a robust data pipeline for training a surrogate model of a biological dynamical system. 

We use a known stiff ODE system (a variation of the Lotka-Volterra equations). Previously, we generated feature embeddings from this system's trajectories by fitting them to a quadratic curve using Ordinary Least Squares. However, the matrix factorization often failed on near-singular inputs when the biological parameters led to flat or rapidly decaying trajectories. 

To fix this, our team compiled a robust C binary (`/app/gen_oracle`) that uses Tikhonov regularization. Unfortunately, the source code was lost, and the binary is too slow for our new pipeline because it lacks parallelization.

Your task is to reverse-engineer the logic from the mathematical specification below and write a highly efficient, parallelized C program that replicates the oracle's output exactly, so we can replace it in our pipeline.

**Mathematical Specification:**
1. **ODE System:**
   $dx/dt = \alpha x - \beta xy$
   $dy/dt = \delta xy - \gamma y$
2. **Simulation:**
   Initial conditions: $x_0 = 2.0$, $y_0 = 1.0$.
   Integration: Forward Euler method.
   Time step: $\Delta t = 0.01$.
   Number of steps: 500 (so $t$ goes from $0.00$ up to $5.00$ inclusive).
3. **Feature Extraction (Curve Fitting):**
   Extract the $x$ trajectory: $(t_0, x_0), (t_1, x_1), \dots, (t_{500}, x_{500})$.
   Fit a quadratic curve $x(t) \approx c_0 + c_1 t + c_2 t^2$ using Least Squares.
   The normal equations are $(M^T M) c = M^T X$, where $M$ is a $501 \times 3$ matrix with rows $[1, t_k, t_k^2]$.
4. **Regularization (The Fix):**
   To prevent near-singular failure, add a Tikhonov regularization term $\lambda = 10^{-4}$ to the main diagonal of $M^T M$ before solving the $3 \times 3$ system for $c_0, c_1, c_2$.

**Implementation Requirements:**
* Your program must be written in C and saved at `/home/user/replicate_gen.c`.
* Compile it to `/home/user/replicate_gen`. You must use OpenMP for parallelization (e.g., `-fopenmp` and `#pragma omp parallel for`) and link against the math library (`-lm`).
* **Input format (stdin):** The first line is an integer $N$, the number of parameter sets. The next $N$ lines each contain four space-separated floats: `alpha beta gamma delta`.
* **Processing:** You must process the $N$ parameter sets in parallel using OpenMP.
* **Output format (stdout):** For each parameter set, output a single line with the 3 fitted coefficients: `c0 c1 c2`. The values must be formatted to 6 decimal places (`%.6f %.6f %.6f`). The output lines must perfectly match the original input order, despite the parallel processing.

You can test your implementation by comparing its output against `/app/gen_oracle`, which takes the exact same stdin format and produces the exact same stdout format.