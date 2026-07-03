You are acting as an AI assistant for a Machine Learning Engineer who is preparing a training dataset for a surrogate physics model. The raw data consists of sensor readings that must be inverted using a nonlinear equation to find the underlying physical state. After inversion, the distribution of these states must be statistically compared against a reference baseline to check for dataset shift.

Your task is to create a reproducible C++ pipeline that processes this data, solves the nonlinear equations, calculates distribution distance metrics, and outputs a statistical report.

**Task Requirements:**

1. **Workspace Setup:**
   - All your code should be placed in `/home/user/src`.
   - Your C++ source file must be named `/home/user/src/pipeline.cpp`.
   - Create a `Makefile` in `/home/user/src` that compiles `pipeline.cpp` into an executable named `process_data` using `g++` with `-O3 -std=c++17`.

2. **Input Data:**
   - Raw Data: `/home/user/data/raw_data.csv` (has a header `id,a,b,c`). Each subsequent line contains an integer `id` and three floating-point numbers `a`, `b`, and `c`.
   - Reference Data: `/home/user/data/ref_states.csv` (has a header `id,ref_x`). Each subsequent line contains an `id` and a floating point number representing a reference physical state.
   *(Assume these files already exist on the system).*

3. **Nonlinear Equation Solving:**
   - For each row in `raw_data.csv`, compute the physical state `x` by finding the root of the equation:
     `f(x) = a * exp(x) + b * x - c = 0`
   - Use the Newton-Raphson method.
   - The derivative is `f'(x) = a * exp(x) + b`.
   - Start with an initial guess of `x_0 = 0.0`.
   - Terminate when `|f(x)| < 1e-6` or after a maximum of 100 iterations.
   - Store the computed root `x` for each `id`.

4. **Statistical and Distribution Metrics:**
   - **Wasserstein-1 Distance ($W_1$):** Calculate the 1D Wasserstein distance between the empirical distribution of your computed `x` values and the `ref_x` values.
     Since the datasets have the exact same number of samples ($N$), you can compute this by sorting both arrays of states in ascending order and taking the mean absolute difference:
     $W_1 = \frac{1}{N} \sum_{i=1}^N |x_{sorted}[i] - ref\_x_{sorted}[i]|$
   - **Welch's T-Statistic ($t$):** Compute the T-statistic to compare the means of the computed `x` values and `ref_x` values:
     $t = \frac{\bar{x} - \bar{ref}}{\sqrt{\frac{s_x^2}{N} + \frac{s_{ref}^2}{N}}}$
     where $\bar{x}$ is the sample mean, and $s_x^2$ is the unbiased sample variance ($\frac{1}{N-1} \sum (x_i - \bar{x})^2$).

5. **Outputs:**
   - The compiled program must be executable via:
     `./process_data /home/user/data/raw_data.csv /home/user/data/ref_states.csv /home/user/data/processed.csv /home/user/data/report.txt`
   - **Processed Data (`processed.csv`):** Write the computed roots with the header `id,computed_x`. Output `computed_x` to 6 decimal places.
   - **Report (`report.txt`):** Write the calculated metrics exactly in this format (values rounded to 6 decimal places):
     ```
     Wasserstein Distance: <value>
     T-Statistic: <value>
     ```

Write the C++ program, create the Makefile, and execute the pipeline to generate `processed.csv` and `report.txt`.