You are a script developer tasked with building and testing a lightweight mathematical microservice. We have a C program that calculates the factorial of a given number, but it currently has bugs that cause integer overflow and incorrect mathematical results for edge cases. 

You need to fix the code, generate a patch, set up a reverse proxy, and write a CI/CD bash script to automate the build and testing pipeline.

Here is your working directory: `/home/user/math_pipeline`
(Create this directory if it doesn't exist).

**Step 1: The C Service**
Create a file `/home/user/math_pipeline/factorial.c` with the following initial buggy code:
```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 1;
    
    int result = 1;
    for (int i = 1; i <= n; i++) {
        result *= i;
    }
    
    printf("%d\n", result);
    return 0;
}
```
This program reads a number from standard input and prints its factorial.
Fix the code so that:
1. It uses a data type large enough to accurately calculate the factorial of 20.
2. It correctly handles the edge case of 0! (which equals 1).
3. It prints the result followed by a newline.

**Step 2: Generate a Patch**
Generate a standard unified diff patch file named `/home/user/math_pipeline/fix.patch` that represents the changes you made to `factorial.c`. An automated system will verify that applying this patch to the original buggy code results in your fixed code.

**Step 3: Reverse Proxy Configuration**
We want to expose this service via a TCP reverse proxy. Create an Nginx configuration file at `/home/user/math_pipeline/proxy.conf`.
The configuration should set up a TCP proxy (using the `stream` block, not `http`) that:
- Listens on port `9090`.
- Proxies incoming TCP connections to `127.0.0.1:8080`.

*Note: Since you do not have root access, ensure your Nginx config writes its `pid` file, `access_log`, and `error_log` to paths inside `/home/user/math_pipeline/` to avoid permission denied errors.*

**Step 4: CI/CD Pipeline Script**
Write a fully automated bash script `/home/user/math_pipeline/ci.sh` that does the following when executed:
1. Compiles your fixed `factorial.c` into an executable named `factorial`.
2. Starts the backend service on port 8080 in the background. Use `socat` to listen on port 8080 and execute your compiled `./factorial` program for every incoming connection. (e.g., `socat TCP-LISTEN:8080,fork,reuseaddr EXEC:./factorial`).
3. Starts the Nginx reverse proxy in the background using your `proxy.conf` file.
4. Waits briefly (e.g., 1-2 seconds) to ensure the services are up.
5. Tests the full pipeline by sending the string `"20\n"` to the Nginx reverse proxy on port 9090 (using `nc` or similar core tools) and captures the output.
6. Writes the exact output of the test (just the numeric result) to `/home/user/math_pipeline/test_result.log`.
7. Gracefully shuts down the background Nginx and socat processes before exiting.

Ensure `/home/user/math_pipeline/ci.sh` is executable. You can test your pipeline manually to verify it successfully writes the correct factorial of 20 to the log file.