You are an automation specialist tasked with building a bash-based data processing pipeline and an HTTP microservice to serve mathematical data.

You have been provided a messy dataset of mathematical equations containing various Unicode formats, full-width characters, and duplicates.

### Step 1: Data Cleaning and Deduplication
A raw CSV file is located at `/home/user/data/equations.csv` with the format `id,equation_text`.
Write a pure Bash script at `/home/user/process_math.sh` (using tools like `sed`, `awk`, `sha256sum`, etc.) that does the following:
1. Normalizes the `equation_text`:
   - Converts Unicode full-width digits (０-９) to standard ASCII digits (0-9).
   - Converts the Unicode multiplication sign (×) to an asterisk (*).
   - Removes all whitespace characters.
2. Deduplicates the equations:
   - Calculate the SHA256 hash of the *normalized* equation string.
   - Keep only the first occurrence of each unique normalized equation.
3. Outputs the results to `/home/user/processed/unique_equations.tsv` in the exact format:
   `<SHA256_HASH><tab><NORMALIZED_EQUATION>`

### Step 2: Fix the HTTP Server Framework
We are using a vendored, lightweight Bash HTTP server framework called `bashttpd` located at `/app/bashttpd-0.1`.
However, the framework has a bug: someone modified it to overly sanitize request URIs, breaking query parameters. Look into `/app/bashttpd-0.1/bashttpd` and fix the request parsing logic so it properly accepts URLs with query strings (e.g., it shouldn't strip out `?`, `=`, and `-` characters from the URI).

### Step 3: Serve the Data
Create a configuration/handler script for `bashttpd` at `/home/user/server.sh`. 
Your server must:
1. Listen on `127.0.0.1:8080`.
2. Handle `GET /equation?hash=<SHA256_HASH>` requests.
3. Read from `/home/user/processed/unique_equations.tsv`.
4. If the hash exists, return an HTTP 200 response with the `<NORMALIZED_EQUATION>` as the plain text body.
5. If the hash does not exist, return an HTTP 404 response.

Once completed, start your server in the background so it is actively listening on port 8080. The verifier will issue HTTP requests to test both the correctness of your data processing and the server responses.