You are a data scientist tasked with cleaning and anonymizing a set of raw customer datasets before they can be used for modeling. The raw data contains sensitive PII (Personally Identifiable Information) and some invalid entries. You must write a C++ program to process these datasets.

Your C++ program should be saved at `/home/user/workspace/cleaner.cpp` and compiled to `/home/user/workspace/cleaner`.

**Input Data:**
The raw data is located in `/home/user/raw_data`. It contains two files:
1. `users.csv`: A CSV file with a header row `id,name,email,age,card`.
2. `users.json`: A JSON file containing an array of objects, each with string or integer keys: `"id"`, `"name"`, `"email"`, `"age"`, `"card"`.

**Processing Requirements:**
Your C++ program must read both files and apply the following Validation and Masking rules to each record:

**1. Constraint-based Validation (Drop the record if it fails any of these):**
*   **Age:** The user's `age` must be 18 or older.
*   **Card Validation (Luhn Algorithm):** The `card` string will contain digits and dashes (e.g., `1234-5678-9012-3456`). Ignore the dashes for validation. The remaining string must be exactly 16 digits long AND must pass the standard Luhn algorithm check.

**2. Data Masking and Anonymization (Apply to valid records):**
*   **Email:** Keep the first letter of the local part, replace the rest of the local part with exactly three asterisks `***`, and keep the domain. 
    *   *Example:* `alice.smith@example.com` becomes `a***@example.com`.
*   **Card:** Replace all digits except the last 4 with `X`. Keep the dashes exactly where they are.
    *   *Example:* `1234-5678-9012-3456` becomes `XXXX-XXXX-XXXX-3456`. `1234567890123456` becomes `XXXXXXXXXXXX3456`.

**Output Data:**
Your program must aggregate all the surviving, masked records and write them out into two different unified formats in the directory `/home/user/clean_data` (create the directory if it doesn't exist):
1. `/home/user/clean_data/unified.csv`: A CSV file containing the aggregated valid and masked records from BOTH input files. Include the header `id,name,email,age,card`. Sort the output rows by `id` in ascending order (treat `id` as an integer).
2. `/home/user/clean_data/unified.json`: A JSON file containing a JSON array of objects of the valid and masked records from BOTH input files. Keys should be `"id"`, `"name"`, `"email"`, `"age"`, `"card"`. The `age` and `id` must be integers. Sort the array objects by `"id"` in ascending order.

*Notes:*
*   You may install any standard C++ JSON libraries available via `apt` (e.g., `nlohmann-json3-dev`) to help with JSON parsing and writing.
*   Do not leave any intermediate files in `/home/user/clean_data`.