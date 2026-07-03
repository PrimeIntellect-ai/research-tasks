You are tasked with fixing a discrete numerical simulation pipeline used for fitting population dynamics models. Our architecture consists of three local services under `/app/`:
1. A Redis cache for intermediate distribution states.
2. A Flask API (`/app/api/`) that serves simulation results.
3. A Jupyter Notebook environment (`/app/notebooks/`) used by our data scientists for orchestrating workflows and comparing distributions.

Currently, the services are not communicating correctly because their configuration files and environment variables are misaligned. Furthermore, the core numerical integrator used by the API has a bug in its step-size adaptation logic, causing it to diverge and produce statistically invalid population distributions. 

Here is what you need to do:

**Phase 1: Multi-Service Orchestration**
- Inspect the services in `/app/`. You must launch all three services. 
- Adjust the environment variables and configuration files so that:
  - The Flask API correctly connects to Redis.
  - The Jupyter Notebook environment uses the Flask API as its backend (via the `SIMULATION_API_URL` environment variable).
- Verify the end-to-end flow: you should be able to trigger a simulation from a notebook script that hits the Flask API, caches in Redis, and returns the data.

**Phase 2: Statistical Validation**
- We have an empirical dataset of population distributions at `/app/data/empirical.csv`.
- Write a Python script (`/home/user/validate_distributions.py`) that fetches simulated data via the Flask API and uses probability distribution distance metrics (specifically the Kolmogorov-Smirnov test and Wasserstein distance) to compare the simulated distribution against the empirical data.
- Use analytical solution validation to prove the hypothesis that the current simulation diverges at $t > 50$ due to the step-size bug. Output a summary of your hypothesis testing to `/home/user/divergence_report.txt`.

**Phase 3: Fuzz Equivalence (The Fix)**
- We have provided a compiled, correct reference implementation (oracle) of the integrator at `/app/oracle/integrator_reference`. 
- You must write a standalone Python script at `/home/user/fixed_integrator.py` that implements the correct discrete numerical integration with proper step-size adaptation.
- Your script must take two command-line arguments: `<initial_state_json_path>` and `<output_json_path>`.
- The behavior of `/home/user/fixed_integrator.py` must be absolutely identical (bit-exact) to the oracle binary for any valid input parameters.