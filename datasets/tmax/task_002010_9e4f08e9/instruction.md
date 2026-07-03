You are a compliance analyst responsible for generating audit trails for a high-volume financial system. Our legacy log processing tool, `/app/legacy_scanner`, is a compiled binary used to audit transaction logs. It performs file integrity verification (validating hashes against payloads) and pattern matching for intrusion detection.

Unfortunately, `/app/legacy_scanner` is extremely slow and its source code was lost during a previous migration. We need a high-performance replacement written in C.

Your task is to:
1. Analyze the behavior of the stripped binary `/app/legacy_scanner`. You can run it against the sample log file provided at `/home/user/sample_logs.txt`.
2. Deduce the rules it uses to classify log entries. The input format is always `LogID | Hash | Payload`. The output format is `LogID: STATUS`.
3. Write a C program at `/home/user/scanner.c` that accurately replicates the classification logic of the legacy scanner.
4. Your program must read a log file path as its first command-line argument and print the classifications to standard output in the exact same format as the legacy tool.
5. Compile your C program to `/home/user/scanner` (e.g., using `gcc -O3 -o /home/user/scanner /home/user/scanner.c -lcrypto`).

The new scanner must handle the data efficiently and match the legacy scanner's output logic perfectly. After you finish, an automated suite will test your compiled `/home/user/scanner` against a massive, hidden dataset to calculate its accuracy metric compared to the legacy tool. 

Ensure your final executable is located strictly at `/home/user/scanner`.