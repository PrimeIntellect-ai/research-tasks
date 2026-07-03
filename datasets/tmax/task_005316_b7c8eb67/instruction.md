You are a cloud architect migrating an internal legacy service to a secure architecture. 

Currently, there is a simple plaintext HTTP service running locally on port `8080` (assume this process is already running in the background and responds to GET requests on `/` with a 200 OK).

Your task is to wrap this service with TLS and create a custom compiled health monitor to ensure the secure endpoint is functioning correctly.

Perform the following steps:

1. **Install Dependencies:** Ensure you have the necessary tools installed. You will need `socat`, `gcc`, `make`, `openssl`, and the `libcurl` development headers (e.g., `libcurl4-openssl-dev`). You can use `sudo apt-get` if necessary, or just run it as user if you have passwordless sudo or if they are already installed. (Assume you have standard user privileges, but can install packages using `sudo apt-get install -y`).

2. **Generate TLS Certificates:**
   Create a self-signed certificate and private key at `/home/user/cert.pem` and `/home/user/key.pem` respectively. Do not use a passphrase. Set the Common Name (CN) to `localhost`.

3. **Set up a TLS Reverse Proxy:**
   Use `socat` to start a background process listening on port `8443` with TLS, using your generated certificate and key. It should forward incoming connections to the legacy plaintext service on `127.0.0.1:8080`. Ensure it does not enforce client certificate verification (`verify=0`).

4. **Write a C Health Monitor:**
   Write a C program at `/home/user/monitor.c` that monitors the new secure proxy. 
   - The program must use `libcurl` (`#include <curl/curl.h>`).
   - It should perform an HTTPS GET request to `https://127.0.0.1:8443/`.
   - Because it's a self-signed certificate, configure `libcurl` to ignore SSL certificate and host verification errors (`CURLOPT_SSL_VERIFYPEER` and `CURLOPT_SSL_VERIFYHOST` set to `0L`).
   - The program should loop and make exactly **3 requests**, pausing for 1 second (`sleep(1);`) between each request.
   - For each request, if the `curl_easy_perform` succeeds AND the HTTP response code is `200`, it should append the string `SUCCESS\n` to a file located at `/home/user/monitor.log`. Otherwise, it should append `FAILURE\n`.

5. **Compile and Run the Monitor:**
   Compile your code using `gcc -o /home/user/monitor /home/user/monitor.c -lcurl`.
   Finally, execute the `/home/user/monitor` binary so that it populates the log file.

Ensure all file paths strictly match the instructions.