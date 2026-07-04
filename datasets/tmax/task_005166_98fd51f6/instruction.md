You are a container and deployment specialist managing a fleet of QEMU-based micro-VMs. We have an automated pipeline that submits deployment configuration requests (in JSON format) to provision new services. However, we've detected malformed and potentially malicious deployment requests attempting to escape directory isolation or hijack privileged ports.

Your task is to write a Python script at `/home/user/validate_deployment.py` that acts as a strict configuration sanitizer and deployment preparer.

The script must accept exactly one CLI argument: the absolute path to a JSON configuration file.

Each JSON file has the following schema:
```json
{
  "service_name": "auth-service",
  "vnc_port": 5904,
  "vm_image_path": "auth_service_v2.qcow2",
  "cluster_id": "..."
}
```

Your script must enforce the following validation rules:
1. **Port Security**: The `vnc_port` must be an integer between `5900` and `5999` (inclusive).
2. **Directory Isolation**: The `vm_image_path` is provided as a relative path. When resolved against the base directory `/home/user/images/`, the absolute normalized path must strictly reside *inside* `/home/user/images/`. It must not traverse out using `../` or symlink attacks.
3. **Cluster Authorization**: The `cluster_id` in the JSON must exactly match the authoritative Cluster ID. The authoritative Cluster ID is embedded in a VNC boot error screenshot located at `/app/vnc_screenshot.png`. You will need to extract the ID from this image (e.g., using `pytesseract` and standard image processing).

If a configuration fails ANY of these rules, your script must:
- Print exactly `REJECT` to stdout.
- Exit with status code `1`.

If a configuration passes ALL rules, your script must:
- Print exactly `ACCEPT` to stdout.
- Idempotently ensure the directory `/home/user/deployments/<service_name>/` exists.
- Idempotently ensure a symlink `/home/user/deployments/<service_name>/latest` exists and points to the resolved absolute path of the VM image in `/home/user/images/`.
- Exit with status code `0`.

Ensure your script is robust and executable. We will test it against a hidden corpus of clean and malicious deployment configurations.