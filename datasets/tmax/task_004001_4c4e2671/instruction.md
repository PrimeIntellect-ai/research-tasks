You are an incident responder investigating a compromised Linux web backend. The backend is a CGI binary written in Rust, located at `/home/user/backend_cgi`. 

We suspect the CI/CD pipeline was compromised, and the compiled binary contains a backdoor that is not present in our source code repository. The attacker injected a hidden HTTP handler and a hardcoded authentication token.

Your objectives are:
1. **Reverse Engineering & ELF Analysis**: Analyze the `/home/user/backend_cgi` ELF binary. Find the hardcoded backdoor token. We know the token starts with the prefix `BDR_`.
2. Locate the memory address of the backdoor function. The injected function is named `secret_backdoor_handler` (it may be mangled, but will contain this substring).
3. **Report**: Create a file at `/home/user/incident_report.txt` with exactly two lines:
   - Line 1: The exact token string starting with `BDR_`
   - Line 2: The hex memory address of the `secret_backdoor_handler` symbol (e.g., `00000000000081a0`, without the `0x` prefix, padded with zeros as output by standard `nm` or `readelf`).
4. **Remediation (Rust)**: Write a Rust program at `/home/user/patcher.rs` that automates patching this vulnerability in the binary. The Rust program must:
   - Read the binary file path from the first command-line argument.
   - Search for the exact bytes of the `BDR_...` token you discovered.
   - Overwrite the first 4 bytes of the token (`BDR_`) with `FIX_`.
   - Write the patched binary to a new file, where the new filename is the original filename with `_patched` appended (e.g., `backend_cgi_patched`).

Do not execute the patcher on the original binary yourself—our automated verification system will compile your `patcher.rs` and test it against a fresh copy of the binary. Just leave the source code at `/home/user/patcher.rs` and the report at `/home/user/incident_report.txt`.