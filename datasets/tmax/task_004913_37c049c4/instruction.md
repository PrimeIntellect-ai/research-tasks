You are a data analyst tasked with estimating the true anomaly rate of a manufacturing process using historical sensor data. You will use a Bayesian Beta-Binomial conjugate model to compute the posterior distribution of the anomaly rate.

Your task is to write a C++ program `/home/user/analyze.cpp` that processes a messy dataset, enforces strict data schema rules, performs the Bayesian inference, and writes the validated model output to a file.

**Data Information:**
The input data is located at `/home/user/sensor_data.csv`. It has no header.
Each row represents a batch of sensor readings in the format:
`sensor_id,total_readings,anomalies`

**1. Data Schema Enforcement:**
The CSV contains malformed and invalid data. Your C++ program must parse the CSV and STRICTLY ignore any row that does not meet ALL of the following criteria:
- `sensor_id`: Must be a non-empty string.
- `total_readings`: Must be a strictly positive integer (> 0).
- `anomalies`: Must be a non-negative integer (>= 0).
- Logical constraint: `anomalies` cannot be greater than `total_readings`.
- The row must have exactly 3 columns. If parsing a numeric field fails, drop the row.

**2. Bayesian Inference:**
For the anomaly rate, we use a Beta-Binomial model. 
- The prior distribution for the anomaly rate is a Uniform distribution, which is equivalent to a Beta distribution with parameters: $\alpha_{prior} = 1$, $\beta_{prior} = 1$.
- Aggregate the data from all *valid* rows to find the total number of anomalies ($\sum anomalies$) and the total number of normal readings ($\sum (total\_readings - anomalies)$).
- Calculate the posterior Beta distribution parameters:
  $\alpha_{post} = \alpha_{prior} + \sum anomalies$
  $\beta_{post} = \beta_{prior} + \sum (total\_readings - anomalies)$
- Calculate the posterior mean: $\mu = \frac{\alpha_{post}}{\alpha_{post} + \beta_{post}}$
- Calculate the posterior variance: $\sigma^2 = \frac{\alpha_{post} \cdot \beta_{post}}{(\alpha_{post} + \beta_{post})^2 \cdot (\alpha_{post} + \beta_{post} + 1)}$

**3. Model Output Validation:**
Your C++ program must compile (e.g., using `g++ -O2 /home/user/analyze.cpp -o /home/user/analyze`) and run.
It must output the final metrics to a file exactly at `/home/user/results.csv` with the following format and strict rounding (use standard half-up rounding):
- `alpha`: integer
- `beta`: integer
- `mean`: rounded to exactly 6 decimal places.
- `variance`: rounded to exactly 8 decimal places.

The output CSV must include a header and look exactly like this:
```csv
metric,value
alpha,<value>
beta,<value>
mean,<value>
variance,<value>
```

Execute your program and ensure `/home/user/results.csv` is created correctly.