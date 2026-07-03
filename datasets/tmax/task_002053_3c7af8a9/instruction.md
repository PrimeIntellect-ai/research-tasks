You are a Data Engineer tasked with building a robust, multi-language ETL pipeline that processes raw transaction logs, handles missing values, clips outliers, and performs feature engineering by hashing categorical IDs.

We recently had an issue where our feature hashing step produced blank or invalid hashes due to a backend misconfiguration in our vendored hashing tool. You need to fix the tool, then build the pipeline around it.

**Step 1: Fix and Compile the Vendored Hashing Tool**
A vendored source of `xxHash-0.8.1` is located at `/app/vendored/xxHash-0.8.1`. 
Currently, running `make xxhsum` fails or produces a broken binary because of a misconfiguration in the `Makefile` (a missing compiler flag causes it to incorrectly try to build with an unsupported SIMD dispatch).
1. Identify and fix the perturbation in `/app/vendored/xxHash-0.8.1/Makefile`.
2. Compile the `xxhsum` binary successfully.

**Step 2: Build the ETL Pipeline**
Create an executable shell script at `/home/user/run_etl.sh` that takes exactly one argument: the path to a JSONL file containing transaction records. Your script must process this file (using Python, Ruby, or standard shell tools internally) and print a strictly formatted CSV to standard output.

**Data Processing Rules (Must be followed EXACTLY for automated verification):**
1. Read the input JSONL file. Each line is a JSON object.
2. **Missing Value Handling:** If a JSON object is missing the `user_id` key or the `amount` key, silently drop the record.
3. **Outlier Handling:** The `amount` field must be numeric. If `amount < 0.0`, cap it to `0.0`. If `amount > 1000.0`, cap it to `1000.0`. Format the resulting amount to exactly two decimal places (e.g., `150.50`, `0.00`, `1000.00`).
4. **Feature Engineering (Hashing):** For each valid record, take the raw string value of `user_id` and compute its 32-bit XXH32 hash using the compiled `xxhsum` utility. 
   *(Hint: You can compute the hash by passing the string to `xxhsum -H0`. Note that `xxhsum` outputs the hash followed by the filename/stdin marker. You ONLY want the lowercase hex hash itself, which is the first token).*
5. **Output Format:** For each valid row, print to standard output:
   `{hashed_user_id},{formatted_amount}`
   *Do not include a CSV header. Do not print any extra spaces.*

**Example Expected Behavior:**
If the input JSONL contains:
`{"user_id": "alice_99", "amount": 1500.2}`
`{"user_id": "bob_12", "amount": -10}`
`{"amount": 50.0}`

The output should be exactly:
`6a5a2988,1000.00`
`587c67c5,0.00`

*Note: Automated tests will heavily fuzz your script with thousands of random inputs to ensure it behaves BIT-EXACTLY like the reference implementation.*