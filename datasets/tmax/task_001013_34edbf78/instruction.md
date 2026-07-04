I am an automation specialist trying to replace a legacy data processing pipeline. We have an old compiled binary that processes raw, messy sensor logs and normalizes them, but the source code was lost.

I need you to write a Python script that perfectly replicates the behavior of this legacy tool. 

The legacy binary is located at `/app/legacy_processor`. 
It reads a single line of raw sensor log data from standard input (stdin) and prints a normalized, cleaned, and imputed pipe-separated string to standard output (stdout).

The input logs typically look something like this:
`SENSOR_LOG [ID:A1B2] [2023-10-25T14:30:00Z] DATA: T=22.4;H=55.1;P=1012;T=23.1`

Your tasks:
1. Experiment with `/app/legacy_processor` by passing it various inputs (normal values, missing values, duplicated metrics, out-of-bound anomalies, junk data) to deduce its exact data extraction, constraint validation, deduplication, and imputation logic.
2. Create a Python script at `/home/user/processor.py` that reads a single line from `sys.stdin` and outputs the exact same formatted string as the legacy binary to `sys.stdout`.

Your Python script must perfectly match the binary's output for ANY valid or malformed log string adhering to the general token structure. Do not prompt for input, just read from stdin and print to stdout.