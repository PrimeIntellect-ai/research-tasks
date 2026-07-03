You are a bioinformatics analyst working on a sequence evolution project. Your team uses a custom nonlinear mathematical model to estimate the evolutionary divergence time ($t$) between two genetic sequences based on the observed mutation proportion ($p$). 

The model equation is:
$f(t) = 1 - e^{-0.5t} + 0.1t - p = 0$

Your tasks are:
1. **Nonlinear Equation Solving**: We have an incomplete C++ program at `/home/user/divergence_solver.cpp`. Complete the `solve_t(double p)` function using the Newton-Raphson method to find the root $t$ for a given $p$. 
   - The derivative of $f(t)$ with respect to $t$ is $f'(t) = 0.5e^{-0.5t} + 0.1$.
   - Use an initial guess of $t_0 = 1.0$.
   - The tolerance for convergence should be $10^{-6}$ (i.e., stop when $|f(t)| < 10^{-6}$).
   - Limit the solver to a maximum of 100 iterations.

2. **Data Processing**: Compile your program and run it against the input dataset `/home/user/sequence_data.txt` (which contains one $p$ value per line). The program should read this file and output the results to `/home/user/divergence_times.csv` in the format `p,t`, with `t` rounded to exactly 4 decimal places.

3. **Experimental Data Visualization**: Create a bash script at `/home/user/plot.sh` that reads `/home/user/divergence_times.csv` and generates an ASCII bar chart of the divergence times. 
   - For each line, output the $p$ value (exactly as it appears in the CSV), followed by a space, a pipe character `|`, a space, and a sequence of asterisks `*`.
   - The number of asterisks should be equal to the integer floor of $(t \times 10)$. For example, if $t = 1.5234$, print 15 asterisks.
   - Run the script and redirect the output to `/home/user/plot.txt`.

Ensure your C++ code handles standard edge cases and successfully compiles using `g++`.