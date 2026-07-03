You are a bioinformatics analyst processing continuous nanopore sequencing signals. You have been tasked with deploying a continuous signal-to-sequence alignment model as a microservice.

We use a specialized hybrid C/Python package for this, `nano_ode_aligner`, which models sequence matches using a continuous numerical integrator (ODE solver) to handle noisy, varying-speed nanopore translocations. The source code for this tool is vendored at `/app/nano_ode_aligner-2.1.0/`.

However, the package is currently broken in two ways:
1. The parallel computing setup is broken. The tool is supposed to use OpenMP for parallelizing the ODE integration, but compilation fails to link or utilize threads properly.
2. When running the compiled tool on highly variable signals, the numerical integrator diverges and produces `NaN` likelihoods. This is due to a flaw in the step-size adaptation logic in the solver when the error threshold is exceeded. You must find and fix this logic bug so the integrator correctly adapts.

Your tasks:
1. **Fix and Compile:** Inspect the source code and build files in `/app/nano_ode_aligner-2.1.0/`. Fix the step-size adaptation bug and the parallel compilation issue. Compile the package so the binary `nano_align` is successfully generated in the `bin/` directory.
2. **Signal Analysis & Hypothesis Testing:** You need to write a Python script that takes a raw signal (an array of floats) and uses the compiled `nano_align` to score the signal against two reference models:
   - `ref_H0.fasta` (Baseline hypothesis: Wild-type)
   - `ref_H1.fasta` (Alternative hypothesis: Structural variant)
   Calculate a simple likelihood ratio test. If the log-likelihood of H1 is strictly greater than H0 by a margin of 5.0, classify it as a variant.
3. **Service Deployment:** Create an HTTP service listening on `127.0.0.1:9090` using Python (e.g., using `http.server` or `Flask`). 
   - Endpoint: `POST /analyze`
   - Authentication: The service MUST require a header `X-Nano-Auth: spectro-secure-token`
   - Request body: JSON in the format `{"signal": [1.2, 0.9, 1.1, ...]}`
   - Response body: JSON in the format `{"variant": true/false, "log_ratio": float}`

Keep this service running in the background. Do not exit the terminal, as an automated system will send test requests to your service to verify your pipeline.