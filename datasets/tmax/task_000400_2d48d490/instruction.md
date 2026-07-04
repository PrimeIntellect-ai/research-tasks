You are acting as a DevSecOps engineer. We have a custom C++ data proxy application that enforces a "policy-as-code" firewall rule, requires TLS certificates to start, and processes an incoming traffic log. 

Unfortunately, the proxy application has a security vulnerability, is missing its required TLS certificates, and doesn't have a configured network policy.

Your task is to fix the environment and code, then run the data proxy.

Here are your instructions:

1. **Code Auditing & Patching (CWE Identification)**
   The source code for the proxy is located at `/home/user/src/data_proxy.cpp`. It reads traffic data and copies it into a fixed-size buffer. 
   - Identify the CWE-120 (Buffer Overflow) vulnerability in the file.
   - Modify the C++ code to safely copy the string without overflowing the 64-byte buffer. Make sure the resulting string is properly null-terminated. Do not change the buffer size.

2. **TLS/SSL Certificate Management**
   The application will fail to start if it doesn't find a TLS certificate and key.
   - Create a directory `/home/user/certs/`.
   - Generate a self-signed RSA-2048 certificate and private key using OpenSSL.
   - Save the certificate as `/home/user/certs/server.crt` and the key as `/home/user/certs/server.key`.
   - The certificate should have the Common Name (CN) set to `localhost` and be valid for 365 days.

3. **Firewall Policy Configuration**
   The proxy enforces network drops based on a configuration file.
   - Create a file at `/home/user/rules.conf`.
   - Add exactly one rule to block the IP address `10.99.0.42`. The format must be exactly: `BLOCK=10.99.0.42`.

4. **Execution**
   - Compile the fixed C++ application: `g++ -o /home/user/data_proxy /home/user/src/data_proxy.cpp`
   - Run the application, passing the provided traffic log and specifying the output file:
     `/home/user/data_proxy /home/user/data/traffic.txt /home/user/output.log`

If you have completed the task successfully, the application will not crash (segfault), it will successfully read the certificates, apply the blocklist policy, and `/home/user/output.log` will contain the processed (and correctly truncated) traffic data.