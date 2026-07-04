I am a build engineer managing web security artifacts for our embedded router project. We are transitioning our pipeline to a lightweight, pure-Bash environment, but we have run into two major issues that I need you to resolve.

First, we have a custom C utility located in `/home/user/log_merger/` that merges and sorts web access logs. Unfortunately, the build is currently broken due to a linking error in the `Makefile`. 
1. Fix the `Makefile` in `/home/user/log_merger/` so that running `make` successfully compiles the executable `log_merger`.
2. Once compiled, use the `log_merger` utility to merge `/home/user/logs/node1.log` and `/home/user/logs/node2.log`.
3. Save the output to `/home/user/merged_access.log`.

Second, we have lost the original source code for our Web Application Firewall (WAF) path evaluator. All we have left is the stripped compiled executable located at `/app/waf_evaluator_stripped`. This binary evaluates incoming HTTP request paths, applies URL decoding, normalizes the path, and prints either "ALLOW" or "BLOCK" (and returns exit code 0 or 1, respectively).
1. Analyze the behavior of `/app/waf_evaluator_stripped` by sending it various test paths.
2. Deduce its internal parsing and blocking rules.
3. Write a pure Bash script at `/home/user/waf_eval_pure.sh` that implements the EXACT same logic, state machine, and outputs as the binary. 

The Bash script must:
- Accept exactly one argument (the URI path string).
- Only use Bash built-ins, coreutils, and standard CLI tools (no Python, Perl, etc.).
- Exactly match the standard output ("ALLOW" or "BLOCK") and exit code (0 or 1) of the binary for ANY given path.

An automated fuzzing test will compare your `/home/user/waf_eval_pure.sh` script against the original `/app/waf_evaluator_stripped` with hundreds of random payloads to ensure bit-exact equivalence.