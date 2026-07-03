You are a performance engineer analyzing the numerical stability of a set of randomly generated matrices processed in a distributed system. Your task is to write a Go program that simulates parallel matrix processing, computes the condition numbers via Singular Value Decomposition (SVD), and calculates a bootstrap confidence interval for the mean condition number.

Write a Go program at `/home/user/analyze_svd.go` that performs the following steps:
1. Initialize a random number generator using `math/rand.New(math/rand.NewSource(42))`.
2. Generate 200 matrices of size 30x30. For each matrix, populate its elements sequentially (row by row, column by column) using `rand.Float64()`. Generate all 200 matrices sequentially in a loop first to ensure deterministic generation.
3. Distribute the computation of the SVD for these 200 matrices across exactly 4 parallel worker goroutines. Use the `gonum.org/v1/gonum/mat` package to compute the SVD (`mat.SVD`).
4. For each matrix, calculate its condition number, defined as the ratio of the largest singular value to the smallest singular value. Collect all 200 condition numbers.
5. Wait for all workers to finish, then sort the 200 collected condition numbers in ascending order.
6. Calculate the mean of these 200 condition numbers.
7. Compute the 95% bootstrap confidence interval for the mean of the condition numbers. 
   - Use exactly 10,000 bootstrap resamples.
   - Initialize a new random number generator for the resampling using `math/rand.New(math/rand.NewSource(99))`.
   - For each resample, draw 200 items with replacement from the sorted condition numbers using `rand.Intn(200)`, and compute the mean. Do this sequentially for the 10,000 resamples.
   - Sort the 10,000 resampled means in ascending order.
   - The 95% CI lower bound is the value at index 250 (the 2.5th percentile) and the upper bound is the value at index 9750 (the 97.5th percentile).
8. Write the original mean, CI lower bound, and CI upper bound to a JSON file at `/home/user/results.json` with the keys `"mean"`, `"ci_lower"`, and `"ci_upper"`.

You will need to initialize a Go module and fetch the required dependencies in `/home/user`.
Run your program to produce the `/home/user/results.json` file.