You are a data analyst working on processing sensor readings to determine the location of a stationary target. You have received a noisy dataset of coordinates in a CSV file, and you need to build a C-based reproducible data processing pipeline.

Your task is to implement a Bayesian update system that combines a prior belief with new sensor measurements to calculate the posterior mean of the target's 2D location.

The input file is located at `/home/user/data.csv`. It contains a header and an unknown number of rows.

**Data Schema & Enforcement:**
You must parse the CSV and strictly enforce this schema:
Column 1: `sensor_id` (integer)
Column 2: `x` (float)
Column 3: `y` (float)
Column 4: `variance` (float, strictly greater than 0)

Any row that does not perfectly match this schema (e.g., malformed numbers, missing columns, variance $\le 0$, or non-numeric strings) must be completely ignored. Do not crash; simply skip the invalid row.

**Bayesian Inference & Linear Algebra:**
Assume the target's $x$ and $y$ coordinates are independent.
- The prior belief of the location is a 2D Gaussian with mean $\mu_0 = (0.0, 0.0)$ and a prior covariance matrix $\Sigma_0 = \begin{pmatrix} 1.0 & 0.0 \\ 0.0 & 1.0 \end{pmatrix}$. The prior precision is $\Lambda_0 = \Sigma_0^{-1}$.
- Each valid measurement $i$ is a 2D Gaussian observation $z_i = (x_i, y_i)$ with a diagonal measurement covariance matrix $R_i = \begin{pmatrix} v_i & 0.0 \\ 0.0 & v_i \end{pmatrix}$, where $v_i$ is the `variance` from the CSV. The measurement precision is $\Lambda_i = R_i^{-1}$.
- Calculate the posterior precision matrix $\Lambda_n = \Lambda_0 + \sum_{i=1}^n \Lambda_i$.
- Calculate the posterior mean vector $\mu_n = \Lambda_n^{-1} \left( \Lambda_0 \mu_0 + \sum_{i=1}^n \Lambda_i z_i \right)$.

**Pipeline Requirements:**
1. Create a C program at `/home/user/processor.c` that reads `/home/user/data.csv`, performs the schema enforcement, calculates the posterior mean, and writes the result to `/home/user/posterior.txt`.
2. The output in `/home/user/posterior.txt` must be exactly a single line containing the posterior $x$ and $y$ means, separated by a comma, each formatted to exactly 4 decimal places (e.g., `1.2345,-0.6789`).
3. Create a `/home/user/Makefile` with the following targets:
    - `all`: compiles `processor.c` into an executable named `processor`.
    - `run`: executes `./processor` to generate `posterior.txt`.
4. Ensure your pipeline runs successfully by running `make all && make run`.