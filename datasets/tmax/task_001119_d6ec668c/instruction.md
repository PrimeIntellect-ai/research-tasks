You are a DevOps engineer investigating why a custom Python webhook service fails to start. The service is managed by a lightweight, custom process supervisor that simulates systemd for user-level processes.

Currently, if you run the supervisor to start the service, it crashes immediately. Your task is to diagnose the issues, fix the code, configure proper logging, set up TLS, and finally create a mock CI/CD pipeline script to automate testing.

Here are your specific requirements:

1. **Fix the Webhook Service (`/home/user/webhook_service.py`)**
   - The service is designed to run an HTTPS server on port `8443`, but it is missing its TLS configuration. Generate a self-signed certificate and key. Save them as `/home/user/certs/cert.pem` and `/home/user/certs/key.pem`.
   - Update `webhook_service.py` to correctly load these TLS files so the server can start successfully over HTTPS.
   - The service currently crashes because it tries to write logs to a missing directory. Ensure the `/home/user/logs/` directory exists.
   - Modify the Python logging configuration inside `webhook_service.py`. It currently uses a basic file handler. Change it to use a `RotatingFileHandler` from the `logging.handlers` module. Configure it to write to `/home/user/logs/webhook.log` with a `maxBytes` of `1024` and `backupCount` of `3`.

2. **Create a CI/CD Verification Pipeline (`/home/user/ci_pipeline.sh`)**
   - Write a bash script at `/home/user/ci_pipeline.sh` (make it executable) that simulates a CI/CD deployment and test step.
   - The script must:
     a) Start the service using the supervisor: `/usr/bin/python3 /home/user/mock_systemd.py start webhook.service` (run this in the background).
     b) Wait a few seconds for the service to initialize.
     c) Use `curl` to make an HTTPS GET request to `https://localhost:8443/` (ignoring certificate validation errors since it's self-signed).
     d) Verify that the response body contains the exact string `"Webhook Service Online"`.
     e) If the string is found, output `CI SUCCESS`, gracefully terminate the background supervisor process, and exit with code `0`.
     f) If the string is not found or the connection fails, output `CI FAILED`, terminate the process, and exit with code `1`.

Your task is complete when `/home/user/ci_pipeline.sh` runs successfully, logs are being correctly rotated, and the service handles HTTPS traffic securely.