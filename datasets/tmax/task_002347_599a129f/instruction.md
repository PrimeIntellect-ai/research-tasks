You are a data analyst setting up an automated pipeline to benchmark tokenization performance for a new text processing model. However, the headless Linux environment is causing display issues when generating reports (similar to how matplotlib sometimes fails or produces blank plots due to backend misconfigurations).

Your task is to write a Python script at `/home/user/benchmark.py` that processes a dataset, benchmarks the tokenization, verifies the output, and tracks the experiment metrics and visualizations.

Please follow these specific requirements:
1. First, install the necessary Python packages: `pandas`, `tiktoken`, and `matplotlib`.
2. Read the input dataset located at `/home/user/data/reviews.csv`. It contains a column named `review_text`.
3. Use the `tiktoken` library with the `cl100k_base` encoding.
4. Iterate through the `review_text` column and tokenize each string. Benchmark the exact time it takes to tokenize the entire column (start the timer just before tokenization and stop it immediately after). Use `time.perf_counter()`.
5. Calculate the total number of tokens across all reviews (this serves as our numerical accuracy test).
6. Save the tracking metrics to a JSON file at `/home/user/results/metrics.json` with the following schema:
   `{"total_tokens": <int>, "time_seconds": <float>}`
7. Generate a histogram of the token counts per review using `matplotlib`. You must configure matplotlib to use a headless backend (e.g., 'Agg') so it does not crash in this terminal environment. Save the plot to `/home/user/results/token_dist.png`.

The directories `/home/user/data/` and `/home/user/results/` already exist. The CSV file is already in place.