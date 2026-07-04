You are a computational chemistry researcher working on chemical kinetic simulations. You recently ran a large batch of numerical ODE simulations on a computing cluster, but a failing memory module on the cluster corrupted several of the output files. You need to build a programmatic filter to distinguish physically valid simulation trajectories from corrupted ones.

You have a scanned image of your lab notebook located at `/app/system_specs.png`. This image contains the governing Ordinary Differential Equations (ODEs) for the reaction network, the specific rate constants, and the expected initial mass conservation law.

Your tasks are to:
1. Extract the ODE formulas, rate constants, and conservation laws from `/app/system_specs.png` (you may use `tesseract` or Python's `pytesseract` to read it).
2. Write a Python script `/home/user/evaluate_sim.py` that takes a single argument: the path to a CSV file containing a simulation trajectory.
3. The script must validate the CSV data against the theoretical model extracted from the image by:
   - Verifying that the analytical conservation law holds at all time steps (within a tolerance of 1e-3).
   - Re-simulating the ODEs numerically using the extracted rate constants and the initial conditions found in the first row of the CSV.
   - Calculating the residuals between the CSV data and your numerical solution. 
   - Performing density estimation/distribution fitting on the residuals. Valid simulations have purely zero-mean Gaussian observational noise ($\sigma \approx 0.02$). Corrupted simulations may exhibit biased noise, uniformly distributed noise, or sudden physical discontinuities.
4. Your script `evaluate_sim.py` must exit with code `0` if the simulation is valid (accept), and exit with code `1` if the simulation violates any physical or statistical properties (reject).

The CSV files have the columns: `time`, `A`, `B`, `C`.

To help you develop and test your filter, a small set of known-valid simulation runs are provided in `/app/data/training_good/` and a small set of known-corrupted runs are in `/app/data/training_corrupted/`. 

Once you are done, an automated verifier will evaluate your `/home/user/evaluate_sim.py` script against a hidden holdout dataset of valid and corrupted simulations. Your script must successfully accept all valid simulations and reject all corrupted ones.