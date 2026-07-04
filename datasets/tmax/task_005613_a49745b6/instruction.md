You are acting as a compliance analyst investigating a potential security breach on a Linux system. We have gathered forensic evidence, and you need to generate an audit trail report.

Here is the context and the files provided to you:
1. `/home/user/app_requests.log`: A JSON-formatted application log containing recent HTTP requests.
2. `/home/user/backend_worker.py`: The source code for a background task worker used by the application.
3. `/home/user/proc_dump/`: A directory containing a snapshot of the `/proc` filesystem taken during the suspected attack window.

Your task is to analyze these files and perform the following steps:

**Phase 1: Log Parsing & HTTP Inspection**
Analyze `/home/user/app_requests.log`. Identify the IP address of the attacker who successfully triggered an exploit by passing a malicious `Cookie` header that contains the substring `auth_bypass=`. 

**Phase 2: Code Auditing & CWE Identification**
Review `/home/user/backend_worker.py`. The script is vulnerable because it accepts sensitive database credentials as command-line arguments, which exposes them to the local system environment. Identify the most specific, standard CWE (Common Weakness Enumeration) ID that applies to "Invocation of Process Using Visible Sensitive Information" (e.g., exposing credentials via command line arguments or environment variables). Format your finding as `CWE-XXX`.

**Phase 3: Exploit / Artifact Extraction**
Because the application invokes the vulnerable script from Phase 2, the attacker's actions caused the script to be run with real credentials. Write a Python script (you can save it anywhere, e.g., `/home/user/extract.py`) to parse the simulated `/proc` snapshot at `/home/user/proc_dump/`. 
You must iterate through the process directories, read the `cmdline` files (which are null-byte `\x00` separated, exactly like a real Linux system), find the execution of `backend_worker.py`, and extract the database password that was passed to it as an argument.

**Phase 4: Audit Trail Generation**
Combine your findings into a strict JSON audit trail. Create a file at `/home/user/compliance_audit.json` with exactly the following format:

```json
{
  "attacker_ip": "<IP address from Phase 1>",
  "cwe_id": "<CWE-XXX from Phase 2>",
  "leaked_password": "<Password extracted in Phase 3>"
}
```

Ensure all paths referenced are absolute and correct. The final output must be valid JSON.