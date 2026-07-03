You are tasked with cleaning a large dataset and serving the cleaned results via a simple API, entirely using Bash and standard Linux tools. 

You have been provided with a proprietary, legacy data sanitization binary located at `/app/filter_oracle`. This binary reads three comma-separated numeric features from standard input and outputs either `CLEAN` or `DIRTY` based on an internal classification model.

Your dataset is located at `/home/user/data/raw_data.csv`. It contains 500,000 rows. The CSV has no header, and the columns are: `id,feature_1,feature_2,feature_3,payload_string`. 

The problem: `/app/filter_oracle` is extremely slow. It takes about 0.5 seconds per invocation. Processing 500,000 rows directly through the binary will take weeks. 

**Your Tasks:**
1. **Model Reconstruction:** Treat `/app/filter_oracle` as a black box and reverse-engineer its internal classification logic. The model is a simple linear inequality based on `feature_1`, `feature_2`, and `feature_3`. 
2. **Data Processing:** Once you deduce the rule, write an `awk` or `bash` script to apply this logic to `/home/user/data/raw_data.csv`. Filter out all `DIRTY` rows. Save the cleaned dataset to `/home/user/data/clean_data.csv`.
3. **Data Serving:** Create a simple HTTP server using Bash (`nc`, `socat`, or similar standard tools) listening on `0.0.0.0:8888`. 
   - The server must accept `GET /payload/<id> HTTP/1.1` requests.
   - It should look up the `<id>` in `/home/user/data/clean_data.csv` and respond with an `HTTP/1.1 200 OK` header, followed by a blank line, followed by the `payload_string` for that ID.
   - If the ID does not exist (e.g., it was filtered out or never existed), respond with `HTTP/1.1 404 Not Found`.

**Constraints:**
- You must use Bash, shell built-ins, coreutils, `awk`, `sed`, or other standard CLI tools. Do not write a Python, Perl, or Ruby script.
- The server must stay running in the background or foreground so an automated verifier can query port 8888.