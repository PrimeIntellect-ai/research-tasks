We have a critical security incident involving compromised credentials and need you to handle a comprehensive credential rotation and auditing scenario. 

First, our core token generation library, `libsectoken`, has been vendored into our repository at `/app/vendor/libsectoken-1.2.0/`. However, the build process is broken due to a recent bad commit, and the C extension responsible for token generation has a known security vulnerability (a timing leak during token validation - CWE-208). 
Your first phase is to fix the build configuration in `/app/vendor/libsectoken-1.2.0/Makefile`, audit the C code in `/app/vendor/libsectoken-1.2.0/src/validate.c`, fix the timing leak, and successfully install the package into the local Python environment.

Second, you must write a standalone CLI tool in Python at `/home/user/rotate_tokens.py` that utilizes this fixed library. This tool will take two arguments: a base seed string and a user ID integer. It must generate a new token, apply a specific content security policy transformation (removing any HTML-unsafe characters and enforcing a strict format), and output the final rotated token string to standard output.
We require your tool to be bit-exact equivalent in its output to our legacy Rust-based reference binary located at `/opt/legacy/rotate_tokens_ref`. Your Python program must behave identically for any valid input combinations.

Finally, you need to perform a local service audit. Write a bash script at `/home/user/audit_services.sh` that scans local ports (1000-5000), uses pattern matching to identify any running services that are exposing the old `/api/v1/auth` endpoint in their response payloads, and logs the vulnerable port numbers to `/home/user/vulnerable_ports.log`, one per line.

Ensure your `rotate_tokens.py` handles input exactly as: `python3 /home/user/rotate_tokens.py <seed> <user_id>`.