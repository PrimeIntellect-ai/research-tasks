You are acting as a data analyst migrating a legacy log analysis pipeline to a modern Python stack.

We have a legacy stripped binary located at `/app/legacy_scorer`. This binary reads a single line of text from standard input (a log message), processes it using pre-trained token weights from `/app/weights.csv`, and outputs a single floating-point anomaly score to standard output. 

We need to completely replace this binary. Your objectives are:

1. **Reimplement the Scoring Logic:**
   Create a Python script at `/home/user/scorer.py`. It must behave *identically* to `/app/legacy_scorer`. It should read a single line from `stdin` and print the calculated float score to `stdout` (formatted to 4 decimal places, e.g., `1.2345`).
   *Hint on the binary's logic:* The binary splits the input string by spaces. For each token, it looks up a 3-dimensional embedding vector in `/app/weights.csv`. If a token is missing from the file (outlier/missing value), it assigns a default fallback vector of `[0.5, 0.5, 0.5]`. It then sums all the token vectors to produce a single aggregated 3D vector. The final score is the L2 norm (Euclidean length) of this aggregated vector, multiplied by a fixed Bayesian prior probability of `0.85`.

2. **Fix the Visualization Script:**
   There is an existing Python script at `/home/user/plot_anomalies.py` which generates random logs, scores them, and plots a histogram. Currently, it runs without error but produces a completely blank image at `/home/user/plot.png` due to a matplotlib backend or configuration issue. Fix the script so it correctly saves the histogram of the scores.

Requirements:
- Your `/home/user/scorer.py` must perfectly match the output of `/app/legacy_scorer` for any valid string of alphanumeric space-separated tokens.
- Use only standard Python libraries and `numpy` for the math.