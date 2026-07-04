You are a data scientist cleaning up and analyzing inference benchmark logs from a distributed machine learning pipeline. 

You have two datasets containing inference requests processed by two different microservices, located at:
1. `/home/user/service_A_logs.csv`
2. `/home/user/service_B_logs.csv`

Each file has the header `req_id,latency_ms`.

Your task:
1. **Join and Clean the Data:** Find all inference requests (`req_id`) that successfully passed through *both* services. Compute the total end-to-end latency for each of these requests (Total Latency = Latency A + Latency B).
2. **Bootstrap CI Calculation (C++):** Write a C++ program at `/home/user/bootstrap.cpp` to perform statistical bootstrap sampling on the joined total latency data to find the 95% confidence interval of the mean end-to-end latency. 

**Bootstrap Requirements:**
- Perform exactly `10,000` bootstrap iterations.
- In each iteration, sample with replacement from your joined dataset. The size of the sample must equal the size of the joined dataset.
- Calculate the mean of each bootstrap sample.
- Sort the 10,000 means in ascending order.
- The 95% confidence interval bounds are the 2.5th percentile and the 97.5th percentile. Use indices `250` and `9750` (assuming 0-indexed arrays) of the sorted means array to get the lower and upper bounds, respectively.
- **Reproducibility:** You *must* use standard C++ pseudo-random number generation with a fixed seed to ensure your answer can be verified. Use exactly:
  ```cpp
  std::mt19937 gen(42);
  std::uniform_int_distribution<> dist(0, N - 1); // where N is the number of joined records
  ```
  Draw the indices for your samples in a sequential loop (iterate over the bootstrap samples 0 to 9999, and inside that, iterate 0 to N-1 to pick elements).

**Final Output:**
Compile and run your C++ program. Have it write the final confidence interval to `/home/user/ci_output.txt` in exactly this format (rounded to 2 decimal places):
`Lower: [val], Upper: [val]`

Example format:
`Lower: 45.12, Upper: 47.89`