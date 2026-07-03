You are an ML engineer preparing training data for a new protein folding dynamics model. We have a pipeline that simulates protein backbone dynamics from PDB files using a custom numerical integration library called `prot_integrator`, computes bootstrap confidence intervals of the pairwise distance fluctuations, and serves the curated dataset to our training infrastructure via a REST API.

Unfortunately, our vendored simulation package `prot_integrator` is currently broken. When run on our raw PDB files, the numerical integrator diverges. A previous engineer mentioned this is likely due to a hardcoded step-size adaptation bug in the vendored package. 

Your task consists of the following steps:

1. **Fix the vendored package**: The source code for `prot_integrator` version 1.2.0 is located at `/app/prot_integrator`. Find and fix the bug causing the integrator to diverge. You will need to build/install it into your Python environment after fixing it.
2. **Process the data**: We have a set of PDB files in `/home/user/data/pdbs/`. For each PDB file, run the fixed `prot_integrator.simulate(pdb_path, steps=1000)` which returns a 2D numpy array of pairwise atomic distance fluctuations.
3. **Statistical Analysis**: For each resulting array, compute the 95% bootstrap confidence interval of the mean fluctuation across all atomic pairs. Use 1000 bootstrap samples.
4. **Serve the Data**: Expose the processed data via an HTTP server. The server must listen on `127.0.0.1:8080`.
    - Endpoint: `GET /api/v1/stats?pdb=<pdb_id>`
    - Response: JSON format `{"pdb_id": "<pdb_id>", "ci_lower": <float>, "ci_upper": <float>}`.
    - Authentication: The server must require a Bearer token: `Authorization: Bearer dev_token_99x`. Return a 401 Unauthorized if the token is missing or incorrect.
5. **Orchestration**: Write a Jupyter Notebook `/home/user/workflow.ipynb` that documents this pipeline. The notebook should contain cells that import the package, run the simulation on `1A2B.pdb`, compute the CI, and print the results.

Please start the HTTP server in the background and ensure it stays running so our training infrastructure can fetch the data.