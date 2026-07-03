You are acting as a network security engineer investigating a suspicious login flow on our custom web application. We captured a snippet of the malicious traffic that was exploiting an open redirect vulnerability, but it was obfuscated and captured as an image screenshot by our automated threat-intel scraper.

Your task is to analyze this image, extract the malicious payload, and build a lightweight Intrusion Detection System (IDS) sink in C to intercept and validate future exploit attempts.

Step 1: Payload Extraction
An image of the captured payload is located at `/app/suspicious_login.png`. Extract the text from this image. The text contains a base64 encoded string. Decode it. 
The decoded payload will have the format: `EXPLOIT_TOKEN:<token_string>|HASH:<sha256_hash>`. 
Verify that the SHA256 hash matches the `<token_string>`.

Step 2: IDS Sink Implementation
Write a C program named `/home/user/ids_sink.c` and compile it to `/home/user/ids_sink`.
The program must act as a TCP server listening on port 8080 (localhost).
When a client connects and sends data, the server must perform pattern matching to detect the open redirect attempt. 
Specifically, if the incoming TCP payload contains the exact substring `GET /login?redirect=` followed anywhere in the same request by the `<token_string>` you extracted, the server must respond exactly with the string `ALERT: MALICIOUS REDIRECT DETECTED\n` and close the connection.
If the payload does not match this pattern, the server should respond with `OK\n` and close the connection.
The server must handle multiple sequential connections (it does not need to be multithreaded, a simple accept loop is fine).

Step 3: Execution
Start your compiled C program in the background so it is listening on `127.0.0.1:8080`.