You are an bioinformatics data scientist optimizing a new isothermal amplification assay. You need to identify a consensus primer from several viral variants and fit a kinetic ODE model to experimental fluorescence data.

We have a local microservice architecture under `/app/` that provides the lab data and evaluates your models.
Services:
1. `redis` (Port 6379) - Used for caching by the APIs.
2. `lab_api` (Port 8000) - Serves the sequence and experimental data.
3. `evaluator_api` (Port 8001) - Evaluates your final model parameters.

Your tasks:

1. **Service Configuration**: 
   The startup script `/app/start_services.sh` is broken. The `lab_api` and `evaluator_api` fail to connect to redis because they expect the environment variable `REDIS_HOST` to be set, but it is missing. Fix the script, start the services, and ensure they are running on their respective ports.

2. **Primer Design**:
   Query `http://localhost:8000/sequences` to get 5 aligned viral DNA sequences (JSON format). 
   Write a Python script to compute the 20-bp consensus sequence from the very beginning of the alignment (positions 0 to 19). The consensus should use the most frequent base at each position. Calculate the GC content (percentage 0.0 to 100.0) of this 20-bp consensus primer.

3. **ODE Modeling and Fitting**:
   Query `http://localhost:8000/kinetics` to retrieve experimental time-series data. It returns a JSON object with `time` (array of time points) and `fluorescence` (array of observed amplicon concentrations).
   
   Our amplification kinetics follow this system of ODEs:
   dP/dt = -k_1 * P * A
   dA/dt = k_1 * P * A - k_2 * A
   
   Where:
   - P is the Primer concentration
   - A is the Amplicon concentration (Fluorescence)
   - k_1 is the forward binding rate
   - k_2 is the decay rate

   Initial conditions at t=0:
   - P(0) = GC_content (the percentage you calculated in step 2, e.g., 45.0)
   - A(0) = 0.01

   Write a Python script using `scipy.integrate.solve_ivp` and `scipy.optimize.minimize` (or `curve_fit`) to find the optimal parameters `k_1` and `k_2` that minimize the Mean Squared Error (MSE) between the simulated `A(t)` and the experimental `fluorescence` data at the given time points. 
   Bounds for k_1 and k_2 are [0.001, 1.0].

4. **Submission**:
   Submit your fitted parameters via a POST request to `http://localhost:8001/submit` with JSON payload:
   `{"k1": <float>, "k2": <float>, "gc_content": <float>}`
   
   The evaluator will return an MSE score. You must achieve an MSE < 0.05.
   Save the exact JSON response from the evaluator to `/home/user/submission_result.json`.