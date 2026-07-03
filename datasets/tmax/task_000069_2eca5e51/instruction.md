You are an MLOps engineer tasked with maintaining an experiment tracking pipeline for a physical binomial trial (e.g., an automated coin-flipping robot). 

We have two main objectives:

**Part 1: ETL & Video Analysis**
An experiment run has been captured in `/app/experiment.mp4`. The video consists of solid color frames: pure white (`#FFFFFF`) representing a "Success" and pure black (`#000000`) representing a "Failure".
1. Extract the frames from `/app/experiment.mp4`.
2. Count the exact number of Successes and Failures in the video.
3. Write these counts to `/home/user/video_results.json` in the following format:
```json
{
  "successes": <int>,
  "failures": <int>
}
```

**Part 2: Adversarial Artifact Filtering (C++)**
Our MLOps system receives thousands of artifact JSONs from distributed edge devices reporting experiment results. Unfortunately, some logs are corrupted, manipulated, or suffer from numerical instability (e.g., NaNs, negative counts, or mathematically incorrect Bayesian posterior updates).

A valid artifact JSON looks like this:
```json
{
  "experiment_id": "exp_101",
  "successes": 45,
  "failures": 105,
  "prior_alpha": 1.0,
  "prior_beta": 1.0,
  "posterior_mean": 0.304635,
  "posterior_variance": 0.001393
}
```
For a Beta-Binomial conjugate prior setup, the exact posterior updates are:
- `alpha_post = prior_alpha + successes`
- `beta_post = prior_beta + failures`
- `posterior_mean = alpha_post / (alpha_post + beta_post)`
- `posterior_variance = (alpha_post * beta_post) / [((alpha_post + beta_post)^2) * (alpha_post + beta_post + 1)]`

You must write a C++ program `artifact_filter.cpp` in `/home/user/` and compile it to `/home/user/artifact_filter`.
Your program must accept a single command-line argument (the path to a JSON file):
`./artifact_filter <path_to_json>`

It must parse the JSON and strictly enforce the following:
1. `successes` and `failures` must be non-negative integers.
2. `prior_alpha` and `prior_beta` must be strictly greater than 0.
3. `posterior_mean` and `posterior_variance` must not be NaN or Infinity.
4. The provided `posterior_mean` and `posterior_variance` must numerically match the true calculated values (based on the formulas above) to within an absolute tolerance of `1e-4`.

If the JSON is completely valid and numerically accurate, your program must exit with code `0`.
If the JSON violates ANY of the rules above, or is malformed, your program must exit with code `1`.

You can test your filter against the directories provided in `/app/corpus/clean/` (which should all exit 0) and `/app/corpus/evil/` (which should all exit 1). (You may need to write a quick bash script to loop over them for testing).