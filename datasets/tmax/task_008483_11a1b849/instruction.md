As a machine learning engineer, I am preparing synthetic training data for a new probabilistic model. I have a custom unnormalized probability density function (PDF) written in C, but I need to compute its normalization constant (the integral of the PDF) over a specific range to use it as a proper distribution. Since we're deploying this in a minimal environment, I need this done using standard Linux CLI tools and Bash.

Here is what you need to do:

1. **Environment Setup & Compilation:**
   - I have placed the C source code for the PDF evaluation at `/home/user/src/pdf_eval.c`. 
   - Compile this C program using `gcc` and output the executable to `/home/user/bin/pdf_eval`. Ensure it is linked with the math library (`-lm`). The executable takes a single numeric argument `x` and prints the evaluated PDF value $f(x)$.

2. **Numerical Integration (Trapezoidal Rule):**
   - Write a Bash script at `/home/user/scripts/integrate.sh`.
   - The script must compute the definite integral of the PDF from $x = -3$ to $x = 3$ using the **trapezoidal rule** with exactly $N = 1000$ equal-width intervals (i.e., 1001 evaluation points).
   - Use standard CLI tools (like `awk`, `bc`, `seq`, and your compiled `pdf_eval`) to do the math.
   - The script should output the final integrated value to a file at `/home/user/data/integral.txt`.

3. **Monte Carlo Area Estimation:**
   - Write a second Bash script at `/home/user/scripts/monte_carlo.sh`.
   - The script must estimate the same integral (area under the curve from $x=-3$ to $x=3$) using **Monte Carlo integration** (Rejection Sampling method).
   - The bounding box for the Monte Carlo simulation should be $x \in [-3, 3]$ and $y \in [0, 2]$.
   - Generate exactly $10,000$ uniformly distributed random points within this bounding box.
   - For each point $(x, y)$, use `pdf_eval` to get $f(x)$. If $y \le f(x)$, consider it a "hit".
   - Calculate the estimated area: $\text{Area} = \text{Total Bounding Box Area} \times \frac{\text{Hits}}{\text{Total Points}}$.
   - Save the estimated area to `/home/user/data/mc_area.txt`.

Ensure both scripts are executable. Do not use Python, R, or any other high-level languages for the scripts; rely entirely on Bash, `awk`, `bc`, and the provided C binary.