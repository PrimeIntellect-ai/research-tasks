You are a network engineer tasked with inspecting suspicious traffic on our internal network. We recently discovered that a legacy Intrusion Prevention System (IPS) edge node is using an undocumented, proprietary stripped binary located at `/app/traffic_oracle` to inspect decrypted TLS payloads for Web Security threats. We suspect this binary is responsible for validating basic authentication (via brute-forcing a small keyspace) and sanitizing payloads against XSS and SQL injection.

Because the legacy system is being decommissioned and the source code is lost, you need to reverse-engineer `/app/traffic_oracle` and write a bit-exact equivalent implementation in C. This will allow us to integrate the logic into our new open-source IDS platform.

Your tasks:
1. Analyze the stripped binary `/app/traffic_oracle`. You have access to tools like `objdump`, `gdb`, `strings`, and `ltrace`.
2. Determine how it processes input strings (passed as the first command-line argument). Note that it performs some form of basic password/PIN validation (it seems to brute-force or hash a 4-digit prefix) and then inspects the remaining payload for specific Web Injection/XSS signatures.
3. Write a C program that replicates this exact behavior, including identical standard output, standard error, and exit codes for any given input.
4. Save your C source code at `/home/user/ids_logic.c`.
5. Compile your C program to the executable path `/home/user/ids_logic`. Use `gcc -O2 /home/user/ids_logic.c -o /home/user/ids_logic`.

Your implementation must be perfectly equivalent to `/app/traffic_oracle`. An automated fuzzer will invoke your compiled binary with thousands of random inputs and assert that its stdout, stderr, and exit code exactly match the oracle.