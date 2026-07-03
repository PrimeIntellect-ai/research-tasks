As a Site Reliability Engineer, you need to implement a continuous deployment pipeline for a custom health-check monitoring agent written in C.

Your objective is to stand up a local secure web server, create a Git repository with a deployment hook, and write a C program that performs an HTTPS health check.

Perform the following steps:

1. **TLS Web Server Setup:**
   - Create a directory at `/home/user/tls_web`.
   - Inside this directory, generate a self-signed TLS certificate (`cert.pem`) and private key (`key.pem`).
   - Create an empty file named `index.html` inside `/home/user/tls_web`.
   - Start a simple HTTPS web server listening on `127.0.0.1:8443` that serves the contents of `/home/user/tls_web`. Make sure it runs in the background (e.g., using Python's `http.server` and `ssl` modules) so you can continue your tasks.

2. **Git Repository & Hook Configuration:**
   - Initialize a bare Git repository at `/home/user/monitor.git`.
   - Create a `post-receive` hook in `/home/user/monitor.git/hooks/post-receive`. Ensure it is executable.
   - The hook must do the following when code is pushed:
     a) Check out the pushed code into `/home/user/monitor_deploy` (create this directory beforehand).
     b) Compile the file `checker.c` located in the deploy directory into an executable named `checker` using `gcc` and linking against `libcurl`.
     c) Execute `./checker` and redirect its standard output to `/home/user/hook_output.log`.

3. **C Health Checker Development:**
   - Clone your bare repository to `/home/user/monitor_src`.
   - In the cloned repository, write a C program named `checker.c`.
   - The C program must use `libcurl` to perform an HTTP GET request to `https://127.0.0.1:8443/index.html`.
   - Because the certificate is self-signed, configure `libcurl` to ignore SSL peer verification (`CURLOPT_SSL_VERIFYPEER` set to 0).
   - The program should extract the HTTP response status code and print exactly `STATUS: <code_number>` (e.g., `STATUS: 200`) to standard output, followed by a newline.
   - Commit `checker.c` and push it to the `master` branch of the `origin` (the bare repo).

Once you have pushed the commit, the hook should trigger automatically, compile the C code, run the health check against your TLS web server, and write the output to the log file.