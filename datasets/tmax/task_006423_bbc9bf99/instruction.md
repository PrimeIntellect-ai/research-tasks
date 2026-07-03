You are acting as a security auditor. We have recently detected anomalous behavior in our sandboxed execution environment. 

Your task is to write a C program that parses a security log, identifies unauthorized sandbox escape attempts, validates the session tokens associated with these attempts, and outputs a list of confirmed compromised tokens.

Here are the requirements:
1. Write your C program in `/home/user/auditor.c` and compile it to `/home/user/auditor`.
2. The log file is located at `/home/user/security.log`.
3. Each line in the log is formatted with pipe-separated key-value pairs. Example:
   `1699999999 | ACTION=EXEC | STATUS=DENIED | REASON=SANDBOX_VIOLATION | TOKEN=a1b2c3d4e5f60718 | COMMAND=/bin/sh`
4. You need to identify lines that contain the exact string `REASON=SANDBOX_VIOLATION`.
5. For each matching line, extract the 16-character hexadecimal string assigned to `TOKEN=`.
6. Validate the token. A token is considered **valid** (meaning it was a legitimately issued token that is now being abused) ONLY if the sum of its 16 hexadecimal digits (evaluated as integers 0-15) is divisible by 3.
7. Output all extracted, **valid** tokens that were involved in a `SANDBOX_VIOLATION` to the file `/home/user/compromised_tokens.txt`. 
8. The output file must contain exactly one token per line, in lowercase, in the order they appeared in the log. Do not include any other text in the file.

Write the C code, compile it, and run it to produce the required output file.