You are tasked with deploying a secure web proxy and filtering service for our legacy backend. As a system administrator, you must handle the virtualization setup, web server configuration, and develop a critical WAF (Web Application Firewall) script in Python to protect the backend.

Our backend authentication validator is a proprietary, legacy compiled service. Unfortunately, we lost the source code, and it occasionally crashes or behaves erratically when fed specific malformed JSON payloads. We have provided a stripped version of this binary at `/app/legacy_auth_daemon`. 

Your tasks are:
1. **Virtualization Setup**: Launch a QEMU virtual machine in the background using the disk image provided at `/app/backend_vm.qcow2`. Configure user-mode networking to forward host port 8080 to the guest port 80.
2. **TLS Configuration**: Generate a self-signed SSL certificate and configure a local lightweight Python web server on host port 8443 that accepts HTTPS traffic.
3. **WAF Implementation (Python)**: Write a WAF script located at `/home/user/waf_filter.py`. This script must expose a function `def filter_request(payload_string: str) -> bool:`. 
    * The function must return `True` if the payload is safe, and `False` if it is malicious.
    * You will need to reverse-engineer or black-box test the `/app/legacy_auth_daemon` binary to understand what causes it to return a non-zero exit code or crash. The binary takes a JSON string as a command-line argument: `./legacy_auth_daemon '<json_payload>'`.
    * Ensure your WAF script correctly identifies the malicious payloads that break the daemon while allowing safe traffic to pass.
4. **Integration**: Create a systemd-style start script at `/home/user/start_services.sh` that boots the QEMU VM, starts your local HTTPS proxy server, and ensures they are running smoothly.

Note: Your WAF implementation (`/home/user/waf_filter.py`) will be tested against a hidden suite of benign and malicious payloads. Your filter must perfectly distinguish between them.