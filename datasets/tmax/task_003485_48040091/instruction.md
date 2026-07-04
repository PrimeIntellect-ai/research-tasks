You are a data engineer tasked with building a high-performance C-based transformation step for an ETL pipeline. This pipeline processes a stream of binary sensor events and performs an iterative Bayesian update to calculate the probability of an underlying system fault. 

We have encountered a persistent issue in our previous pandas-based pipeline: missing data (represented as specific integer codes) was silently converting integer columns to float NaNs and corrupting downstream state. Your C implementation must explicitly handle this missing data propagation exactly as specified.

The specification for the mathematical parameters and control codes is provided in an image artifact left by the data science team at `/app/bayes_spec.png`. You will need to extract the text from this image (e.g., using `tesseract`) to obtain the required constants for your program.

**Program Requirements:**
1. Write a C program that reads a stream of integers from `stdin` (one integer per line).
2. The program must maintain a running Bayesian posterior probability $P(H)$ where $H$ is the hypothesis that the system is faulty. The prior probability and the likelihoods $P(D=1|H)$ and $P(D=1|\neg H)$ are written in `/app/bayes_spec.png`.
3. For each integer read:
   - If the value is `1` or `0`, update $P(H)$ using Bayes' theorem given the observation $D$, and print the new posterior to `stdout` formatted to exactly 4 decimal places (e.g., `0.7241`).
   - If the value matches the `MISSING` code (found in the image), the system enters "NaN mode". When in NaN mode, print `NaN` for this and ALL subsequent inputs, regardless of whether they are 0 or 1.
   - If the value matches the `RESET` code (found in the image), immediately reset $P(H)$ to the initial prior, exit NaN mode (if active), and print `RESET`. 
4. Stop processing when `EOF` is reached.
5. Compile your final executable to `/home/user/etl_transform`. 

Make sure your calculations use double-precision floats. An automated fuzzing system will feed your compiled binary thousands of randomized event streams and compare the outputs byte-for-byte against a reference oracle.