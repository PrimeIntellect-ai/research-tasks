You are a Data Engineer building a lightweight ETL pipeline using native Bash and Unix tools (no Python/Node.js scripts allowed; you must use Bash, `awk`, `sed`, `jq`, etc.). 

Your input data is located at `/home/user/raw_data/transactions.csv`. 
The file has the following CSV header: `timestamp,email,ip,amount,category`. The file is ordered by `timestamp`.

You need to write a master script at `/home/user/etl_pipeline.sh` that accomplishes the following tasks:

1. **Setup:** 
   Create the output directory `/home/user/etl_output/`.

2. **Parallel Data Masking:** 
   Process the CSV lines (excluding the header) in parallel using at least 4 concurrent processes (e.g., using `xargs -P`, `split` with background jobs `&`, or `parallel`). 
   Apply the following masking rules:
   - `email`: Keep the first character, replace the characters before the `@` with `***`, and keep the domain. Example: `alice@example.com` becomes `a***@example.com`.
   - `ip`: Mask the last octet with `0`. Example: `192.168.1.45` becomes `192.168.1.0`.
   Recombine the processed rows, prepend the original header, sort them chronologically by `timestamp` (ascending), and save to `/home/user/etl_output/masked.csv`.

3. **Rolling Statistics:** 
   Read the newly created `masked.csv`. For each `category`, calculate the rolling average of `amount` over a window of the last 3 transactions (the current transaction and up to 2 previous ones). 
   Output the result to `/home/user/etl_output/rolling.csv` with the header `timestamp,category,rolling_avg`. Format the `rolling_avg` to exactly 2 decimal places. Sort the output chronologically by `timestamp`.

4. **Summary Statistics:** 
   Calculate the total sum and the overall average of `amount` for each `category`. 
   Save the output to `/home/user/etl_output/summary.json` in the following JSON format:
   ```json
   {
     "Retail": {
       "total": 1250.50,
       "avg": 45.21
     },
     "Tech": {
       "total": 5000.00,
       "avg": 1250.00
     }
   }
   ```
   *Note: Format all monetary numbers to 2 decimal places.*

Constraints:
- Your script `/home/user/etl_pipeline.sh` must be executable (`chmod +x`).
- You must rely on Bash and standard Unix utilities (`awk`, `sed`, `jq`, `sort`, etc.). 
- Execute your script so the output files are generated for verification.