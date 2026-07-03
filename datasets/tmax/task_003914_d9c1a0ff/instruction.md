You are an edge computing engineer deploying an IoT fleet. We have an existing legacy binary `/app/proxy_oracle` that filters and routes incoming proxy requests for our edge devices. However, we need to re-implement this logic in Go so we can compile it for different ARM and MIPS architectures.

The filter program must read a single line of base64-encoded text from standard input, decode it, and print a routing decision string to standard output.

To understand the baseline routing rules, analyze the flowchart provided at `/app/proxy_rules.png`. (You may use OCR tools like `tesseract` to read it). It describes the authentication and routing logic, including an SSH config rule that silently rejects certain key-based logins, and how various payloads are distributed to load balancers.

Requirements:
1. Analyze `/app/proxy_rules.png` to extract the routing logic and precedence rules.
2. Write a Go program at `/home/user/filter.go` that implements these exact rules.
3. Build the program to `/home/user/filter_bin`.
4. Your program's output must be BIT-EXACT identical to `/app/proxy_oracle` for ANY valid base64 input string. The oracle takes the same input format (a base64 string on stdin) and outputs the decision string.
5. In addition to the Go program, set up a directory structure in `/home/user/edge_deploy/` with subdirectories `logs`, `conf`, and `bin`. Create a symlink at `/home/user/edge_deploy/bin/filter_bin` pointing to `/home/user/filter_bin`.

Note: The automated verifier will aggressively fuzz your binary with thousands of random inputs and compare it against `/app/proxy_oracle`. Make sure all edge cases (e.g., base64 decoding errors, empty strings, exact string match precedence) are handled exactly as the oracle does.