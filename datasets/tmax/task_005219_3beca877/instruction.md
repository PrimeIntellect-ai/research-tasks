You are an AI assistant helping a data scientist debug and run a statistical model fitting pipeline.

We are fitting a parameterized model to a reference dataset. The model evaluates a numerical integral to make predictions, and we are using gradient descent to find the optimal parameters `a` and `b`. 

The Rust project is located in `/home/user/model_fitter`. You can compile it using standard Cargo commands. 

Currently, the code has a critical flaw: the gradient and loss calculation uses multithreading where threads add their partial results to a shared `Mutex<f64>`. Because thread scheduling is non-deterministic, the floating-point reduction order changes on every run. This causes the objective function to jitter due to floating-point roundoff differences, which prevents the gradient descent from converging reliably.

Your tasks are:
1. Examine `/home/user/model_fitter/src/main.rs`.
2. Modify the loss and gradient computations so that they are strictly deterministic and reproducible. You must ensure that the summation of floating-point numbers occurs in a fixed, predictable order (e.g., sequentially by data index).
3. Compile the scientific software from source (use `--release` for performance).
4. Run the optimization against the reference dataset `/home/user/dataset.csv`.
5. The program will output the final optimized parameters once convergence is achieved. 
6. Create a log file at `/home/user/optimized_params.txt` containing the final parameters in exactly this format, rounded to 2 decimal places:
`a=<value>,b=<value>`

Note: The dataset has no noise, so the gradient descent should converge to the exact integer or simple fractional parameters used to generate the reference dataset.