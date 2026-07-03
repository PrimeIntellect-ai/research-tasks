You are a build engineer tasked with modernizing and securing an old artifact management pipeline. 

We currently rely on an unmaintained, undocumented stripped binary located at `/app/migrator_legacy`. This binary reads a v1 JSON artifact schema from standard input and outputs a migrated v2 JSON schema to standard output. However, it is vulnerable to malicious inputs and crashes under load.

Your objective is to create a robust REST API natively in Bash that performs the schema migration and strictly filters out malicious payloads.

Requirements:
1. **API Construction:** Write a Bash script at `/home/user/server.sh` that listens on TCP port 8000. It must accept HTTP `POST` requests to the endpoint `/api/v2/migrate` containing a JSON body. (You may use tools like `nc` or `socat` available on standard Linux).
2. **Schema Migration & Code Translation:** Reverse-engineer the exact JSON transformation logic of the `/app/migrator_legacy` binary by feeding it sample inputs. Re-implement this transformation natively in your Bash script using `jq`. Your final script **must not** execute the legacy binary.
3. **Adversarial Filtering:** The legacy binary processes everything, which is a security risk. We have captured samples of attacks. Inspect the malicious JSON payloads in `/app/corpus/evil/` and the safe payloads in `/app/corpus/clean/`. Deduce the patterns that distinguish malicious inputs from clean ones. 
   - If an incoming JSON payload matches the malicious patterns, your API must respond with an HTTP `403 Forbidden` status and the exact body `REJECTED`.
   - If the payload is safe, perform the schema migration and respond with an HTTP `200 OK` status, returning the migrated v2 JSON as the body.

Make sure your script correctly parses the HTTP request headers to extract the JSON body, processes it, and sends back a valid HTTP response. Ensure your script is executable and can run persistently. Leave the server running in the background when you are finished.