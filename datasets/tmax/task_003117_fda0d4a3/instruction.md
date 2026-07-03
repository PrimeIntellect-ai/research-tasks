You are a data analyst tasked with processing a batch of sensitive financial transactions. You have been provided with a CSV file at `/home/user/transactions.csv`. 

Your goal is to write and execute a Python script that reads this CSV, performs data validation, calculates rolling aggregations, applies data anonymization, and saves the final result to `/home/user/processed_transactions.csv`.

The input CSV has the following columns: `transaction_id`, `user_id`, `ssn`, `date`, `amount`.

Here are the requirements for your data processing pipeline:

**1. Constraint-based Data Validation**
You must filter out invalid rows. A row is considered VALID if and only if:
- `amount` is a non-negative number (`>= 0`).
- `date` is on or before `2023-12-31` (Format is `YYYY-MM-DD`).
- `ssn` is exactly 9 digits long (no dashes, just numbers).
Drop any rows that do not meet ALL of these criteria.

**2. Windowed Aggregation**
For the valid rows, calculate a rolling average of the `amount` for each `user_id`.
- Group the data by `user_id`.
- Sort the records within each group by `date` (ascending) and then by `transaction_id` (ascending).
- Calculate a 3-transaction rolling average of the `amount` (this includes the current transaction and up to 2 preceding transactions for that user). If a user has fewer than 3 previous transactions, calculate the average over the available transactions (minimum 1).
- Add this value as a new column named `rolling_avg_amount`. Round the values in this column to exactly 2 decimal places.

**3. Data Masking and Anonymization**
Protect the sensitive SSN data.
- Replace the `ssn` column with a new column named `ssn_masked`.
- The `ssn_masked` column should replace the first 5 digits of the valid SSN with the character `X` (e.g., `123456789` becomes `XXXXX6789`).

**Final Output Formatting:**
The final CSV file must be saved to `/home/user/processed_transactions.csv` and include the following columns in this exact order:
`transaction_id`, `user_id`, `ssn_masked`, `date`, `amount`, `rolling_avg_amount`.

The final CSV should be sorted primarily by `user_id` (ascending), secondarily by `date` (ascending), and tertiarily by `transaction_id` (ascending). Include the header row.

Use Python (pandas is highly recommended, but you may use any standard library/installed package).