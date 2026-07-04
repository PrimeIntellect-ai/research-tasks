You are acting as a network engineer troubleshooting connectivity and logging issues in a microservice setup. We have a custom C++ logging and networking daemon, but its source code has some issues and we need a robust log sanitizer to process its output.

Your objectives:

1. **Fix the Vendored Package:**
   We have vendored the source for our networking daemon at `/app/vendor/netlogger-1.2.tar.gz`.
   Extract this archive to `/home/user/netlogger`. 
   The package has a deliberate perturbation in its `Makefile` (it is failing to compile due to missing standard library links and wrong C++ standard flags; it requires C++17). Fix the `Makefile`, compile the source, and ensure the executable `netlogger` is successfully built at `/home/user/netlogger/netlogger`.

2. **Develop a Log Sanitizer (C++):**
   The daemon outputs raw connection logs, but they are polluted with spoofed external connection attempts.
   Write a C++ program at `/home/user/log_sanitiser.cpp` and compile it to `/home/user/log_sanitiser`.
   
   The sanitizer must take a single command-line argument (the path to a log file) and print ONLY the clean log lines to standard output.
   
   **Sanitizer Rules:**
   - A log line has the format: `[TIMESTAMP] IP:PORT STATUS MESSAGE`
   - You MUST ACCEPT (preserve) lines where the IP belongs to the private subnets `10.0.0.0/8` or `192.168.0.0/16`.
   - You MUST REJECT (drop) lines where the IP is from outside those subnets (e.g., public IPs).
   - You MUST REJECT lines where the `MESSAGE` contains the exact substring `SPOOF` or `MALFORMED`.
   - You MUST REJECT lines where the `PORT` is less than `1024` (privileged ports).

3. **Verification Corpora:**
   Your sanitizer will be tested against two sets of log files located in:
   - `/app/corpus/clean/`: Contains strictly valid, internal traffic logs. Your program must output these lines exactly as they are.
   - `/app/corpus/evil/`: Contains malicious, spoofed, or invalid connection attempts. Your program must drop these lines completely.
   
   To pass, your compiled `/home/user/log_sanitiser` must preserve 100% of the lines in the clean corpus and reject 100% of the invalid lines in the evil corpus.

Ensure your C++ code is efficient and handles file I/O properly. Compile your sanitizer using `g++ -O2 -std=c++17 /home/user/log_sanitiser.cpp -o /home/user/log_sanitiser`.