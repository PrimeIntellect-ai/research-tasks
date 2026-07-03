You are an AI assistant helping a bioinformatics researcher analyze protein simulations. The researcher has a workflow that extracts B-factors from protein structures, compares their distributions, and serves the statistical results via a local API. 

However, the internal parsing library they use is currently broken, and the analysis API needs to be implemented.

Here are your instructions:

1. **Environment & Package Setup**:
   - You have a pre-created Python virtual environment at `/app/venv`. Always use this environment.
   - There is a vendored package located at `/app/vendored_bio_struct_parser`. It contains a `Makefile` used for installation, but the `install` target is broken due to a deliberate typo in the command. 
   - Fix the `Makefile`, then install the package into the virtual environment.

2. **Data Processing**:
   - You are provided with two PDB files: `/app/data/proteinA.pdb` and `/app/data/proteinB.pdb`.
   - Use the newly installed `bio_struct_parser` library to parse these files. The library provides a function `parse_pdb(filepath)` which returns a list of dictionaries, each representing an atom.
   - Filter the parsed atoms to extract the `b_factor` values exclusively for atoms where `atom_name == "CA"` (Alpha Carbons) for both proteins. Keep them as 1-dimensional numpy arrays.

3. **Statistical Analysis**:
   - Perform a two-sample Kolmogorov-Smirnov (KS) test to compare the CA B-factor distributions of Protein A and Protein B (using `scipy.stats.ks_2samp`).
   - Fit a Gaussian Kernel Density Estimate (KDE) to the CA B-factors of each protein separately (using `scipy.stats.gaussian_kde`).

4. **API Service**:
   - Implement an HTTP server in Python listening exactly on `127.0.0.1:8080`.
   - The server must handle the following `GET` requests and return valid JSON with a `200 OK` status:
     - `GET /ks_test`
       Response format: `{"stat": 0.1234, "pvalue": 0.0567}` (Use the exact statistic and p-value from your KS test).
     - `GET /density/<protein_id>/<b_factor>`
       (e.g., `GET /density/proteinA/22.5` or `GET /density/proteinB/30.1`)
       Response format: `{"density": 0.0456}` (The value of the KDE evaluated at that specific B-factor for the requested protein).

Run your server so it remains active (you can leave it running in the foreground of a terminal session or run it in the background). An automated verifier will make HTTP requests to `127.0.0.1:8080` to evaluate your API.