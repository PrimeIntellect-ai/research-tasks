You are managing a local, file-based Kubernetes operator that monitors manifest files and applies them to a local control plane. 

Your task is to create a health-check and diagnostics script for this operator. You can write the script in any language you prefer (e.g., Bash, Python). 

The script must perform the following checks:
1. **Storage Monitoring**: Calculate the total size in bytes of all `.yaml` files inside the directory `/home/user/manifests`.
2. **Connectivity Diagnostics**: Verify if the local control plane API is reachable by checking if it can connect to `127.0.0.1` on port `8080`.

After performing these checks, the script must generate a JSON file at `/home/user/operator_status.json` with the exact following structure:
```json
{
  "status": "healthy",
  "manifest_bytes": 12345,
  "api_reachable": true
}
```

**Rules for the JSON output:**
- `manifest_bytes`: (Integer) The total byte size of all `.yaml` files in the `/home/user/manifests` directory.
- `api_reachable`: (Boolean) `true` if a connection to `127.0.0.1:8080` succeeds, `false` otherwise.
- `status`: (String) Must be `"healthy"` if `api_reachable` is `true` AND `manifest_bytes` is less than or equal to `1048576` (1 MB). If either condition is not met, the status must be `"unhealthy"`.

Once you have written the script, execute it so that `/home/user/operator_status.json` is successfully created with the current system state.