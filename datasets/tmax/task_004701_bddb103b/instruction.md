You are an incident responder investigating a rogue internal service running on a compromised host. You need to analyze the service, identify the compromised account, and exploit a known vulnerability to retrieve the stolen data (the flag).

Follow these steps to complete your investigation:

1. **Service Auditing:** The rogue HTTPS service is running on `127.0.0.1` on a port somewhere between `8000` and `9000`. Find which port it is listening on.
2. **Certificate Inspection:** The attackers left a clue in the service's SSL/TLS certificate. Retrieve the certificate presented by the service and extract the Common Name (CN) from the Subject. This CN is the exact username of the compromised administrator account.
3. **Exploit Crafting (Rust):** We suspect the service uses a flawed JWT implementation for its `/flag` endpoint. Specifically, it is vulnerable to the `alg: "none"` bypass.
   Create a new Rust project at `/home/user/exploit_project`. Write a Rust program that:
   - Constructs a JWT header indicating the `none` algorithm.
   - Constructs a JWT payload for the compromised administrator account you found in step 2 (the JSON payload must strictly be `{"user": "<extracted_CN>", "role": "admin"}`).
   - Encodes and formats these parts correctly to form a signature-less JWT.
   - Sends an HTTPS GET request to `https://127.0.0.1:<PORT>/flag` with the HTTP header `Authorization: Bearer <your_crafted_jwt>`. Since the service uses a self-signed certificate, your Rust client must be configured to accept invalid certificates (e.g., bypassing TLS validation).
4. **Data Retrieval:** The service will respond with the secret flag if the exploit is successful. Save the exact text of the flag to a file at `/home/user/flag.txt`.

Ensure your Rust project is properly initialized with `cargo` and includes any necessary dependencies in its `Cargo.toml`. You are permitted to use standard crates like `reqwest`, `base64`, `serde_json`, etc.