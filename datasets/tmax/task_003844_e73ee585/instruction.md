You are a system administrator tasked with securely sharing some local assets over HTTPS for an internal microservice. Please perform the following setup:

1. Create two directories: `/home/user/app_content` and `/home/user/shared_assets`.
2. Inside `/home/user/shared_assets`, create a file named `logo.png` containing exactly the string: `FAKE PNG DATA`
3. Inside `/home/user/app_content`, create a symbolic link named `assets` that points to `/home/user/shared_assets`.
4. Create a directory `/home/user/tls`. Inside it, generate a self-signed RSA-2048 TLS certificate (`server.crt`) and an unencrypted private key (`server.key`) valid for 365 days. The Subject Common Name (CN) should be `localhost`.
5. Write a Python script at `/home/user/run_https.py` that starts a simple HTTPS web server. 
    - The server must listen on `localhost` port `9443`.
    - It must serve files from the `/home/user/app_content` directory.
    - It must use the `server.crt` and `server.key` generated in the previous step.
6. Run your Python script in the background so that the server remains active.

Ensure the server is running and reachable. An automated test will attempt to fetch `https://localhost:9443/assets/logo.png` using `curl -k` to verify success.