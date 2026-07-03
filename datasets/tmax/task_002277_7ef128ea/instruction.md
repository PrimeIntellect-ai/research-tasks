You are a data scientist tasked with building an automated data cleaning and statistical analysis pipeline using only Bash and standard Unix text processing tools (like `awk`, `sed`, `join`, `sort`, `bc`). You do not have access to Python, R, or any external data science libraries.

You have two dataset files located in `/home/user/`:
1. `/home/user/temps.txt` - Contains server CPU temperature logs. 
   Format: `timestamp|server_id|cpu_temp`
2. `/home/user/loads.txt` - Contains server CPU load logs.
   Format: `timestamp|server_id|cpu_load`

Your objective is to write a bash script at `/home/user/analyze.sh` that performs the following steps when executed:

1. **Data Joining**: Join the two datasets on `timestamp` and `server_id`. The files may not be pre-sorted.
2. **Data Cleaning**: Filter out any rows where:
   - `cpu_temp` is non-numeric (e.g., "ERR") or greater than 100.
   - `cpu_load` is missing or non-numeric.
3. **Statistical Analysis**: Treating `cpu_temp` as the independent variable ($X$) and `cpu_load` as the dependent variable ($Y$), calculate:
   - The Pearson correlation coefficient ($r$)
   - The slope ($m$) of the linear regression line ($Y = mX + b$)
   - The y-intercept ($b$) of the linear regression line
4. **Reporting**: Output the results into a JSON file at `/home/user/results.json` with the following exact structure, rounding the numerical values to exactly 4 decimal places:
```json
{
  "correlation": 0.0000,
  "slope": 0.0000,
  "intercept": 0.0000
}
```

Constraints:
- You must write the solution entirely in Bash. You can use standard tools like `awk`, `sort`, `join`, `grep`, `bc`, etc.
- Your script `/home/user/analyze.sh` must be executable (`chmod +x`).
- Do not use Python, Perl, or any non-standard Unix shell tools. 

Execute your script to produce the final `/home/user/results.json` file.