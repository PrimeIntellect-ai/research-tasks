You are a Site Reliability Engineer tasked with setting up a configuration-driven uptime monitoring system. You need to build a pipeline where updating a Git repository automatically triggers a custom Rust-based network health checker to verify service availability.

Your task consists of the following steps:

1. **Git Server Configuration**:
   - Create a bare Git repository at `/home/user/uptime_repo.git`.
   - Create a `post-receive` hook in this repository. When code is pushed, the hook must check out the contents of the `master` branch into `/home/user/uptime_config` (create this directory).
   - After checking out the configuration, the hook must automatically execute the compiled Rust binary located exactly at `/home/user/monitor_bin`.

2. **Rust Uptime Monitor**:
   - Initialize a new Rust project in `/home/user/monitor_src`.
   - Write a Rust program that reads a file named `endpoints.txt` located in `/home/user/uptime_config/`. This file will contain a list of HTTP URLs, one per line.
   - For each URL in the file, the program must perform an HTTP GET request.
   - It must evaluate the HTTP status code. If the code is `200 OK`, the status is `UP`. For any other status code or if the connection fails, the status is `DOWN`.
   - The program must append the results to `/home/user/uptime_results.log` in the exact following format, one per line:
     `<URL> is <UP|DOWN>`
     *(Example: `http://127.0.0.1:9999/status is UP`)*
   - Build the project and place the final executable binary at `/home/user/monitor_bin`. Ensure it is executable.

3. **Testing the Pipeline**:
   - Clone your bare repository to `/home/user/uptime_client`.
   - Inside the client repository, create the file `endpoints.txt`.
   - Add the following two URLs to `endpoints.txt`:
     `http://127.0.0.1:8080/health`
     `http://127.0.0.1:8081/health`
   - Commit this file with the message "Add endpoints" and push it to the bare repository's `master` branch.

If you have set everything up correctly, pushing the commit will trigger the hook, checkout the endpoints file, run your Rust network monitor, and populate `/home/user/uptime_results.log`.

Note: Local servers on ports 8080 and 8081 are already running in the background for this test.