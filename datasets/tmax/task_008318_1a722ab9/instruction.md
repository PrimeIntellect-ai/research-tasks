You are a performance engineer analyzing a physical simulation that frequently stalls due to ill-conditioned inputs. The simulation depends on finding the root time $x$ where the energy integral matches a target dissipation threshold. 

Your task is to build a C-based numerical solver and a shell-based orchestration pipeline to profile the distribution of these root times using bootstrap confidence intervals.

**Step 1: The Numerical Solver (`/home/user/solver.c`)**
Write a C program that reads `/home/user/dataset.csv`. The CSV contains 100 rows, each with 4 comma-separated floating-point numbers: `a, b, c, target`.
For each row, find the root $x > 0$ of the nonlinear equation:
$$ f(x) = \int_0^x (a t^2 + b t + c) \, dt - target = 0 $$

Your C program must:
1. Use the **Trapezoidal Rule** with exactly $N=1000$ intervals to compute the integral $\int_0^x$. (Do *not* use the analytical polynomial integral).
2. Use **Newton's Method** to find the root $x$. The derivative $f'(x)$ is simply the integrand evaluated at $x$: $a x^2 + b x + c$. 
3. Start with an initial guess of $x_0 = 1.0$. Iterate until $|f(x)| < 10^{-5}$ or a maximum of 50 iterations.
4. Print the final root $x$ for each row to standard output, one per line, formatted to 4 decimal places (e.g., `2.1532`).

**Step 2: Workflow Orchestration and Bootstrapping (`/home/user/orchestrate.sh`)**
Write a bash script that acts as your analytical workflow coordinator. It must:
1. Compile `solver.c` into an executable named `solver` using `gcc` and standard math libraries.
2. Run `solver` and save the 100 roots to a temporary file.
3. Perform a **Bootstrap Analysis** using standard shell tools (like `awk`, `sort`, `bash`) to find the 95% confidence interval of the **mean** of these roots.
    - Generate 1000 bootstrap samples. Each sample is created by randomly selecting 100 roots from your results *with replacement*.
    - Calculate the mean of each of the 1000 bootstrap samples.
    - Sort these 1000 sample means in ascending order.
    - The lower bound is the 25th value (index 25, 2.5th percentile).
    - The upper bound is the 975th value (index 975, 97.5th percentile).
4. Output the final confidence interval to `/home/user/ci_results.txt` in exactly this format:
```
Lower CI: 1.2345
Upper CI: 1.6789
```
*(Values should be rounded/formatted to 4 decimal places).*

**Constraints:**
- You may only use Bash built-ins, coreutils, and standard CLI tools (`awk`, `sed`, `grep`, `seq`, `shuf`, etc.) for the orchestration and bootstrapping. Do not use Python, R, or Perl.
- Ensure the orchestration script has executable permissions and can be run directly.