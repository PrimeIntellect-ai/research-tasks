As a Linux systems engineer hardening our logging infrastructure, you have been tasked with replacing an undocumented, stripped binary with a clean, maintainable C implementation. You must also set up the surrounding process supervision and log rotation.

Your tasks are:

1. **Reverse Engineer the Binary**: 
   There is a stripped binary located at `/app/sec_logger`. It reads raw data from `stdin` until EOF, applies a specific byte-wise mathematical transformation to obfuscate the logs, and writes the result to `stdout`.
   Analyze its behavior (using reverse engineering tools or black-box testing). Write a C program at `/home/user/sec_logger_clone.c` that performs the exact same transformation, and compile it to `/home/user/sec_logger_clone`. It must be bit-exact equivalent to `/app/sec_logger` for any input.

2. **Automated Initialization**:
   There is an interactive configuration script at `/app/init_env.sh`. It prompts for a "Username:" and a "PIN:". 
   Write an `expect` script at `/home/user/init.exp` that automates running `/app/init_env.sh`, providing the username `sysadmin` and the PIN `8080`. Run this expect script to generate the required environment configuration.

3. **Process Supervision**:
   Create a bash script at `/home/user/supervisor.sh` that continuously runs your compiled binary `/home/user/sec_logger_clone`. It should read from a named pipe `/home/user/input.fifo` (which you must create) and redirect standard output to `/home/user/logs/output.log`. If the binary crashes or terminates, the supervisor should immediately restart it. Ensure the script is executable.

4. **Log Configuration & Rotation**:
   Create a `logrotate` configuration file at `/home/user/logrotate.conf` that targets `/home/user/logs/output.log`. The configuration must specify:
   - Daily rotation
   - Retain exactly 7 backlogged rotated files
   - Compress the rotated files
   - Missing log files should not produce an error
   - File size must be greater than 10k before rotating

Make sure all directories and files are placed exactly where requested. We will verify the correctness of your C implementation by aggressively fuzzing it against the original binary.