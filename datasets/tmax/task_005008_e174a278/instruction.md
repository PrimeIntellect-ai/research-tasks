You are an internal penetration tester. You have been assigned to evaluate a poorly documented local development server running on a hardened Linux machine. 

Your reconnaissance has indicated that there is a local HTTPS web service running on `127.0.0.1` on port `8443`. It is known to have a hidden administrative endpoint at `https://127.0.0.1:8443/admin` that is protected by HTTP Basic Authentication.

Your objective is to gain access to this administrative endpoint and retrieve the secret flag. 

Here is your intelligence briefing:
1. **Username Enumeration:** The developers reused the TLS/SSL certificate's Subject Common Name (CN) as the administrative username. You must extract the certificate details from the running service to discover the username.
2. **Password Cracking:** The password is weak and exists in a provided dictionary file located at `/home/user/wordlist.txt`.
3. **Exploitation:** You must write a Python script to automate a brute-force attack against the `/admin` endpoint using the discovered username and the provided wordlist. Note: Since this is a local development server, it uses a self-signed certificate, so your script will need to ignore SSL verification warnings.

Once your script successfully authenticates to the `/admin` endpoint, the server will return a JSON response containing a `secret_flag`.

Create a final report file at `/home/user/loot.json` containing the exact credentials you found and the secret flag. The file must be valid JSON and match this exact structure:

```json
{
  "username": "<extracted_CN>",
  "password": "<cracked_password>",
  "secret_flag": "<flag_from_server>"
}
```