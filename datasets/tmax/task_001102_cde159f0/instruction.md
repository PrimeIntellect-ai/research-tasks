You are tasked with fixing and integrating a multi-service distributed bioinformatics simulation system that models the pharmacokinetics of peptide sequences. The system is located in `/app/` and consists of a Node.js API gateway, a Python worker, and a Redis message broker.

Currently, the system is partially implemented, contains mathematical and logical bugs, and lacks security. Your objective is to fix the code, configure the services, and ensure the end-to-end workflow functions correctly.

Here are the requirements:

1. **System Architecture & Setup**
   - The system consists of three processes: a Redis server (port 6379), a Node.js API (`/app/api.js` on port 8080), and a Python worker (`/app/worker.py`).
   - You must install any necessary dependencies using `npm` and `pip` in the `/app/` directory and ensure all three services are running concurrently.

2. **Python Worker (`/app/worker.py`) - ODE Solving**
   - The worker reads peptide sequences from the Redis list `jobs` and must calculate the peak concentration of a metabolite using a 2-compartment pharmacokinetic model.
   - You need to implement the ODE system in the worker using `scipy.integrate.solve_ivp` (or `odeint`).
   - The model:
     `dA/dt = -k1 * A`
     `dB/dt = k1 * A - k2 * B`
   - Parameters:
     `k1 = (count of 'A' amino acids in sequence) * 0.1 + 0.05`
     `k2 = (count of 'B' or 'C' amino acids in sequence) * 0.05 + 0.02`
   - Initial conditions at `t=0`: `A = 100`, `B = 0`.
   - Time span: `t=0` to `t=50` with 1000 evaluated points.
   - The worker must find the maximum (peak) value of `B` and push a JSON string `{"sequence": "<seq>", "length": <len>, "peak_B": <max_B>}` to the Redis list `results`.

3. **Node.js API (`/app/api.js`) - Aggregation, Regression, and Fixes**
   - The API exposes a `POST /simulate` endpoint that accepts JSON: `{"sequences": ["AABBC", "ACCA", ...]}`.
   - **Security**: You must secure the API endpoint. It must reject requests without the exact HTTP header: `Authorization: Bearer bio-secret-2024`.
   - **Floating-point Reproducibility**: The API currently sums the `peak_B` results as they arrive asynchronously, leading to non-reproducible floating-point totals due to reduction order. You must fix `api.js` to collect all results first, **sort them alphabetically by the sequence string**, and then perform a standard sequential sum over `peak_B` to calculate `total_peak`.
   - **Linear Regression**: Calculate a simple linear regression mapping the independent variable (sequence `length`) to the dependent variable (`peak_B`). Compute the `regression_slope` and `regression_intercept`.
   - The endpoint must return:
     ```json
     {
       "total_peak": 123.456,
       "regression_slope": 1.23,
       "regression_intercept": 4.56
     }
     ```

4. **Visualization (`/app/plot.py`)**
   - Before the API returns the response, it must invoke `/app/plot.py` with the collected data.
   - Implement `/app/plot.py` to generate a scatter plot of `length` vs `peak_B` and draw the fitted regression line.
   - The plot must be saved exactly to `/home/user/plot.png`.

Leave the three services running in the background when you are done, so the automated verifier can test your API.