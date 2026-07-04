You are an integration developer testing APIs protected by a custom embedded Web Application Firewall (WAF). You need to write a Go-based testing tool that emulates the WAF's rule engine, satisfies its access constraints to generate a valid bypass payload, and compiles into standalone binaries for different gateway architectures using conditional build tags.

Perform the following steps:

1. Create a Go module in `/home/user/tester` named `waf_tester`.
2. Write a simple Go-based interpreter/emulator in this module that parses and evaluates the following custom WAF Access Rule DSL:
   `ALLOW_IF: LEN == 10 AND PREFIX == "TST_" AND SUM_DIGITS == 10`
   *(Explanation of DSL: The payload string must be exactly 10 characters long, must start with "TST_", and the sum of all numeric digits in the string must exactly equal 10. Non-numeric characters do not contribute to the sum).*
3. Implement constraint satisfaction logic (or a solver loop) within your Go program to automatically find exactly ONE string payload that satisfies the WAF rule above. Have your program write this satisfying string to `/home/user/bypass_payload.txt`.
4. Use Go conditional builds (build constraints/tags). Define a global variable `Endpoint`. 
   - When built for Linux, `Endpoint` should be `"https://linux.gateway.local/api"`.
   - When built for Windows, `Endpoint` should be `"https://win.gateway.local/api"`.
   - Your `main` function should print the `Endpoint` to stdout.
5. Cross-compile your Go program. 
   - Build a Linux ARM64 binary and output it to `/home/user/tester_arm64`.
   - Build a Windows AMD64 (x86_64) binary and output it to `/home/user/tester_amd64.exe`.

Ensure that all files are created at the exact absolute paths specified. The payload written to `bypass_payload.txt` must strictly satisfy the DSL constraints.