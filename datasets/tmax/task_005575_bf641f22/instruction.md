You are a security auditor performing a baseline security check on a staging environment directory located at `/home/user/audit`. You need to investigate file permissions, network configurations, certificate validity, and source code vulnerabilities.

Please perform the following tasks using standard Linux CLI tools and generate a final report at `/home/user/audit_report.txt`.

**1. File Permissions**
Find all files within `/home/user/audit/code` that are world-writable (o+w). 

**2. Certificate Chain Validation**
There are several certificates in `/home/user/audit/certs/`. You have a trusted CA certificate at `/home/user/audit/certs/ca.pem`. Validate the leaf certificates (`leaf1.pem`, `leaf2.pem`, `leaf3.pem`) against this CA. Identify the single leaf certificate that fails validation.

**3. Vulnerability Analysis**
Analyze the source code files in `/home/user/audit/code/`. Find the single file that contains a direct Reflected Cross-Site Scripting (XSS) vulnerability (specifically, look for a PHP file that directly echoes unencoded user input from the `$_GET` array).

**4. Firewall Policy Configuration**
Review the saved iptables rules in `/home/user/audit/firewall/iptables.rules`. Identify the TCP port number that is explicitly configured to `ACCEPT` incoming traffic from any source (`0.0.0.0/0` or missing source restriction), excluding the standard web ports (80 and 443). 

**Output Format**
Create the file `/home/user/audit_report.txt` exactly matching the following format (replace the bracketed placeholders with your findings). Do not include paths in the filenames, just the basenames:

```text
[PERMISSIONS]
<world-writable-filename-1>
<world-writable-filename-2>
(alphabetical order if multiple)

[CERTIFICATES]
<invalid-leaf-filename>

[VULNERABILITIES]
<vulnerable-source-filename>

[FIREWALL]
<exposed-tcp-port-number>
```