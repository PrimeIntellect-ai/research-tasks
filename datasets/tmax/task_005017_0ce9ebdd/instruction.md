As a FinOps analyst, I am working on a cloud storage cost optimization pipeline. We recently lost the original source code for our tier-pricing calculator, but we have a compiled reference binary and a screenshot of the internal rate card. I need you to rebuild the Python implementation of this calculator.

Here is what you need to do:

1. **Information Recovery:**
   There is an image file located at `/app/storage_rates.png` containing our custom enterprise agreement rates for three storage tiers (Standard, Infrequent Access, and Deep Archive). You must extract the exact base price per GB and the price per API request for each tier from this image. 

2. **Environment & Logging Setup:**
   - Create a directory `/home/user/finops/`.
   - Modify the `/home/user/.bashrc` file to set the environment variable `FINOPS_LOG_PATH` to `/home/user/finops/optimizer.log`.
   - The Python script you write must use Python's built-in `logging` module to log all operations. It must use a `RotatingFileHandler` pointing to the path specified by the `FINOPS_LOG_PATH` environment variable. Configure it to rotate at 10,240 bytes with a backup count of 3.
   - For every input line processed, log an INFO message: `Processing record: <GB> GB, <reqs> requests`.

3. **Rebuild the Optimizer Script:**
   - Create the script at `/home/user/finops/optimizer.py`.
   - The script must read continually from `sys.stdin`. Each line of input will contain two space-separated integers: `<storage_gb> <api_requests>`.
   - For each line, calculate the total cost for all three tiers based on the rates you extracted from the image. 
   - The formula for a tier's cost is: `(storage_gb * price_per_gb) + (api_requests * price_per_request)`.
   - The script must print a single float to `sys.stdout` representing the minimum cost among the three tiers, formatted to exactly four decimal places (e.g., `45.1200`), followed by a newline.
   - The script must exit cleanly when EOF is reached.
   - The behavior of your script must perfectly match our reference binary, including edge cases with 0 requests.

Ensure your environment variables are configured in the profile, the log rotation logic is properly implemented, and the math matches the reference data precisely.