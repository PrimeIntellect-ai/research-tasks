You need to implement a lightweight Kubernetes Admission Webhook in C that acts as an adversarial manifest validator. Since standard operators are heavy, you are building a custom fast-path validator that parses YAML directly and runs as a user-level background service behind a TLS endpoint.

Your task has the following stages:

**1. Fix and Compile the Vendored YAML Parser**
We have vendored the source code for `libyaml-0.2.5` in `/app/libyaml-0.2.5`. 
However, it currently fails to compile due to a deliberate configuration perturbation injected during the vendoring process.
- Diagnose and fix the build error in the vendored package.
- Compile and install the library locally into `/home/user/local/` (so that `lib/` and `include/` are present there). 
*Note: Do not attempt to download a fresh version from the internet.*

**2. Develop the C Validator (`manifest_validator.c`)**
Write a C program at `/home/user/manifest_validator.c` that reads a YAML document from `stdin`.
- You must use the fixed `libyaml` library to parse the incoming YAML stream.
- The validator must scan the parsed YAML tokens/events for any scalar key exactly matching `hostNetwork` followed by a scalar value `true`.
- If `hostNetwork: true` is found anywhere in the YAML structure, the program must print exactly `REJECT` to `stdout` and exit with code `1`.
- If the document is parsed successfully and no such key-value pair is found, the program must print exactly `ACCEPT` to `stdout` and exit with code `0`.
- Compile this program to `/home/user/manifest_validator` linking against your locally installed `libyaml`.

**3. Configure TLS and the Webhook Service**
Admission webhooks must be served over HTTPS. 
- Generate a self-signed TLS certificate and private key combined into a single file at `/home/user/webhook.pem`.
- Create a user-level systemd service named `k8s-webhook.service` (placed in `~/.config/systemd/user/`).
- The service must use `socat` to listen on TCP port `8443` with TLS enabled using your `webhook.pem` certificate. It must accept incoming connections (with TLS verification disabled for clients) and `fork` and `exec` your `/home/user/manifest_validator` binary for each connection, piping the socket input to `stdin` and the stdout back to the socket.
- Enable and start this user service via `systemctl --user`.

Ensure your webhook service correctly handles standard Kubernetes Pod manifests, rejecting any that attempt to use the host network namespace.