You are acting as a machine learning engineer preparing training data for a predictive model. We want to predict bacterial growth parameters directly from genetic sequences, but first, we need to extract the target labels (growth parameters) from noisy experimental data.

You have been provided with two files in your home directory:
1. `/home/user/strains.fasta`: Contains the genetic sequences of the bacterial strains being studied.
2. `/home/user/growth_data.csv`: Contains time-series spectroscopy data (OD600 optical density measurements) for these strains. The columns are `StrainID`, `Time` (in hours), and `OD600`.

Your task is to write and execute a Python script that does the following:
1. Parse `/home/user/strains.fasta` to identify the valid `StrainID`s.
2. For each valid strain, extract its corresponding time-series data from `/home/user/growth_data.csv`.
3. Model the bacterial growth using the Logistic Growth Ordinary Differential Equation (ODE):
   `dy/dt = r * y * (1 - y / K)`
   Where `y` is the OD600 at a given time, `r` is the growth rate, and `K` is the carrying capacity. 
   Assume the initial condition `y(0)` is exactly equal to the experimental OD600 measurement at `Time = 0.0` for that strain.
4. Use an optimization routine (e.g., `scipy.optimize.curve_fit` or `scipy.optimize.minimize` coupled with an ODE solver) to find the best-fitting parameters `r` and `K` that minimize the mean squared error against the noisy experimental data.
   - Constrain `r` to the bounds [0.01, 5.0] and `K` to [0.1, 5.0].
5. Output the extracted parameters to a CSV file located at `/home/user/training_features.csv`. The file must have a header `StrainID,r,K`, and the rows should be sorted alphabetically by `StrainID`. Round the `r` and `K` values to 3 decimal places.
6. Generate a single visualization saving it to `/home/user/growth_fits.png`. The plot should display the noisy experimental data as scatter points and the fitted ODE solutions as solid lines for all strains (you can use subplots or a single plot with a legend).

Please install any Python packages you need (like `scipy`, `pandas`, `matplotlib`, `biopython`) before running your script.