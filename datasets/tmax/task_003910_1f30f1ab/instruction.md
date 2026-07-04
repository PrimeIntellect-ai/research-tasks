You are assisting a FinOps analyst in deploying a lightweight, secure C++ API server that aggregates cloud instance spot pricing metrics, along with an automated reporting service.

Currently, we have the source code for the API server, but it needs to be compiled with TLS support, configured as a user-level systemd service, and linked with our local reporter script. 

Here is what you need to do:

1. **Compile the API Server**:
   You have a C++ source file at `/home/user/cost_api.cpp` and a header file at `/home/user/httplib.h`.
   Compile `/home/user/cost_api.cpp` into an executable named `/home/user/cost_api`. 
   The server relies on OpenSSL for TLS support and standard threading, so ensure you link the appropriate libraries (`ssl`, `crypto`, `pthread`).

2. **Generate TLS Certificates**:
   The API server expects a private key at `/home/user/key.pem` and a certificate at `/home/user/cert.pem`. 
   Generate a self-signed RSA 2048-bit certificate valid for 30 days without an interactive prompt. Use `/CN=localhost` for the subject.

3. **Configure the API systemd Service**:
   Create a user-level systemd service for the API server at `/home/user/.config/systemd/user/cost-api.service`.
   - The service should execute `/home/user/cost_api`.
   - It should restart always.
   - Set the working directory to `/home/user`.

4. **Fix and Configure the Reporter systemd Service**:
   There is an existing reporter script at `/home/user/reporter.sh` which sends a JSON payload to the API server via `curl`. 
   Create a systemd service for it at `/home/user/.config/systemd/user/cost-reporter.service`.
   - It must be a `Type=oneshot` service executing `/home/user/reporter.sh`.
   - **Crucial Fix**: The reporter must *not* start until the API server is fully active. Add the appropriate systemd directives so that `cost-reporter.service` explicitly requires and runs *after* `cost-api.service`.

5. **Start and Test**:
   - Reload the user systemd daemon.
   - Start `cost-api.service`.
   - Start `cost-reporter.service`.
   - If successful, the C++ server will receive the payload and write it to `/home/user/metrics.log`.

Make sure `/home/user/metrics.log` is successfully created by the API server and contains the reported JSON payload. Do not use `sudo` or root permissions; all systemd commands must use the `--user` flag.