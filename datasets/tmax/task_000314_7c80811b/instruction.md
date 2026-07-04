You are tasked with deploying and optimizing a local storage monitoring and log parsing daemon for our user-level server environment. We have a vendored package located at `/app/quotalogger-2.1` that needs to be fixed, optimized, and deployed as a user-level systemd service.

Currently, the deployment has several issues:
1. **Systemd Dependency Issue**: The service template `systemd/quotalogger.service` within the package fails to start reliably. It relies on a local mock database service called `mock-db.service` being fully started first, but it is missing the appropriate `After=` and `Requires=` directives to ensure correct ordering.
2. **Performance Bottleneck**: The core parsing logic in `quotalogger/parser.py` processes a large storage allocation log. The current implementation is highly inefficient (likely $O(N^2)$ due to nested loops or poor data structure choices). It currently takes over 15 seconds to parse our standard 50,000-line test log. 
3. **CI/CD Validation Pipeline**: We need a local shell script `/home/user/ci_check.sh` that acts as a continuous integration check. It must run the CLI tool, capture the output, and use `awk` and `grep` to extract the final summary statistics, writing them to `/home/user/ci_results.txt`.

**Your instructions:**

1. **Fix the Package**:
   - Edit the `quotalogger.service` file in `/app/quotalogger-2.1/systemd/` to include the correct dependencies on `mock-db.service`.
   - Optimize the `calculate_quotas` function in `/app/quotalogger-2.1/quotalogger/parser.py` using Python. The output logic must remain exactly the same, but you must improve its algorithmic complexity. The optimized execution time must be strictly less than 1.0 seconds when processing the provided test log at `/app/data/test_logs.txt`.

2. **Deploy the Service**:
   - Install the package locally in development mode (e.g., `pip install -e /app/quotalogger-2.1`).
   - Copy the fixed `quotalogger.service` to your user systemd directory (`~/.config/systemd/user/`, create it if necessary).
   - Reload the user systemd daemon and enable/start `quotalogger.service`.
   - *Note:* Assume `mock-db.service` is already set up and running in your user environment.

3. **Create the CI Pipeline Script**:
   - Write `/home/user/ci_check.sh`.
   - The script should execute `quotalogger-cli /app/data/test_logs.txt`.
   - Pipe the output through `grep` and `awk` to find the line starting with `TOTAL_USAGE:`.
   - Extract only the numeric value and save it to `/home/user/ci_results.txt`.
   - Ensure the script is executable.

We will verify your solution by checking the user systemd service status, running your CI script, and using an automated benchmarking script to measure the runtime of your `parser.py` implementation to ensure it meets the performance threshold.