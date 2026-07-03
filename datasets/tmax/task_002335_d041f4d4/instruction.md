We are currently experiencing a 502 Bad Gateway issue on our internal Nginx API gateway. The gateway routes authentication requests to a local CGI backend.

Upon investigating the error logs (which you can find simulated in `/home/user/nginx_error.log`), we discovered that the backend CGI script crashes because the proprietary authentication binary it relies on, located at `/app/auth_backend`, is randomly segfaulting under load. 

Since we do not have the source code for `/app/auth_backend`, your task is to write a pure Bash replacement for it. 

Here is what you need to do:
1. Analyze the stripped binary `/app/auth_backend`. It takes exactly one command-line argument (a session token, which is an alphanumeric string between 8 and 16 characters) and outputs a specifically formatted validation string to standard output.
2. Reverse-engineer the logic of this binary. You can use standard tools like `strings`, `strace`, `ltrace`, `xxd`, or simply observe its input/output pairs.
3. Write a Bash script at `/home/user/auth_backend.sh` that perfectly replicates the output of the `/app/auth_backend` binary for any given valid alphanumeric token.
4. Your script must use standard text processing tools (`awk`, `sed`, `grep`, `tr`, etc.) to achieve this.

Your final solution will be verified by an automated fuzzer. The fuzzer will generate hundreds of random alphanumeric strings and pass them as an argument to both `/app/auth_backend` and your `/home/user/auth_backend.sh`. Your script must produce the exact same standard output (bit-for-bit, including newlines) as the original binary for every test case.

Ensure your script is executable and located exactly at `/home/user/auth_backend.sh`.