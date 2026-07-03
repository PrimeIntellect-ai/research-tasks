You are a machine learning engineer preparing training data. You need to verify if a new batch of sampled data matches the distribution of your large reference dataset. To do this, you will evaluate the convergence of the Total Variation Distance (TVD) as the sample size increases.

Write a Go program `/home/user/evaluate_distribution.go` that does the following:
1. Accepts three command-line arguments: `<reference_file>`, `<sample_file>`, and `<seed>` (an integer).
2. Reads the floats (one per line) from the reference and sample files. All values are guaranteed to be between 0.0 and 1.0 inclusive.
3. Initializes a random number generator using the provided `<seed>` (`math/rand` with `NewSource`).
4. Shuffles the sample data using this seeded random generator (using `rand.Shuffle`).
5. For subset sizes $N = 100, 200, 300, \dots, 1000$ (in increments of 100):
   a. Take the first $N$ elements from the *shuffled* sample data.
   b. Compute the empirical probability distribution of the *full* reference data and the $N$-element sample subset by binning the values into 10 equal-width bins: `[0.0, 0.1), [0.1, 0.2), ..., [0.9, 1.0]`. (If a value is exactly 1.0, place it in the last bin).
   c. Calculate the Total Variation Distance (TVD) between the two distributions. Let $P$ be the reference distribution and $Q$ be the subset sample distribution. $TVD = 0.5 \times \sum_{i=1}^{10} |P_i - Q_i|$.
   d. Print to standard output a CSV line: `N,TVD`, where TVD is formatted to exactly 6 decimal places (e.g., `100,0.045000`).

Next, create a reproducible bash script `/home/user/pipeline.sh` that:
1. Compiles or runs the Go program.
2. Executes it with the files `/home/user/reference.txt` and `/home/user/sample.txt`, using `42` as the seed.
3. Redirects the output to `/home/user/tvd_convergence.csv`.
4. Includes a header `N,TVD` at the top of the CSV file.

The files `/home/user/reference.txt` (10,000 lines) and `/home/user/sample.txt` (1,000 lines) already exist on your system.