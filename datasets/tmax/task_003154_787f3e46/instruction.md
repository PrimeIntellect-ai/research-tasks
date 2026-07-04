You are an incident responder investigating a compromised Python web application. You have been provided with an artifact directory containing the application's source code and a captured TLS certificate chain used by the attacker's command and control (C2) server. 

Your task is to analyze these artifacts and produce a summary report of your findings.

The artifacts are located in: `/home/user/incident/`
1. `/home/user/incident/app.py`: The compromised Flask web application.
2. `/home/user/incident/cert_chain.pem`: The captured TLS certificate chain (containing the server certificate and the Root CA).

You need to identify:
1. The exact line number in `app.py` that contains a SQL Injection (SQLi) vulnerability.
2. The exact line number in `app.py` that contains a Cross-Site Scripting (XSS) vulnerability.
3. The Common Name (CN) of the Root Certificate Authority (CA) that issued the certificate chain in `cert_chain.pem`. Validate the chain to determine which certificate is the Root CA (the self-signed issuer at the top of the chain) and extract its CN.

Once you have identified these three pieces of information, create a JSON report at `/home/user/investigation_summary.json` with the exact following structure:

```json
{
  "sqli_line": <integer>,
  "xss_line": <integer>,
  "root_ca_cn": "<string>"
}
```

Constraints:
- You may use Python, OpenSSL, and standard Linux utilities to perform your analysis.
- Ensure the line numbers are integers and the CN is a string.
- Do not modify the original artifact files.