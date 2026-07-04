You are an engineer setting up a simple but robust CI/CD pipeline and build system for a Go-based REST API.

Please complete the following steps to create a polyglot build pipeline from scratch:

1. **Setup the Project**:
   - Create a directory at `/home/user/polybuild`.
   - Initialize a Go module named `polybuild` inside this directory.

2. **Implement the API (`main.go`)**:
   - Write a Go HTTP server in `/home/user/polybuild/main.go`.
   - The server must listen on port `8080`.
   - It should have a global string variable named `Version` initialized to `"dev"`.
   - Implement a `GET /version` endpoint that returns the value of the `Version` variable as plain text.
   - Implement a `GET /data` endpoint that returns the following exact plain text (4 lines):
     ```
     zebra
     alpha
     charlie
     bravo
     ```

3. **Create the Test Fixture (`expected.txt`)**:
   - Create a file `/home/user/polybuild/expected.txt` that contains the alphabetically sorted version of the lines returned by the `/data` endpoint.

4. **Implement the CI Pipeline (`ci.sh`)**:
   - Create an executable bash script at `/home/user/polybuild/ci.sh`.
   - The script must perform the following actions:
     a. Build the Go application into an executable named `server` in the same directory. During the build step, use Go's `ldflags` to inject the value `"1.2.3"` into the `main.Version` variable.
     b. Start `./server` in the background and save its PID.
     c. Wait for 1-2 seconds to ensure the server is ready.
     d. Use `curl` to fetch the `/version` endpoint and save the response to `/home/user/polybuild/actual_version.txt`.
     e. Use `curl` to fetch the `/data` endpoint, pipe the output to the `sort` command, and save the result to `/home/user/polybuild/actual_data.txt`.
     f. Use `diff` to compare `actual_data.txt` with `expected.txt`.
     g. Check if `actual_version.txt` contains exactly `1.2.3` and if the `diff` command succeeded (exit code 0).
     h. If both conditions are met, write the exact string `CI_PASS` to `/home/user/polybuild/ci_result.log`. If not, write `CI_FAIL`.
     i. Terminate the background server process using its PID.

5. **Run the Pipeline**:
   - Execute `/home/user/polybuild/ci.sh` to test your setup. Ensure it runs successfully and generates the `CI_PASS` log.