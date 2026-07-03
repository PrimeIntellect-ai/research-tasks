You are a performance engineer tasked with processing a large dataset of raw spectroscopic signals. The data processing needs to be heavily optimized to run in a short amount of time, requiring parallelization.

A raw signal file is located at `/home/user/data/signal.bin`. It contains exactly 1,000,000 `f32` values in little-endian binary format representing an intensity spectrum $Y[k]$ for $k = 0, \dots, 999,999$.

Your objective is to write a highly parallel Rust program to analyze this spectrum, smooth it, find the dominant peak, and fit a simple analytical model to the peak using a grid search optimization.

Here are the exact requirements:

1. **Create a Cargo Project**:
   Initialize a new Rust project at `/home/user/spectra_optimizer`.
   You may use external crates like `rayon` for parallelization, `bytemuck` for reading binary data, or `serde_json` for output. 

2. **Signal Smoothing (Moving Average)**:
   Apply an 11-point moving average to the signal to compute the smoothed spectrum $S[k]$:
   $S[k] = \frac{1}{11} \sum_{j=-5}^{5} Y[k+j]$
   *Boundary Condition*: Only compute $S[k]$ for indices $k \in [5, 999994]$. For all other indices, assume $S[k] = 0.0$.

3. **Peak Identification**:
   Find the index $k_{max}$ that maximizes the smoothed signal $S[k_{max}]$. If there is a tie, pick the smallest index. Let this peak value be $S_{max}$.

4. **Model Fitting via Parallel Grid Search**:
   Extract a local window around the peak: $j \in [-50, 50]$. You will fit a Gaussian-like model to this local window:
   $M(j, \alpha) = S_{max} \cdot \exp\left(-\frac{j^2}{\alpha^2}\right)$
   
   Define the Error function $E(\alpha)$ as the Sum of Squared Errors (SSE) over this window:
   $E(\alpha) = \sum_{j=-50}^{50} (S[k_{max} + j] - M(j, \alpha))^2$

   Perform a grid search to find the parameter $\alpha$ that minimizes $E(\alpha)$. 
   Test exactly 1,000,000 evenly spaced values of $\alpha$ in the range $[0.1, 10.0]$.
   Specifically: $\alpha_i = 0.1 + i \times \frac{9.9}{999999}$ for $i = 0, 1, \dots, 999999$.
   
   **Constraint**: You MUST parallelize this grid search. Use the `rayon` crate to compute the errors across the 1,000,000 candidate $\alpha$ values in parallel.

5. **Output**:
   Write the final results to `/home/user/result.json` in the following format:
   ```json
   {
       "k_max": <integer>,
       "s_max": <float rounded to 4 decimal places>,
       "best_alpha": <float rounded to 4 decimal places>,
       "min_error": <float rounded to 4 decimal places>
   }
   ```

Build your application in release mode (`cargo build --release`) and run it. The file `/home/user/result.json` must be present and correctly populated when you are finished.