You are a monitoring specialist tasked with migrating an undocumented, legacy alert routing system to a modern Go-based architecture.

We have a legacy alert filter binary located at `/app/legacy_filter`. It is a stripped executable. Its job is to take a single log message as a command-line argument and print a routing severity level (e.g., "CRITICAL", "WARNING", "INFO", or "IGNORE") to standard output. 

Your tasks are as follows:
1. Reverse-engineer or perform black-box analysis on `/app/legacy_filter` to deduce its exact classification logic.
2. Write a Go program at `/home/user/filter.go` that perfectly replicates the behavior of the legacy binary. It must accept a single command-line argument (the log message) and print the identical output as the oracle.
3. Compile your Go program to `/home/user/filter`.
4. Initialize a bare Git repository at `/home/user/repo.git`. Set up a `post-receive` hook in this repository so that any push to the `main` branch automatically compiles the Go code pushed and places the resulting binary at `/home/user/filter`.
5. Clone the repository to `/home/user/workspace`, add your `filter.go`, commit, and push to the `main` branch to trigger the hook and build the binary.

The automated verification will fuzz your compiled `/home/user/filter` against the `/app/legacy_filter` with thousands of random log strings to ensure bit-exact output equivalence.