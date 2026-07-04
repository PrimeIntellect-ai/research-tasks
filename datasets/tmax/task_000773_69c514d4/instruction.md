You are an MLOps engineer investigating a pipeline bug where misconfigured backends are occasionally producing blank matplotlib plots instead of actual experiment visualizations. You have two files tracking your recent experiment artifacts:

1. `/home/user/artifacts.txt`: Contains space-separated columns `id` and `size` (in bytes).
2. `/home/user/metrics.txt`: Contains space-separated columns `id` and `error_rate` (a float between 0 and 1).

Your task is to build a reproducible pipeline to detect the 3 most likely "blank plot" anomalies. 

Create a bash script at `/home/user/pipeline.sh` that performs the following steps:
1. Joins `/home/user/artifacts.txt` and `/home/user/metrics.txt` on the `id` column using standard Linux command-line tools. (Assume both files are already sorted by `id` and have no headers).
2. Compiles a C++ program from a file named `/home/user/detect.cpp` (which you must write).
3. Pipes the joined data (format: `id size error_rate`) into the compiled C++ program.
4. Redirects the output of the C++ program to `/home/user/top_anomalies.txt`.

You must write the C++ program (`/home/user/detect.cpp`) to do the following for each incoming record:
1. Read the `id`, `size`, and `error_rate` from standard input.
2. Compute the Bayesian posterior probability that the artifact is corrupted ($C$), given the observed $error\_rate$ ($E$). Use this exact formulation:
   - Prior probability of corruption: $P(C) = 0.05$
   - Prior probability of normal: $P(\neg C) = 0.95$
   - Likelihood of error given corruption: $P(E|C) = error\_rate$
   - Likelihood of error given normal: $P(E|\neg C) = 0.01$
   - Posterior: $P(C|E) = \frac{P(E|C)P(C)}{P(E|C)P(C) + P(E|\neg C)P(\neg C)}$
3. Perform a similarity search by calculating the Euclidean distance $D$ of the artifact to a hypothetical "perfect blank plot" profile. The perfect blank profile has a posterior $P(C|E) = 1.0$ and a normalized size of $0.0$.
   - Distance formula: $D = \sqrt{(P(C|E) - 1.0)^2 + (\frac{size}{1000.0})^2}$
4. Output the integer `id`s of the 3 artifacts with the **smallest** distance $D$, printing one `id` per line, sorted from smallest distance to largest distance.

Constraints:
- Use standard C++ libraries (e.g., `<iostream>`, `<vector>`, `<cmath>`, `<algorithm>`).
- Ensure the bash script `pipeline.sh` has executable permissions and can be run to produce the final `/home/user/top_anomalies.txt` file.