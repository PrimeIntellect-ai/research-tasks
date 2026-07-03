You are acting as a network security engineer investigating a legacy intrusion detection system. 

We have a legacy, compiled log filtering tool located at `/app/audit_filter`. Unfortunately, the source code was lost, and the binary is stripped. This tool reads process and network audit logs from standard input (one log entry per line) and outputs specific security alerts to standard output. 

Your task is to reverse-engineer the logic of this binary (treating it as a black box and/or using standard reverse-engineering tools like `strings`, `ltrace`, `strace`, or `objdump`) and write a pure Bash script that precisely replicates its behavior.

The input logs are comma-separated values (CSV) with the following format:
`timestamp,src_ip,uid,pid,command_line`

Write your Bash script to `/home/user/filter.sh`. 
- Your script must read from standard input and write to standard output.
- It must produce the exact same output as `/app/audit_filter` for any valid input.
- You must use Bash (shell built-ins and standard coreutils like `awk`, `grep`, `sed` are allowed).
- Make sure your script is executable (`chmod +x /home/user/filter.sh`).

Your script will be tested against a massive suite of randomized log entries to ensure it is bit-for-bit equivalent to the original binary's output.