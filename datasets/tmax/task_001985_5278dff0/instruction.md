You are an AI assistant helping a materials researcher run a statistical simulation in Go.

The researcher has collected heat emission data $Q$ from a 10x10 spatial grid on a new composite material. For this material, the emission $Q$ is modeled by the non-linear equation:
$$Q = \alpha e^\alpha$$
where $\alpha$ is the localized heat retention coefficient of the material at a specific grid point.

The data is stored in a CSV file at `/home/user/data/grid.csv` (10 rows, 10 columns, comma-separated float values of $Q$).

Your task is to write and execute a Go program (`/home/user/simulate.go`) that does the following:
1. Parses the 2D grid of $Q$ values from `/home/user/data/grid.csv`.
2. Solves the non-linear equation $Q = \alpha e^\alpha$ to find $\alpha$ for each grid point. 
   - Use the Newton-Raphson method.
   - Use an initial guess of $\alpha_0 = 1.0$.
   - Iterate until $| \alpha_{n+1} - \alpha_n | < 1 \times 10^{-6}$.
   - Store the resulting $\alpha$ values in a multi-dimensional array (or a flattened slice representing the grid).
3. Computes the 95% bootstrap confidence interval for the **mean** of these 100 $\alpha$ values.
   - Use $B = 10,000$ bootstrap resamples.
   - To ensure reproducibility, instantiate a local random number generator with a specific seed: `r := rand.New(rand.NewSource(42))` (using `math/rand`).
   - Draw the bootstrap samples using this specific generator `r.Intn(100)` to pick indices.
   - Calculate the sample mean for each of the 10,000 resamples.
   - Sort the 10,000 means and use the percentile method to find the 95% confidence interval (i.e., the 2.5th percentile and the 97.5th percentile, corresponding to the 250th and 9750th elements in a 0-indexed sorted array).
4. Writes the lower and upper bounds of the confidence interval to `/home/user/alpha_ci.txt`, formatted exactly as `lower,upper` rounded to 6 decimal places (e.g., `1.123456,1.987654`).

Ensure your Go program is self-contained and handles file reading, numerical solving, array manipulation, and statistical bootstrapping. Execute the code so the output file is generated.