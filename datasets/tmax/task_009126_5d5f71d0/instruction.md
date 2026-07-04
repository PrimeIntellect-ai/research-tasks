You are a performance engineer analyzing execution traces of a distributed microservice. You need to estimate the probability of the service experiencing execution times within a specific latency window using Kernel Density Estimation (KDE) and numerical integration. 

You must implement this analysis entirely using Bash shell scripts and standard POSIX tools (like `awk`, `bc`, `sed`). Do not use Python, R, or other high-level languages.

**Environment Setup:**
You have four trace files located in `/home/user/traces/`: `trace_1.txt`, `trace_2.txt`, `trace_3.txt`, and `trace_4.txt`. Each file contains 50 floating-point execution times (one per line).

**Phase 1: Density Estimation (KDE)**
Write a script `/home/user/kde.sh` that takes two arguments: an input file path and a target value `x`. It should output the estimated probability density $\hat{f}(x)$ at that point.
* Use a Gaussian kernel: $K(u) = \frac{1}{\sqrt{2\pi}} e^{-u^2 / 2}$ (use `2.506628` for $\sqrt{2\pi}$).
* Use a fixed bandwidth of $h = 0.5$.
* Formula: $\hat{f}(x) = \frac{1}{n h} \sum_{i=1}^n K\left(\frac{x - x_i}{h}\right)$, where $n$ is the number of lines in the file, and $x_i$ is each execution time.

**Phase 2: Numerical Integration**
Write a script `/home/user/prob.sh` that integrates your KDE over a range to find a probability. It should take four arguments: `<input_file> <start> <end> <steps>`.
* Use the left-endpoint Riemann sum for numerical integration.
* $\Delta x = \frac{\text{end} - \text{start}}{\text{steps}}$.
* Area $\approx \sum_{j=0}^{\text{steps}-1} \hat{f}(\text{start} + j \Delta x) \cdot \Delta x$.
* The script must print *only* the final integrated value, rounded to 4 decimal places (e.g., `0.1234`).

**Phase 3: Parallel Execution and Orchestration**
Write a master script `/home/user/analyze.sh` that runs `prob.sh` for all four trace files **in parallel** (using Bash background jobs `&` and `wait`).
* Calculate the probability that the execution time falls between `2.0` and `5.0` (using `100` steps).
* Save the results in `/home/user/results/probs.txt`.
* The final output file must have exactly four lines in the format: `trace_N.txt: <value>` (e.g., `trace_1.txt: 0.3142`), sorted alphabetically by filename.

Ensure your scripts are executable. The automated test will simply execute `/home/user/analyze.sh` and evaluate the contents of `/home/user/results/probs.txt`.