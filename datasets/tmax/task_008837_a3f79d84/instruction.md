You are an applied mathematics researcher analyzing an oscillatory decay function, specifically $f(x) = e^{-x} \sin(5x)$, representing a damped signal. You must write a Go program to perform numerical integration, mesh refinement, numerical differentiation, and bootstrap uncertainty estimation. 

Create a Go module and program at `/home/user/workspace/main.go` that does the following:

1. **Analytical Validation & Mesh Refinement:**
   - Define the domain $x \in [0, 2]$.
   - Start with $N = 4$ uniform intervals (step size $h = 0.5$).
   - Compute the numerical integral of $f(x)$ over $[0, 2]$ using the **Trapezoidal Rule**.
   - Compare this numerical integral to the exact analytical integral:
     $$ \int_0^2 e^{-x} \sin(5x) dx = \frac{5 - e^{-2}(\sin(10) + 5\cos(10))}{26} $$
   - **Refine the mesh:** Recursively double the number of intervals $N$ (halving $h$) until the absolute difference between the numerical integral and the exact analytical integral is strictly less than $10^{-4}$.

2. **Numerical Differentiation:**
   - Using the final, refined step size $h$ from Step 1, compute the numerical derivative of $f(x)$ at $x = 1.0$ using the central finite difference method: 
     $$ f'(1.0) \approx \frac{f(1.0 + h) - f(1.0 - h)}{2h} $$
   - Let's call this value `derivative_estimate`.

3. **Bootstrap Confidence Intervals:**
   - In physical measurements, the signal readings at $x = 1.0+h$ and $x = 1.0-h$ contain noise. 
   - Simulate a noisy dataset of 10,000 pairs of readings. Use Go's `math/rand` (seed it with `rand.Seed(42)`).
   - For each pair $i \in [1, 10000]$:
     - Generate noisy forward reading: $y_{fwd, i} = f(1.0 + h) + \epsilon_{fwd}$, where $\epsilon_{fwd} \sim \mathcal{N}(0, 0.05^2)$.
     - Generate noisy backward reading: $y_{bwd, i} = f(1.0 - h) + \epsilon_{bwd}$, where $\epsilon_{bwd} \sim \mathcal{N}(0, 0.05^2)$.
     - Compute the bootstrap derivative estimate $d_i = \frac{y_{fwd, i} - y_{bwd, i}}{2h}$.
   - Sort these 10,000 derivative estimates and find the 95% confidence interval using the percentile method (the 2.5th percentile and 97.5th percentile values).

4. **Output:**
   Write the final values to `/home/user/workspace/results.json` matching this exact structure:
   ```json
   {
     "refined_N": 0,
     "integral_error": 0.0,
     "derivative_estimate": 0.0,
     "ci_lower": 0.0,
     "ci_upper": 0.0
   }
   ```
   (Replace the zeros with your computed values as floating-point numbers/integers).

Ensure the output JSON is properly formatted. You should initialize the go module (`go mod init analyzer`), build, and run the program within the `/home/user/workspace` directory.