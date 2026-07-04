You are a data scientist tasked with cleaning a messy dataset of e-commerce products and building a simple ETL pipeline.

You have been provided with a raw, scraped dataset at `/home/user/raw_products.jsonl`. This file contains JSON objects representing products, but the data is dirty and inconsistent.

Write a Python script at `/home/user/process_products.py` that reads the input file, cleans the data, enforces a strict schema, creates new features, and outputs a cleaned CSV file to `/home/user/cleaned_products.csv`.

**Schema Enforcement & Cleaning Rules:**
1. `product_id`: Must be a string of exactly 8 alphanumeric characters. Drop any row that does not meet this requirement or is missing.
2. `price`: Can appear as a float, an integer, or a string (e.g., "$12.99" or "12.99 USD"). You must extract the numeric value and convert it to a float. Drop any row where the price is missing, cannot be parsed into a number, or is less than or equal to 0.
3. `category`: Must be one of the following exactly: `['electronics', 'clothing', 'home', 'toys']`. If the category is missing or anything else, map it to the string `'other'`.

**Feature Engineering:**
1. `discounted`: Create a new boolean column (`True` or `False`). Set to `True` if the key `original_price` exists in the JSON, is a valid number, and is strictly greater than the extracted `price`. Otherwise, set to `False`.
2. `price_bucket`: Create a new categorical string column based on the extracted float `price`:
   - `'low'`: price < 20.0
   - `'medium'`: 20.0 <= price < 50.0
   - `'high'`: price >= 50.0

**Output Requirements:**
1. The output must be a valid CSV file saved to `/home/user/cleaned_products.csv`.
2. The CSV must contain exactly these columns in this order: `product_id,price,category,discounted,price_bucket`.
3. The rows in the CSV must be sorted in ascending alphabetical order by `product_id`.
4. Ensure boolean values are written as `True` or `False`.