You are a data analyst tasked with building a reproducible, zero-dependency ETL and recommendation pipeline from scratch.

You have a dataset of customer profiles located at `/home/user/customers.csv`. The CSV has a header: `id,age,income,spending_score`.

Unfortunately, the data is messy and contains invalid rows. Your task is to write a Python script `/home/user/find_similar.py` that processes this data, cleans it, normalizes it, and finds the top 3 most similar customers to a target profile using Euclidean distance.

**Constraints & Rules:**
1. **Zero External Dependencies**: You must use ONLY Python standard libraries (e.g., `csv`, `math`). Do not use `pandas`, `numpy`, `scikit-learn`, or any other third-party packages.
2. **Schema Enforcement (Data Cleaning)**: Your script must read the CSV and drop any row that fails *any* of the following conditions:
   - `id` must be an integer.
   - `age` must be an integer greater than 0.
   - `income` must be a float greater than or equal to 0.
   - `spending_score` must be a float between 0 and 100 (inclusive).
   - Drop any row where values are missing or fail to parse into the correct numeric types.
3. **Normalization**: For the *valid* rows only, compute the minimum and maximum values for `age`, `income`, and `spending_score`. Min-max normalize these three features to a 0.0 - 1.0 scale using the formula `(value - min) / (max - min)`.
4. **Similarity Search**: 
   - A target customer profile is given: `age=35`, `income=75000`, `spending_score=50`.
   - Normalize this target profile using the min and max values computed from the valid dataset.
   - Calculate the Euclidean distance between the normalized target profile and each normalized valid customer profile in the dataset.
5. **Output**: Find the `id` of the 3 customers with the *smallest* Euclidean distance to the target profile. 
   - Write these 3 integer IDs, comma-separated (e.g., `10,4,2`), to `/home/user/similar_customers.txt`.
   - Order them from most similar (smallest distance) to least similar.

Write the script and execute it to produce the final output file.