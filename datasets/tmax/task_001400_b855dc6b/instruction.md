I need you to debug a failing automated data processing build pipeline. I am working on a Bash-based data processing suite, but our nightly build job is currently failing, and it has left the system in a broken state.

Here is what you need to know and do:

1. **Build Failure & Core Dump Analysis**:
   There is a build script located at `/home/user/build/run_pipeline.sh`. When executed, a helper binary called by this script segfaults and produces a core dump in `/home/user/build/`. You need to analyze the core dump to determine why the helper binary is crashing (it is likely an environment misconfiguration, such as a missing environment variable). Fix `/home/user/build/run_pipeline.sh` so that the pipeline runs successfully without crashing.

2. **Database Recovery**:
   The pipeline relies on a SQLite database located at `/home/user/data/metrics.db`. However, the main database file was accidentally truncated, leaving it corrupted. Fortunately, the SQLite Write-Ahead Log (WAL) file `/home/user/data/metrics.db-wal` is intact. You need to recover the corrupted database using the WAL file so that the data is queryable again.

3. **Query Debugging & Image Extraction**:
   I don't remember the exact criteria for the final reporting query, but someone took a screenshot of the query requirements during a meeting. The image is located at `/app/schema_clue.png`. You will need to extract the text from this image (e.g., using `tesseract`) to understand the specific `WHERE` clause conditions required for the final metric calculation.

4. **Final Integration**:
   Create a bash script at `/home/user/build/get_metric.sh`. This script must execute a SQL query against your recovered `/home/user/data/metrics.db`. 
   The query should calculate the average (mean) `duration` of requests that match the conditions extracted from the image. 
   Your script must output *only* a single floating-point number to standard output (e.g., `42.53`).

Make sure your script `/home/user/build/get_metric.sh` is executable. We will run it to verify your success. The closer your output is to the true average, the better.