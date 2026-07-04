You are a configuration manager for a legacy server fleet. Over time, configuration backups were saved in various character encodings. You need to write a Bash script or use shell commands to analyze the volatility of these configurations over time.

You have been provided an inventory file at `/home/user/inventory.csv` with the following format:
`version_number,file_path,encoding`

The configuration backups are located in `/home/user/configs/`. 

Your task is to:
1. Parse the CSV file and process the configuration files in strictly increasing order of their `version_number`.
2. Convert the contents of each file from its original encoding to UTF-8.
3. Compute the "distance" (number of changes) between each consecutive version (e.g., v1 to v2, v2 to v3) using their UTF-8 representations. The distance metric is defined as the total number of added and removed lines. You should calculate this by running `diff -U0 fileA fileB` and counting the number of lines that begin with exactly one `+` or `-` (ignoring the `---` and `+++` file headers).
4. Compute the rolling average of the distance over a window of the last 2 transitions. If only 1 transition has occurred so far, the rolling average is just the value of that single transition.
5. Output the results to a new CSV file at `/home/user/change_metrics.csv` with the exact header `transition,changes,rolling_avg`. The `transition` column should be formatted as `v{X}-v{Y}` (e.g., `v1-v2`). The `rolling_avg` column must be formatted to exactly one decimal place (e.g., `2.0`, `2.5`).

Constraints:
- You must use Bash built-ins, coreutils, and standard Unix CLI tools (like `iconv`, `awk`, `diff`, `grep`). Do NOT use Python, Perl, or Ruby.
- Ensure your output file exactly matches the requested CSV format.

Example expected output format for `/home/user/change_metrics.csv`:
```csv
transition,changes,rolling_avg
v1-v2,10,10.0
v2-v3,5,7.5
...
```