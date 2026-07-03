You are a support engineer investigating a highly specific parsing failure in a legacy service. 

We have a vendored package located at `/app/vendored_logparser-1.2.0`. It contains a fast log parsing utility (written in Python with a C extension). Currently, the package fails to build its C extension due to a misconfiguration in its build files, causing it to fall back to a deeply flawed pure-Python implementation. Your first task is to diagnose and fix the build perturbation in `/app/vendored_logparser-1.2.0` so the package builds and installs successfully (using `pip install -e .`).

We recently had a crash on production caused by a specific malformed log line. A disk image containing the recovered filesystem from that server is mounted at `/app/server_disk.img`. The core dump was deleted by an automated cleanup script, but the file may still be recoverable from the `ext4` image. Extract the deleted memory dump from the image, and perform memory dump analysis to extract the string that caused the crash (it starts with `CRASH_INP:`).

Furthermore, a former engineer created a canonical, bug-free "oracle" binary of the parser, but accidentally deleted it and purged it from the working tree in the Git repository located at `/app/internal_tools`. Use Git history forensics to recover the file named `parser_oracle_bin` from the repository's history and place it at `/home/user/oracle`.

Finally, use the insights from the crashing input and the behavior of the oracle to write a standalone Python script at `/home/user/fixed_parser.py`. This script must accept a single command-line argument (a string) and print the parsed output. Your Python script must be bit-exact equivalent in its output to the `/home/user/oracle` binary for any input string. 

Do not rely on the vendored package for your final script; write a clean, pure-Python parsing function in `/home/user/fixed_parser.py` that perfectly mirrors the oracle's output. Make sure the script is executable.