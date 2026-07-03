You are a Site Reliability Engineer responsible for monitoring system uptime and securing deployments. You need to configure a Git hook that verifies system health before allowing code commits, and create a log analysis tool to detect SSH configuration issues.

Part 1: Fix and Deploy the SRE Git Hook
A third-party Go package is provided at `/app/git-sre-hook-1.0.0`. It is designed to run as a Git `pre-receive` hook that checks disk storage thresholds and verifies uptime via an SSH tunnel.
1. The package has a deliberate flaw preventing it from compiling and functioning: it reads the environment variable `SSH_PRT` instead of `SSH_PORT` in `main.go`, and its `Makefile` has a syntax error (spaces instead of tabs for the `build` target).
2. Fix the package, compile it, and place the executable at `/home/user/sre-repo.git/hooks/pre-receive`. Make sure `/home/user/sre-repo.git` is initialized as a bare Git repository.
3. Configure an SSH tunnel that forwards local port 9999 to `localhost:22`. The hook will use this to verify SSH connectivity. (You can background this tunnel process).

Part 2: SSH Log Classifier
We recently had an incident where an SSH configuration change silently rejected key-based logins. You must write a Go program to detect this specific failure mode in auth logs.
1. Write a Go program at `/home/user/detector.go`.
2. The program must accept a single command-line argument: the path to a log file.
3. It must analyze the file and output exactly `EVIL` to standard output if the log contains evidence of silent key-based login rejections (e.g., "Authentication refused: bad ownership or modes").
4. It must output exactly `CLEAN` to standard output if the log represents normal SSH behavior (successful logins, or standard password failures).
5. Compile your program to `/home/user/detector`.

Automated tests will run your `/home/user/detector` binary against a secret test corpus containing both 'evil' and 'clean' logs. It must perfectly classify 100% of both corpora.