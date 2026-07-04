You are assisting a researcher investigating the numerical stability and convergence of finite difference methods.

Your task is to build a reproducible computation pipeline that calculates the derivative of a function, compares it against the analytical reference dataset (the exact theoretical derivative), and tests for numerical stability by finding the point where floating-point round-off error overtakes truncation error.

Step 1: Write a C program at `/home/user/finite_diff.c`
- The program must compute the forward finite difference approximation of the derivative of $f(x) = \sin(x)$ at $x = \pi/4$.
- Use `double` precision for all calculations. Use `3.14159265358979323846` for $\pi$.
- The exact derivative is $\cos(\pi/4)$.
- Iterate through step sizes $h = 10^{-i}$ for $i$ from $1$ to $16$ (inclusive).
- For each step size, compute the approximation: `approx = (sin(x + h) - sin(x)) / h`
- Compute the absolute error compared to the exact derivative: `error = fabs(approx - cos(x))`
- The program should print a CSV header: `h,approx,error`
- For each $h$, print the values to standard output using the format string `"%e,%.16e,%.16e\n"`.

Step 2: Create a Bash pipeline script at `/home/user/pipeline.sh`
- The script must compile `finite_diff.c` using `gcc` (remember to link the math library with `-lm`) into an executable named `finite_diff`.
- It must run the executable and redirect the output to `/home/user/results.csv`.
- It must then parse `/home/user/results.csv` (ignoring the header) to find the row with the smallest `error` value.
- Finally, it must extract the $h$ value from that row and save it (just the $h$ string, exactly as formatted in the CSV) to `/home/user/best_h.txt`.

Step 3: Execution
- Make the script executable and run it so that `/home/user/results.csv` and `/home/user/best_h.txt` are generated.