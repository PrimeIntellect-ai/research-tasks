You are an observability engineer tuning dashboards for a new internal system. You need to create a custom metrics exporter in C and securely route its traffic using SSH tunneling to simulate our production environment's scraping architecture.

Please perform the following steps:

1. **Write a Custom Exporter in C**:
   Create a C source file at `/home/user/exporter.c`. This program must:
   - Run as a simple HTTP server listening on `127.0.0.1` port `8000`.
   - On receiving *any* incoming request, it should read the contents of the file `/home/user/dashboard_data/metrics_source.txt`.
   - It must respond with a valid `HTTP/1.1 200 OK` header, `Content-Type: text/plain`, followed by the exact contents of the `metrics_source.txt` file in the response body.
   - Compile this program to `/home/user/exporter` and start it as a background process.

2. **Configure SSH Port Forwarding**:
   Our dashboard scraper expects to connect to port `9090`. Set up a local SSH port forward so that traffic sent to `127.0.0.1:9090` is forwarded to `127.0.0.1:8000`.
   - Connect to `user@127.0.0.1` using SSH.
   - Use the pre-existing SSH key located at `/home/user/.ssh/id_rsa`.
   - Ensure the SSH tunnel runs in the background (e.g., using the `-f` and `-N` flags).

3. **Verify the Pipeline**:
   Test the entire pipeline by using `curl` to fetch the metrics through the SSH tunnel:
   - Make a GET request to `http://127.0.0.1:9090/`.
   - Save the raw response body (excluding HTTP headers) to `/home/user/dashboard_test.log`.