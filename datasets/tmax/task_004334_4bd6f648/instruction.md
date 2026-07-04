You are an edge computing engineer deploying an IoT telemetry processing pipeline on a remote field device. You need to fix a broken vendored C++ package, set up a local Git-based deployment workflow, and configure a secure local tunnel for telemetry data routing.

Your tasks are to perform the following:

1. **Fix the Vendored Telemetry Processor:**
   A vendored package is located at `/app/telemetry-processor-1.0.0`. It contains a C++ application that reads raw byte streams from standard input, processes them, and outputs the result to standard output. 
   The intended behavior of the processor is to read `stdin` byte-by-byte, XOR each byte with the hex value `0x55`, and print the uppercase, zero-padded, two-character hexadecimal representation of each processed byte followed by a space (e.g., inputting "A" (0x41) should output `14 `).
   Currently, the package is broken:
   * The `Makefile` is misconfigured and fails to build the C++ code properly.
   * The processing logic in `processor.cpp` contains a bug causing incorrect byte transformations.
   Fix the source code and the Makefile so that running `make` successfully produces an executable named `telemetry_processor` that performs the exact expected transformation.

2. **Configure Local Git Deployment:**
   To allow remote updates to the device, set up a local deployment pipeline:
   * Initialize a bare Git repository at `/home/user/device-repo.git`.
   * Create a `post-receive` Git hook in this repository.
   * When code is pushed to this repository, the hook must:
     a) Check out the latest code to a working directory at `/home/user/build_workspace`.
     b) Compile the code by running `make` in `/home/user/build_workspace`.
     c) Copy the resulting `telemetry_processor` binary to `/home/user/deploy/telemetry_processor`.
     d) Write the exact string `DEPLOYMENT_SUCCESS` to a log file at `/home/user/deploy/deploy.log`.
   * **Crucial Constraint:** Similar to a cron job environment, the git hook runs with a severely restricted `PATH`. Your hook script must explicitly set its `PATH` to include standard binary directories (`/usr/bin`, `/bin`, etc.) before executing any commands, or the build will fail silently and output to the wrong location.

3. **Deploy the Fixed Code:**
   Initialize a standard Git repository inside `/app/telemetry-processor-1.0.0`, commit your fixed files, add the bare repository `/home/user/device-repo.git` as a remote named `local`, and push the `master` branch to trigger your hook.

4. **Configure Telemetry Routing (SSH Tunnel):**
   The edge device's internal telemetry gateway sends raw data to local port `7070`. The data aggregator listens on local port `8080`. 
   Using SSH, set up a background local port forward to tunnel traffic arriving on `localhost:7070` to `localhost:8080`. 
   (Assume passwordless SSH access to `user@localhost` is already configured).

Complete these steps ensuring the final compiled binary at `/home/user/deploy/telemetry_processor` functions flawlessly and the tunnel is active.