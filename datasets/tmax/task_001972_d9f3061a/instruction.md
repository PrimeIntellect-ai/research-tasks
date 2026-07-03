You are an MLOps engineer tasked with analyzing a set of model experiments to find efficient, similarly-architected models while tracking the performance of the similarity search itself.

You have been provided a dataset of experiment metrics and descriptions at `/home/user/experiments.csv`.

Your goal is to write a Go program that processes this data, computes a lightweight custom "embedding" for each model description, calculates similarities using linear algebra, and benchmarks the similarity computation.

Perform the following steps:
1. Initialize a Go module named `mlops` in `/home/user/mlops`.
2. Write a Go program at `/home/user/mlops/analyze.go`.
3. The program must read `/home/user/experiments.csv`.
4. For each experiment, compute a 5-dimensional "embedding" vector based on its `Description`. The vector consists of the counts of the vowels `[a, e, i, o, u]` (case-insensitive) in the description text.
5. Use the `gonum.org/v1/gonum/mat` package to compute the Cosine Similarity between the embedding vector of the baseline experiment (`EXP-001`) and all other experiments (including itself).
6. Filter the experiments to find those that meet BOTH of the following criteria:
   - Latency_ms is strictly less than 50.
   - Cosine Similarity to `EXP-001` is greater than or equal to 0.85.
7. Write the IDs of the matching experiments (one per line, sorted alphabetically) to `/home/user/similar_experiments.txt`.
8. Benchmark the similarity calculation: Inside your Go program, isolate the mathematical cosine similarity computation for all rows against EXP-001 (do not include string parsing, file I/O, or vector creation in the benchmark). Run this pure mathematical computation loop 100,000 times.
9. Write the total duration of the benchmark loop in milliseconds (just the integer or float value, e.g., `45.2`) to `/home/user/benchmark_result.txt`.

Ensure your Go program downloads necessary dependencies and executes successfully to produce the required output files.