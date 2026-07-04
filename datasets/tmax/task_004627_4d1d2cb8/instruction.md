You are a security engineer building an automated supply-chain audit utility. A recent vulnerability check revealed that malicious actors are attempting to poison your build pipeline by serving compromised package versions with invalid checksums. Your project is currently failing to build due to peer dependency conflicts caused by avoiding these tampered packages.

Your task is to write a Bash script that fetches package manifests over a WebSocket connection, verifies the cryptographic integrity of the packages, resolves a valid dependency tree, and generates a safe CI/CD pipeline configuration.

**Step 1: Data Ingestion**
A local WebSocket server is running at `ws://localhost:9090`. It serves the current package catalog.
You may need to install a WebSocket client (like `websocat` or `wscat`) to interact with it.
When you connect to the server, it will send a series of text lines and then close the connection. Each line represents a package version and follows this exact format:
`PKG <package_name> <version> <sha256_hash> <base64_encoded_content> <dependency_requirement>`

*Example:*
`PKG core-lib 1.0.0 e3b0c442... [base64_string] web-framework=2.0.0`
*(Note: If a package has no dependency requirements, the last field will be `NONE`)*

**Step 2: Integrity Verification**
Write a Bash script at `/home/user/audit_resolver.sh` that reads this WebSocket stream.
For every package line, your script must decode the `<base64_encoded_content>` and compute its SHA-256 hash.
If the computed hash does NOT match the `<sha256_hash>` provided in the line, the package has been tampered with and must be **discarded**.

**Step 3: Constraint Satisfaction**
Your application requires exactly one valid version of each of the following three packages:
- `core-lib`
- `web-framework`
- `auth-plugin`

Using only the cryptographically valid packages from Step 2, find a combination of versions that satisfies all dependency requirements. A requirement like `web-framework=2.0.0` means that if you choose that package, you MUST also choose version `2.0.0` of `web-framework`. All chosen packages must be compatible with each other. There will be exactly one valid combination.

**Step 4: CI/CD Pipeline Setup**
Once your script has determined the correct, safe versions of the three packages, it must automatically generate a GitHub Actions workflow file at `/home/user/.github/workflows/secure_build.yml`.

The generated YAML file must exactly match this template, replacing the bracketed placeholders with the resolved version numbers:

```yaml
name: Secure Build
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    env:
      CORE_VERSION: [resolved_core-lib_version]
      WEB_VERSION: [resolved_web-framework_version]
      AUTH_VERSION: [resolved_auth-plugin_version]
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      - name: Install
        run: ./install.sh $CORE_VERSION $WEB_VERSION $AUTH_VERSION
```

**Requirements:**
- Your script must be written purely in Bash (`/home/user/audit_resolver.sh`), utilizing standard Linux utilities (e.g., `sha256sum`, `base64`, `awk`, `grep`).
- The script must perform the entire process (connecting to the WS server, validating hashes, resolving constraints, and writing the YAML file) automatically when executed.
- Ensure the output directory for the YAML file exists before writing to it.