You are an MLOps engineer tasked with building a reproducible evaluation pipeline to track experiment artifacts for a Bayesian A/B test. 

You have been provided with raw clickstream logs in `/home/user/raw_events.jsonl`. 
Each line is a JSON object with `user_id`, `timestamp`, `event_type`, and `variant` ("A" or "B").

Your task is to create a complete, reproducible Python pipeline `/home/user/pipeline.py` that performs the following steps:

1. **Feature Engineering**: Parse `/home/user/raw_events.jsonl`. For each unique `user_id`, determine if they converted. A user is considered converted (1) if they have at least one event with `event_type` == "checkout". Otherwise, they are not converted (0). Keep track of which `variant` each user was assigned to.
2. **Bayesian Inference**: Model the conversion rates for Variant A and Variant B using a Beta-Binomial model. 
   - Assume a Uniform prior: Beta(1, 1) for both variants.
   - Calculate the posterior Beta distribution parameters for both A and B.
   - Using a random seed of `42`, draw exactly 1,000,000 samples from the posterior of A and the posterior of B using `numpy.random.beta`.
   - Calculate the probability that Variant B is strictly better than Variant A (i.e., sample_B > sample_A).
3. **Inference Performance Benchmarking**: Isolate the sampling step (drawing 1M samples for A and 1M samples for B, then comparing) into a distinct function. Use the `timeit` library to measure how long it takes to run this function 50 times.
4. **Numerical Library Configuration**: Ensure your script captures the active numerical thread configuration by reading the `OMP_NUM_THREADS` environment variable. 
5. **Artifact Tracking**: Save the final results to `/home/user/artifacts/experiment_results.json`. The JSON must have exactly this schema:
```json
{
  "variant_A_successes": int,
  "variant_A_failures": int,
  "variant_B_successes": int,
  "variant_B_failures": int,
  "prob_B_better_than_A": float, // Rounded to 4 decimal places
  "benchmark_time_seconds": float, // Total time for 50 runs
  "omp_threads": string // Value of OMP_NUM_THREADS env var, or "not_set"
}
```

**Constraints & Instructions:**
- Create the `/home/user/artifacts/` directory if it does not exist.
- Run your pipeline using: `OMP_NUM_THREADS=4 python3 /home/user/pipeline.py`
- You may use standard Python libraries and `numpy`. Install `numpy` if necessary.
- Ensure your script is reproducible. The exact value of `prob_B_better_than_A` depends on setting the numpy random seed to `42` *right before* your single draw of 1,000,000 samples in the main execution (you don't need to fix the seed for the timeit benchmarking loops).