I am a researcher validating a numerical solver. I need you to write a parallel Python script using MPI to calculate the definite integral of the function \( f(x) = \frac{4}{1 + x^2} \) from \( x = 0 \) to \( x = 1 \). 

This integral analytically evaluates to \( \pi \). I want to validate our parallel integration approach by comparing the numerical result against this analytical reference.

Please do the following:
1. If necessary, install `openmpi-bin`, `libopenmpi-dev`, and the Python package `mpi4py`.
2. Write a Python script at `/home/user/integrate_mpi.py` that uses `mpi4py` to compute this integral using the **Midpoint Rule**. 
3. The script should take the total number of intervals `N` as a command-line argument (e.g., `python3 integrate_mpi.py 1000000`).
4. The script must divide the `N` intervals as evenly as possible among the available MPI ranks. 
5. Each rank should compute its local sum, and then use `comm.Reduce` to sum the total integral on rank 0.
6. On rank 0, compute the absolute difference (error) between the numerical result and the analytical solution (`math.pi`).
7. Rank 0 must write the final results to `/home/user/integration_output.txt` with exactly the following three lines:
   Numerical: <numerical_result>
   Analytical: <math.pi_value>
   Error: <absolute_error>

Once you have written the script, execute it using 4 MPI processes and \( N = 1000000 \) (one million) intervals:
`mpiexec --allow-run-as-root -n 4 python3 /home/user/integrate_mpi.py 1000000`

Ensure the script runs successfully and generates the `/home/user/integration_output.txt` file as specified.