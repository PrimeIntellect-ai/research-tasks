You are a security auditor building a new automated vulnerability scanning pipeline in Go. As part of this pipeline, you need to integrate a legacy, proprietary policy evaluation module provided by a client. 

The client has lost the source code and only provided a stripped Linux binary located at `/app/legacy_checker`. 

You know the following about this binary:
1. It takes exactly one argument (`argv[1]`): a 12-character uppercase hex-encoded string representing an obfuscated payload.
2. The payload encodes a file's UID, GID, and Permission Mode (in that order).
3. The binary evaluates these file attributes against the client's internal access control policy and prints a single security status string to standard output ("CRITICAL", "WARNING", or "SECURE"), followed by a newline.

Your task is to reverse-engineer the `/app/legacy_checker` binary to understand its payload decoding (which uses a simple, static single-byte XOR cipher) and its access control logic. 

Once you understand the algorithm, write a Go program at `/home/user/policy_check.go` that perfectly replicates the behavior of the legacy binary. 

Requirements:
- Your Go program must take the 12-character hex string as `os.Args[1]`.
- It must output the exact same string as the `/app/legacy_checker` binary for any given valid hex input.
- Compile your Go program to `/home/user/policy_check`.
- Do not rely on calling the legacy binary from your Go code; you must implement the logic natively in Go.

Use standard reverse-engineering tools (like `objdump`, `ltrace`, `strace`, `xxd`, `gdb`) to analyze how the binary transforms the input and evaluates the permissions.