You are a network engineer tasked with securing a legacy network traffic analysis pipeline located in `/home/user/network_tools`. The current pipeline has multiple security flaws, including credential leakage via command-line arguments visible in `/proc`, and plain-text transmission of logs.

Your objective is to secure the pipeline by completing the following steps:

1. **Verify Integrity**:
   Verify the SHA384 checksum of the existing script `/home/user/network_tools/analyzer.py` against the hash provided in `/home/user/network_tools/checksum.txt`. If the hash does not match, log "INTEGRITY_FAILURE" to `/home/user/network_tools/receipt.txt` and exit. (Assume it matches for the rest of the steps).

2. **Fix Credential Leakage**:
   The script `analyzer.py` currently accepts a highly sensitive token via the `--secret-token` command-line argument, which exposes it to all users on the system via `/proc`. 
   Modify `analyzer.py` so that it no longer accepts `--secret-token` as a command-line argument. Instead, it must securely read the token from an environment variable named `ANALYZER_TOKEN`. Keep the `--data` argument unchanged. The output logic of the script must remain exactly the same.

3. **Run the Analysis**:
   Run your modified `analyzer.py` against the dummy pcap file `/home/user/network_tools/traffic.pcap`. 
   Provide the token `SECURE_TOKEN_8842` via the `ANALYZER_TOKEN` environment variable. This will generate a file named `/home/user/network_tools/analysis.log`.

4. **TLS Certificate Generation**:
   Generate a self-signed RSA-2048 TLS certificate (`server.crt`) and private key (`server.key`) valid for `localhost`. Store them in `/home/user/network_tools/`.

5. **Secure Transmission System**:
   Write two new Python scripts:
   * `/home/user/network_tools/secure_receiver.py`: A TLS server that listens on `127.0.0.1:8443` using the generated certificate and key. It should accept exactly one connection, read all incoming data until the client disconnects, compute the SHA256 hex digest of the received data, write only this hex digest to `/home/user/network_tools/receipt.txt`, and then exit.
   * `/home/user/network_tools/secure_sender.py`: A TLS client that connects to `127.0.0.1:8443` (ignoring self-signed certificate validation errors), reads the entire contents of `/home/user/network_tools/analysis.log`, sends the contents over the encrypted socket, and closes the connection.

6. **Execution**:
   Start the receiver in the background, run the sender to transmit the log securely, and ensure `receipt.txt` is successfully written.

Ensure all paths are absolute and exactly as specified.