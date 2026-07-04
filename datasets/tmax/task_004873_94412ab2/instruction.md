As a cloud architect migrating our legacy services to a new infrastructure, I need you to set up a new connection gateway and its supervision. 

We received an architecture diagram as an image located at `/app/arch.png`. It contains the target SSH gateway hostname, port, and a specific rejection code that must be returned when an unauthorized key is used. 

Your task:
1. Extract the `Hostname`, `Port`, and `RejectionCode` from the image `/app/arch.png`. You can use the preinstalled OCR tools (like `tesseract`) or any other method.
2. Write a Rust program named `/home/user/gateway_simulator` (source code in `/home/user/gateway/src/main.rs`) that acts as a simple TCP server listening on the extracted `Port` on `127.0.0.1`.
3. When the Rust server receives a connection, it must immediately send back the exact `RejectionCode` string followed by a newline, and then close the connection. This simulates our new silent-reject SSH policy.
4. Write a robust bash script at `/home/user/supervisor.sh` that continuously runs the Rust `gateway_simulator` process. If the process crashes or is killed, the script must restart it within 1 second. The script should be running in the background.
5. Create a file `/home/user/migration_summary.txt` containing the extracted values in this exact format:
```
HOST=<Extracted Hostname>
PORT=<Extracted Port>
CODE=<Extracted RejectionCode>
```

Ensure the server can handle at least 100 concurrent connection requests per second. We will benchmark the Rust server's performance to ensure it meets our throughput requirements for the migration.