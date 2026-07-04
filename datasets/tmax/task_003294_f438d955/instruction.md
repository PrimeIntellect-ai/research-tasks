You are a data analyst working with an international e-commerce platform. You need to build a multi-stage data processing pipeline to extract features from multilingual product reviews, aggregate metrics, and sort the results. 

The raw data is located at `/home/user/reviews_raw.csv`. It contains the following columns:
`review_id`, `product_id`, `text`, `upvotes`

Your goal is to build a multi-stage Python pipeline that processes this data. You must create four Python scripts:

**Stage 1: Feature Extraction (`/home/user/extract.py`)**
Read `/home/user/reviews_raw.csv`. For each row, calculate the following features from the `text` column:
- `char_count`: The number of characters in the text.
- `emoji_count`: The total number of emojis present in the text. You may use the `emoji` Python package (install it via pip).
- `has_latin`: A boolean (`True` or `False`) indicating if the text contains any standard Latin alphabet characters (`a-z` or `A-Z`).

Write the output to `/home/user/features.jsonl` (JSON Lines format), where each line is a JSON object containing:
`review_id`, `product_id`, `upvotes` (as integer), `char_count`, `emoji_count`, `has_latin`.

**Stage 2: Aggregation (`/home/user/aggregate.py`)**
Read `/home/user/features.jsonl`. Group the data by `product_id` and compute the following metrics for each product:
- `total_upvotes`: Sum of `upvotes`.
- `total_emojis`: Sum of `emoji_count`.
- `avg_char_count`: The mean `char_count`, rounded to exactly 2 decimal places.

Write the aggregated data to `/home/user/aggregated.csv` with headers: `product_id`, `total_upvotes`, `total_emojis`, `avg_char_count`.

**Stage 3: Sorting (`/home/user/sort.py`)**
Read `/home/user/aggregated.csv`. Sort the data based on:
1. `total_upvotes` in descending order.
2. In case of a tie, by `total_emojis` in descending order.
3. In case of a further tie, by `product_id` in ascending (alphabetical) order.

Write the sorted results to `/home/user/final_metrics.csv` (keep the same headers).

**Stage 4: Orchestration (`/home/user/pipeline.py`)**
Write a master script that executes `extract.py`, `aggregate.py`, and `sort.py` sequentially as subprocesses. If any stage fails, the pipeline should exit immediately with a non-zero exit code.

Execute `python3 /home/user/pipeline.py` to complete the task. Verify that `/home/user/final_metrics.csv` is correctly generated.