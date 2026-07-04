You are an embedded data scientist working on a lightweight sensor data cleaning pipeline. 

We have an old compiled binary oracle that processes sensor readings, but we need to replace it with a readable Bash script. The documentation for the data transformations was lost, but a scan of the original specification sheet was recovered and is available at `/app/spec_sheet.png`.

Your task is to write a Bash script at `/home/user/pipeline.sh` that exactly replicates the behavior of the reference binary located at `/app/bin/oracle_cleaner`. 

The pipeline reads a continuous stream of CSV rows from standard input and writes processed records to standard output. 
The input format is intended to be: `SensorID,TempA,TempB` (all integers).
However, the input data is messy. You must:
1. Silently drop any rows that are malformed, contain embedded newlines, or contain non-numeric characters (except the commas separating the fields). Valid rows have exactly three columns, where `SensorID` and `TempA` are integers, and `TempB` is either an integer or completely empty.
2. Anonymize the `SensorID` using the specific mathematical masking rule found in the scanned specification image.
3. If `TempB` is missing, impute its value using the mathematical interpolation formula provided in the specification image.
4. Format the final output exactly as dictated by the template shown in the image.

The automated verification system will run a fuzzing test against your script. It will generate thousands of random inputs (both valid and intentionally malformed) and pipe them simultaneously into the `/app/bin/oracle_cleaner` binary and your `/home/user/pipeline.sh` script. Your script must produce bit-exact equivalent standard output, and exit with code 0.

Ensure your script has executable permissions (`chmod +x /home/user/pipeline.sh`). You may use standard Unix utilities (like `awk`, `sed`, `grep`, `bc`) within your script to construct the pipeline DAG.