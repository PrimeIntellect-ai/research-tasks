You are a data scientist working on an embedded system where only standard POSIX shell tools (Bash, awk, bc, standard coreutils) are available. You need to fit a model to experimental data that follows an exponential decay process representing the analytical solution to the ODE $dy/dt = -ky$.

The dataset is located at `/home/user/decay_data.csv` and contains two comma-separated columns: `t` (time) and `y` (observed value). The first row is the header `t,y`.

The analytical solution to the system is $y(t) = y_0 e^{-kt}$.
We know from physical constraints that the initial value $y_0 = 5.0$ exactly. 

Your task is to write a Bash script `/home/user/optimize_k.sh` that determines the optimal decay constant $k$ by performing a 1D grid search optimization to minimize the Sum of Squared Errors (SSE) between the observed $y$ values and the predicted $y$ values ($5.0 e^{-kt}$). 

Requirements for `/home/user/optimize_k.sh`:
1. Use a grid search for $k$ starting from $0.00$ up to $1.00$ inclusive, with a step size of $0.01$.
2. For each $k$, calculate the SSE over all data points in `/home/user/decay_data.csv`. You may use `awk` or `bc` for the math. Note that `awk` has a built-in `exp()` function.
3. Identify the value of $k$ that yields the minimum SSE.
4. The script should output a single file `/home/user/model_params.txt` containing the best $k$ value in the exact format: `k=0.XX` (e.g., `k=0.42`).

You must run the script yourself and ensure that `/home/user/model_params.txt` is created with the correct answer before you finish.