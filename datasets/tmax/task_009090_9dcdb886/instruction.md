You are a data scientist validating a newly implemented network diffusion model written in Rust. The model simulates heat diffusion over a molecular graph structure using numerical integration.

You have the following files provided in your home directory (`/home/user`):
1. `/home/user/diffusion_model.rs`: The Rust source code for the simulation.
2. `/home/user/analytical_reference.csv`: A reference dataset containing the exact analytical solutions for the steady-state temperatures of the graph nodes.

Your task is to validate the simulation output against the analytical reference using command-line tools:

1. Compile the Rust model with maximum optimizations (`-C opt-level=3`).
2. The model uses a custom threadpool that requires the environment variable `NUM_OMP_THREADS` to be strictly set to `4` to correctly initialize the parallel graph partitioning engine.
3. Run the compiled model. It will output a single floating-point number per line representing the simulated temperature of each node in order.
4. Compare the model's output against `analytical_reference.csv` (which also contains one floating-point number per line).
5. Calculate the maximum absolute difference (error) between the simulated values and the reference analytical values across all corresponding nodes.
6. Write this single maximum absolute error, formatted to exactly 3 decimal places, to a new file at `/home/user/max_error.txt`.

You must accomplish this using only standard Linux shell built-ins and core utilities (e.g., `bash`, `awk`, `paste`, `rustc`).