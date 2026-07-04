You are a compliance analyst tasked with generating an audit trail for internal applications. You have been provided with access logs, application certificates, and an untrusted reporting script.

Perform the following tasks using Bash and standard Linux tools:

1. **Certificate Validation**:
   Check the PEM certificates located in `/home/user/certs/`. Identify the single certificate that is currently expired. Write the full filename of this expired certificate (e.g., `app_name.pem`) to `/home/user/expired_cert.txt`.

2. **Log Parsing & Correlation**:
   The service name corresponds to the certificate filename without the `.pem` extension (e.g., if `app_name.pem` is expired, the service name is `app_name`). 
   Parse the access log at `/home/user/access.log` to find all entries where this specific expired service had a `STATUS: SUCCESS` event. 
   Extract the IP addresses from these successful events, sort them uniquely, and save them to `/home/user/suspect_ips.txt` (one IP per line).

3. **Process Sandboxing**:
   You need to generate a final JSON report using an internally provided, but untrusted, Python script located at `/home/user/generate_report.py`. Because this script is unvetted, it might attempt to exfiltrate data.
   You must execute this script within a network-isolated sandbox using `bwrap` (Bubblewrap). 
   
   Construct a `bwrap` command with the following strict constraints:
   - Network namespace must be unshared (completely isolated).
   - The root filesystem `/` must be bound as read-only.
   - The `/home/user` directory must be bound as read-write.
   - The command to run inside the sandbox is: `python3 /home/user/generate_report.py /home/user/suspect_ips.txt /home/user/audit_report.json`

If your `bwrap` command is correct, the script will detect the network isolation and safely output the required audit trail to `/home/user/audit_report.json`. If network isolation fails, the script will refuse to generate the correct report.