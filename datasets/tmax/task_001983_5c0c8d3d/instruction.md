I am an ML engineer preparing a training dataset for a new protein dynamics model. We simulate protein motion by integrating a system of non-linear ordinary differential equations (ODEs) over the initial atomic coordinates extracted from PDB files. 

We are using a proprietary (but locally vendored) Python package for this called `vendored_bio_sim`, located at `/app/vendored_bio_sim`. Unfortunately, the latest version of this package has a bug: the numerical integrator diverges and fails to solve the ODE because someone hardcoded a wildly incorrect `first_step` size in the solver parameters, overriding the step-size adaptation.

Your task is to:
1. Identify and fix the deliberate perturbation in `/app/vendored_bio_sim/sim.py` so the ODE solver succeeds without diverging (removing the bad `first_step` parameter is sufficient).
2. Create and run a persistent HTTP server listening precisely on `127.0.0.1:8888`. You can use Flask, FastAPI, or Python's built-in `http.server`.
3. The server must expose a `GET /simulate` endpoint.
4. The endpoint must require an `Authorization: Bearer sim-token-42` header. If missing or invalid, return a 401 status code.
5. When a valid request is received, the endpoint must:
    - Use the fixed `vendored_bio_sim` to load the PDB file at `/app/data/input.pdb` and run the simulation.
    - Extract the initial X-coordinates of the atoms (returned by the parser) and the final X-coordinates of the atoms (returned by the simulation).
    - Compare the two probability distributions by calculating the 1st Wasserstein distance between the initial and final X-coordinates using `scipy.stats.wasserstein_distance`.
    - Return a JSON response with the structure: `{"distance": <float_value>}`.

Leave the server running in the background or foreground so that my verification script can issue real HTTP requests to it.