You are a security researcher analyzing a suspicious data transformation pipeline on a Linux system. You have intercepted a script that a suspected malware strain uses to obfuscate numerical payload data.

In your home directory (`/home/user`), you will find three files:
1. `data_inputs.txt`: A file containing 10,000 floating-point numbers (one per line).
2. `reference_transform.sh`: A known-good reference implementation of the mathematical transformation (written in Bash).
3. `suspicious_transform.sh`: The intercepted obfuscation script.

The `suspicious_transform.sh` script is suspected of having a precision-loss bug that occurs due to an environmental or mathematical edge case deep within its execution path. This bug causes its output to deviate from `reference_transform.sh`. Both scripts take a single file as an argument and print the transformed values to standard output, line by line.

Your task:
1. Perform delta debugging/data diff analysis to identify the **first line number** (1-indexed) in `data_inputs.txt` where the absolute difference between the output of `reference_transform.sh` and `suspicious_transform.sh` is strictly greater than `0.1`.
2. Calculate the exact absolute difference between the two outputs for that specific line, rounded to exactly two decimal places.
3. Write your findings to a file named `/home/user/bug_report.txt` in the exact following format:
`Line: [LINE_NUMBER], Diff: [DIFFERENCE]`

Example of the expected output format in `/home/user/bug_report.txt`:
`Line: 1502, Diff: 0.45`

You may write additional Bash/Python scripts to automate the bisection or diffing process.