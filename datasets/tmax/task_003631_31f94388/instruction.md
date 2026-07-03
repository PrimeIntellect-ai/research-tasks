You are a performance engineer investigating floating-point non-determinism in a parallel scientific simulation. The simulation computes the total energy of a system, but due to the non-associativity of floating-point arithmetic and unpredictable parallel reduction orders, the output varies slightly between runs.

Your goal is to compile the simulation, generate a dataset of these variations, and write a Rust-based statistical analysis tool to profile the distribution of the results.

Here are your steps:

1. **Compile the Simulation**: 
   There is a Rust project located at `/home/user/sim`. Compile it from source in release mode.

2. **Generate Data**:
   Run the compiled simulation 1000 times. Each run will print a single floating-point number to standard output. Save all 1000 numbers into a file at `/home/user/results.txt` (one number per line).

3. **Write the Analysis Tool**:
   Create a new Rust project at `/home/user/analyzer`. Write a program that reads `/home/user/results.txt` and computes the following:
   
   *   **Robust Mean (Equation Solving)**: Instead of a simple average, find the robust mean $\mu$ by finding the root of the equation: 
       $$f(\mu) = \sum_{i=1}^{N} \tanh(x_i - \mu) = 0$$
       Implement a root-finding algorithm (like Bisection or Newton-Raphson) to find $\mu$ to an accuracy of $10^{-5}$. Assume the root lies between the minimum and maximum of your dataset.
   
   *   **Bootstrap Confidence Interval**: Compute the 95% bootstrap confidence interval for the *simple sample mean* of the dataset. Use the percentile method with exactly 10,000 resamples. Use the `rand` crate with a standard RNG. (We will accept answers within a reasonable probabilistic tolerance).
   
   *   **Density Estimation**: Implement a Gaussian Kernel Density Estimator (KDE). Use a bandwidth of $h = 0.01$. The Gaussian kernel is $K(u) = \frac{1}{\sqrt{2\pi}} e^{-u^2/2}$. Evaluate the estimated density $f_{KDE}$ precisely at the **robust mean** ($\mu$) you calculated in the first step.

4. **Output Requirements**:
   Your analyzer must create a JSON file at `/home/user/analysis.json` with exactly the following structure:
   ```json
   {
     "robust_mean": 12.3456,
     "ci_lower": 12.3400,
     "ci_upper": 12.3500,
     "kde_at_mean": 4.5678
   }
   ```
   (Replace the numbers with your calculated `f64` values).

Ensure your analyzer compiles and runs successfully, producing the required JSON file.