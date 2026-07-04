You are tasked with building a reproducible data processing pipeline to clean a dataset of mathematical text, tokenize it, and simulate inference performance benchmarking.

We have a raw dataset located at `/home/user/math_raw.csv`. This CSV contains two columns: `id` and `text`. The `text` column contains mathematical explanations heavily polluted with HTML tags and irregular whitespace.

Your goal is to create a Python script `/home/user/pipeline.py` and a shell script `/home/user/run_pipeline.sh` that execute the following steps:

1. **Data Cleaning**: Read `/home/user/math_raw.csv`. For each row's `text`, remove all HTML tags (anything enclosed in `<` and `>`), and replace all occurrences of multiple consecutive whitespace characters with a single space. Strip any leading or trailing whitespace.
2. **Tokenization**: Tokenize the cleaned text using the `tiktoken` library with the `cl100k_base` encoding.
3. **Inference Benchmarking Simulation**: To simulate the performance of a mathematical language model, calculate a simulated inference cost for each row. The simulated inference time for a row is exactly `0.0002` seconds per token.
4. **Metrics Reporting**: Compute the aggregate metrics across all rows and save them to a JSON file at `/home/user/metrics.json`. The JSON must contain exactly these keys:
   - `total_rows`: (integer) The total number of records processed.
   - `total_tokens`: (integer) The sum of all tokens across all cleaned texts.
   - `total_cost`: (float) The total simulated inference time in seconds, rounded to 4 decimal places.

Your shell script `/home/user/run_pipeline.sh` should be executable and must install any necessary Python dependencies before running `pipeline.py`. 

Ensure that your output JSON precisely matches the requested format so it can be automatically verified.