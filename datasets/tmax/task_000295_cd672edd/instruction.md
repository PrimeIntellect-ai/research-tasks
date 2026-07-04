and <truth> Generation

```xml
<task>
You are a performance engineer tasked with profiling a legacy application. The system's legacy hardware monitor does not export digital logs for its baseline run; instead, it outputs a video recording of a load bar. We need to reconstruct the baseline statistics and build an automated anomaly detector.

Your objective is split into three phases:

**Phase 1: Observational Data Reshaping**
You have been provided with `/app/diagnostic_screen.mp4`. This video is 10 seconds long at 10 fps (100 frames total). Each frame shows a solid white region on a black background. The area of this white region (the exact number of white pixels) represents the CPU load for that moment in time. 
- Extract the video frames.
- Calculate the CPU load (white pixel count) for each frame.
- Save this time-series data to `/home/user/baseline_load.csv` (one integer per line).

**Phase 2: MCMC Sampling and Curve Fitting**
The baseline CPU load fluctuates but follows a normal distribution $\mathcal{N}(\mu, \sigma^2)$. 
- Write a C program `/home/user/mcmc_fit.c` that reads `baseline_load.csv`.
- Implement a Metropolis-Hastings MCMC sampler from scratch in C to estimate the posterior distributions of $\mu$ and $\sigma$. Assume uniform priors: $\mu \in [0, 500000]$ and $\sigma \in [1, 50000]$.
- Run the sampler for at least 50,000 iterations.
- Calculate the expected value (mean of the posterior samples after a suitable burn-in) for both $\mu$ and $\sigma$.
- Write these two values (space-separated, formatted to 2 decimal places: `[mu] [sigma]`) to `/home/user/baseline_params.txt`.

**Phase 3: Adversarial Classifier**
We are now streaming textual trace logs from various application instances. You must build a classifier to detect performance anomalies (e.g., CPU spikes from memory leaks).
- We have provided two corpora of trace files under `/app/traces/clean/` (normal behavior) and `/app/traces/evil/` (anomalous behavior).
- Write a C program `/home/user/trace_classifier.c` that compiles to `/home/user/classifier`.
- The classifier must accept exactly one CLI argument: the absolute path to a trace text file (which contains one integer CPU load per line).
- The classifier should read the trace file and use the $\mu$ and $\sigma$ derived in Phase 2. 
- If the trace contains ANY single load value strictly greater than $\mu + 4\sigma$, it should flag the trace as anomalous by exiting with status code `1`. Otherwise, it should accept the trace as normal by exiting with status code `0`.

Your final classifier will be tested against a holdout dataset, but you must ensure it successfully accepts 100% of the clean corpus and rejects 100% of the evil corpus provided in `/app/traces/`.