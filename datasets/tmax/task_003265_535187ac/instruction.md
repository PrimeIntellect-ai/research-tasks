You are an SRE (Site Reliability Engineer) tasked with restoring a legacy uptime monitoring pipeline. The previous engineer left behind a C++ log analyzer tool in `/home/user/uptime_analyzer` which processes encrypted system logs to generate uptime reports, but it is currently broken.

Your tasks are:

1. **Build Failure Diagnosis:** The C++ tool currently fails to compile. Identify the missing dependencies, headers, or syntax errors and fix `analyzer.cpp` and/or the `Makefile` so that `make` successfully produces the `uptime_bin` executable.

2. **Git History Forensics & Secret Recovery:** The log file `/home/user/system_events.enc.log` is encrypted. The C++ tool requires an encryption key passed via the environment variable `DECRYPT_KEY`. The key was accidentally committed to the git repository in the past but later removed. Find the key in the git history and export it.

3. **Dashboard Image Extraction:** A screenshot of the old monitoring dashboard is located at `/app/sre_dashboard.png`. You must use OCR (e.g., `tesseract`) to extract the target region's timezone offset (e.g., UTC-X or UTC+X) from this image. The C++ tool has a subtle timezone bug and defaults to UTC. You need to modify the C++ code to apply the offset found in the image when calculating daily buckets. 

4. **Format Parsing & Boundary Condition Repair:** 
   - The C++ parser contains strict assertions validating intermediate parsing states. Currently, running it will trigger an assertion failure on line 144 of the logs due to a format parsing edge-case (malformed ISO8601 strings).
   - There is an off-by-one boundary error in the downtime duration calculation. Fix the code so that it correctly computes the exact inclusive second boundaries.

5. **Final Integration:** Once compiled and fixed, run the executable on `/home/user/system_events.enc.log`. The tool expects two arguments: the input log file and the output CSV path.
   Generate the final parsed report at `/home/user/uptime_report.csv`. The format of the CSV should be exactly: `Date,Total_Uptime_Seconds,Downtime_Events`.

You have standard bash CLI tools, git, and tesseract available.