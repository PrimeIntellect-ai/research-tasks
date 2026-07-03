You are a data analyst working on a text processing pipeline. We need to process a large dataset of product reviews, but due to performance constraints, the core processing engine must be written in C++. 

Your task is to build a C++ pipeline that performs tokenization, feature engineering, and feature selection, along with a bash script to ensure reproducibility and experiment tracking.

**1. Input Data:**
There is a raw dataset located at `/home/user/raw_data.csv`. 
It has the following header: `id,review_text,rating,timestamp`
The `review_text` column contains text enclosed in double quotes.

**2. C++ Data Processor (`/home/user/processor.cpp`):**
Write a C++ program that takes exactly one integer command-line argument: `MIN_TOKENS`.
The program must:
*   Read `/home/user/raw_data.csv`.
*   **Tokenization & Feature Engineering:** For each `review_text`, tokenize the string strictly by the space character (`' '`). Calculate two new features:
    *   `token_count`: The total number of tokens.
    *   `avg_token_length`: The average length of these tokens (total characters in all tokens / number of tokens). Format this as a float with exactly 2 decimal places.
*   **Feature Selection:** Discard any row where `token_count` is strictly less than `MIN_TOKENS`.
*   **Dataset Preparation:** Save the retained rows to `/home/user/processed/filtered_<MIN_TOKENS>.csv`. The output CSV must have the header: `id,token_count,avg_token_length,rating`.
*   **Experiment Tracking:** Write a JSON summary of the run to `/home/user/experiments/run_<MIN_TOKENS>.json`. It must have the exact format: `{"min_tokens": <MIN_TOKENS>, "total_rows": <TOTAL>, "kept_rows": <RETAINED>}`. (You may use standard C++ string formatting to write this JSON, you don't need an external JSON library).

*Note: You must create the `processed` and `experiments` directories if they do not exist.*

**3. Pipeline Reproducibility Script (`/home/user/run_pipeline.sh`):**
Write a bash script that:
*   Compiles `processor.cpp` into an executable named `processor` using `g++` with `-O3`.
*   Runs the processor for three experiments: `MIN_TOKENS` values of 5, 10, and 15.
*   Generates a SHA256 checksum of the three resulting CSV files in `/home/user/processed/` and saves the output to `/home/user/reproducibility_check.txt` using the command `sha256sum /home/user/processed/filtered_*.csv > /home/user/reproducibility_check.txt`.

Execute your `run_pipeline.sh` script to produce the final artifacts.