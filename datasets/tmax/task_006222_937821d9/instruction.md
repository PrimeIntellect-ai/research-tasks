You are a build engineer investigating a potential supply chain attack in your web application's Continuous Integration pipeline. The security team suspects a malicious Common Gateway Interface (CGI) binary was injected into the latest release to output anomalous HTTP headers.

Your workspace contains two build manifests:
1. `/home/user/build_v1_manifest.json` (Known good release)
2. `/home/user/build_v2_manifest.json` (Suspicious release)

The compiled artifacts are stored in `/home/user/artifacts/`.

Perform the following tasks:
1. Parse, sort, and diff the two JSON manifests to identify the newly added artifact in `v2`.
2. Analyze the newly added binary artifact using assembly-level analysis tools (like `objdump` or `strings`) to determine the exact suspicious HTTP header string it outputs.
3. Save the exact string (exactly as it appears in the binary's data section, including any carriage returns or newlines like `\r\n`) to `/home/user/injected_payload.txt`. 
4. Create a minimal end-to-end test script at `/home/user/test_artifact.sh` that executes the anomalous binary and verifies its output matches the extracted string. Ensure the script has executable permissions and exits with code 0 on success, or 1 on failure.

All files must be created in `/home/user/`. Do not use any external dependencies outside of standard Linux utilities and your chosen scripting language (e.g., Python, Bash).