You are managing a fleet of servers and need to analyze their configuration files to identify how many servers belong to various deployment profiles. 

You have been provided a directory of raw configuration files at `/home/user/raw_configs/`. There are 50 configuration files, each representing a server. The files are noisy, containing comments, varying whitespace, and different capitalizations.

Your task is to write a Bash script named `/home/user/analyze.sh` that processes these configuration files and generates a summary report.

**Processing Requirements:**
1. **Parallel Processing:** Your script must process the files in parallel (e.g., using `xargs -P`, `parallel`, or background jobs with `wait`). Do not process them sequentially in a simple loop.
2. **Cleaning & Normalization:**
   - Ignore all empty lines and lines starting with `#` (comments).
   - Extract key-value pairs separated by `=`.
   - Normalize the data by converting all keys and values to lowercase.
   - Remove all leading/trailing whitespace from keys and values (e.g., `  Role = WEB  ` becomes `role=web`).
3. **Feature Extraction:**
   - For each file, extract the values for three specific keys: `role`, `tier`, and `region`.
   - Construct a "server profile" string in the exact format: `role_value,tier_value,region_value`.
   - If any of these three keys are missing in a file, use the string `none` for that value.
4. **Aggregation & Deduplication:**
   - Collect the server profiles from all files.
   - Deduplicate and count the occurrences of each unique server profile across the fleet.
   - Output the results to `/home/user/profile_summary.txt`.

**Output Format:**
The file `/home/user/profile_summary.txt` must contain the aggregated counts and profiles, sorted in descending order by count, then alphabetically by profile. The format for each line should be:
`<count> <profile>`

Example of the expected output format:
```
25 web,frontend,us-east
15 db,backend,us-west
10 cache,backend,us-east
```

Make sure your script `/home/user/analyze.sh` is executable and run it to produce the final `profile_summary.txt` file.