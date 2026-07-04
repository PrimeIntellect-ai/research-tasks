You are a database administrator tasked with optimizing a slow data processing pipeline. We recently exported a large dataset of employee records from our NoSQL database into a JSON Lines format, located at `/app/data.jsonl`. 

A junior developer wrote a pure-Bash aggregation script (`/app/baseline.sh`) to process this data. However, the script uses unoptimized `while read` loops and subshells, making it prohibitively slow.

We have an image containing the original schema requirements and the desired aggregation pipeline steps, located at `/app/query_spec.png`. 

Your task:
1. Extract the aggregation requirements from the image `/app/query_spec.png` (you may use `tesseract`).
2. Write a highly optimized Bash script at `/home/user/optimized.sh` that performs the exact aggregation pipeline specified in the image. You must use standard Linux CLI tools (like `jq`, `awk`, `grep`, etc.) to achieve this.
3. Your optimized script must output the final result in standard JSON array format and save it to `/home/user/result.json`.
4. Ensure your script produces the *exact* same logical output as the baseline script would for the specified pipeline, but it must be heavily optimized. We will measure the performance of your script against the baseline.

Requirements:
- Your script `/home/user/optimized.sh` must be executable.
- The output in `/home/user/result.json` must be a valid JSON array of objects.
- The execution time of your optimized script must be substantially faster than the baseline approach (our automated verifier requires a significant speedup threshold to pass).