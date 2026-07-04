You are a machine learning engineer preparing a dataset to train a Physics-Informed Neural Network (PINN). The network will learn heat diffusion over a discrete 1D ring graph topology. Before generating the massive training dataset, you need to ensure your numerical ODE solver converges properly and is optimized for parallel execution.

Your task is to write a C program that simulates this diffusion, parallelize it using OpenMP, and run a convergence study over different time steps.

**Requirements:**

1. **C Program (`/home/user/heat_ode.c`)**:
   - Simulates heat diffusion on a 1D ring graph with $N = 1000$ nodes using the Forward Euler method.
   - The governing ODE for each node $i$ is: 
     $\frac{dT_i}{dt} = \alpha (T_{i-1} - 2T_i + T_{i+1})$
     where $\alpha = 1.0$.
   - Since it's a ring graph, enforce periodic boundary conditions (node $0$ connects to node $N-1$, and node $N-1$ connects to node $0$).
   - **Initial Conditions:** At $t = 0.0$, node $0$ has a temperature of $1000.0$. All other nodes have a temperature of $0.0$.
   - **Time limits:** Simulate from $t = 0.0$ to $t = 1.0$ (inclusive).
   - **OpenMP:** Use OpenMP to parallelize the spatial loop (the loop over the $N$ nodes computing the derivative/next state).
   - **CLI Arguments:** The program must accept exactly one command-line argument: the time step `dt` (as a double).
   - **Output:** The program should print a single line to standard output in exactly this format: `dt=<dt>, T0=<final_temperature_of_node_0>` (e.g., `dt=0.010000, T0=45.123456`), using `%f` for both values.

2. **Convergence Testing Script (`/home/user/run_convergence.sh`)**:
   - Write a bash script that compiles `heat_ode.c` using `gcc` with OpenMP enabled (`-fopenmp`) and standard math libraries if needed. Name the executable `heat_ode`.
   - Run the compiled executable for the following three `dt` values: `0.1`, `0.01`, and `0.001`.
   - Redirect the output of these runs, in that exact order, to `/home/user/convergence.txt`.

Ensure your bash script has executable permissions and executes successfully, leaving the compiled binary and the `convergence.txt` file in `/home/user/`.