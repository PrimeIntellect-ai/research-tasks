You are a systems engineer diagnosing a deployment issue with a custom email notification application. 

You have an application suite residing in `/home/user`. There is a backend mail dummy server running as a user-level systemd service (`backend-mailer.service`) listening on TCP port `2525`. It simply records incoming email payloads to `/home/user/mail_spool.log`.

Your goal is to configure a local port forward, fix a failing C++ notification service, and ensure it correctly sends an alert through the forwarded port upon startup.

Here are your specific tasks:

1. **Create a Port Forwarding Service:**
   Create a new user-level systemd unit file at `/home/user/.config/systemd/user/port-forward.service`. This service must run a `socat` command to listen on TCP port `10025` and forward all connections to `127.0.0.1:2525`. 
   * The service should keep running (use `Restart=always`).
   * It should be started using `systemctl --user`.

2. **Fix and Compile the C++ Mailer App:**
   There is a C++ source file at `/home/user/mailer_app.cpp`. It connects to a local port and sends a standard SMTP-like sequence.
   * However, it currently has a configuration error (it tries to connect to the wrong port). 
   * Edit `/home/user/mailer_app.cpp` so it connects to the port forwarder on `10025`.
   * Compile it to an executable named `/home/user/mailer_app` (using standard `g++`).

3. **Fix the Systemd Dependency (The Core Issue):**
   There is an existing user service at `/home/user/.config/systemd/user/mailer_app.service` that executes `/home/user/mailer_app`. 
   Currently, the service fails to start reliably because it doesn't wait for the port forwarder to be ready.
   * Modify `/home/user/.config/systemd/user/mailer_app.service` so that it strictly requires and starts *after* `port-forward.service`.

4. **Execution:**
   * Reload the user systemd daemon.
   * Start `port-forward.service`.
   * Start `mailer_app.service`.
   
If everything is configured correctly, the `mailer_app` will successfully send its message through the `socat` port forward into the `backend-mailer.service`, and `/home/user/mail_spool.log` will contain the string `STATUS: FIXED`. 

Ensure both services are running or have completed successfully (mailer_app.service is a `Type=oneshot` service).