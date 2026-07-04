You are a security engineer tasked with rotating credentials and securing an internal C++ authentication microservice.

Currently, the service uses a hardcoded legacy key to validate HTTP cookies. The legacy key has been compromised. You must rotate the key to a new secure value, test the service by crafting a valid administrative payload, and generate firewall rules to block IPs that previously sent malformed or invalid authentication data.

Here are your detailed instructions:

1. **Rotate Credentials in Code:**
   You will find the source code for the authentication service at `/home/user/auth_server.cpp`. 
   - Inspect the code. You will see a hardcoded `SECRET_KEY` currently set to `"LEGACY_KEY_884"`.
   - Change the `SECRET_KEY` in `/home/user/auth_server.cpp` to `"NEW_SECURE_KEY_2024"`.
   - Compile the updated code to `/home/user/auth_server` using `g++`.

2. **Craft an Administrative Payload:**
   To verify the new key works, you must craft a raw HTTP request payload that would successfully authenticate as an administrator under the *new* key.
   - The server expects the payload via standard input. It reads HTTP headers and looks for a `Cookie:` header.
   - The cookie must be formatted exactly as `session=DATA:HASH`.
   - To gain admin access, the `DATA` portion must be exactly `role=admin`.
   - The `HASH` must be the valid hex-encoded XOR hash of `role=admin` using `"NEW_SECURE_KEY_2024"`. (You can analyze the `compute_hash` function in the C++ source to see how this is calculated).
   - Save your raw HTTP request (including the valid Cookie header) to `/home/user/admin_payload.http`. 
   - If you pipe this file into your compiled `/home/user/auth_server`, it should output `Access Granted: Admin`.

3. **Analyze Logs & Generate Firewall Rules:**
   You have been provided a historical traffic log at `/home/user/traffic.log`. The log contains raw cookie strings sent by various IP addresses when the *old* key (`"LEGACY_KEY_884"`) was active.
   - Format of the log: `<IP_ADDRESS> <COOKIE_STRING>`
   - Inspect the cookies in the log. A cookie is considered *invalid/malicious* if the hash does not match the valid hash for the given data using the *old* key (`"LEGACY_KEY_884"`).
   - Identify all IPs that sent invalid or malicious cookies.
   - Create a bash script at `/home/user/firewall_rules.sh` that blocks these malicious IPs.
   - The script must contain exactly one line per malicious IP, in the format: `iptables -A INPUT -s <IP_ADDRESS> -j DROP`
   - Sort the iptables commands alphabetically by IP address.

All final output files (`/home/user/auth_server`, `/home/user/admin_payload.http`, and `/home/user/firewall_rules.sh`) must be precisely in the specified locations and formats.