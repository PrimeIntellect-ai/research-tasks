You are a system administrator maintaining a fleet of QEMU virtual machines. Users submit their VM provisioning requests in the form of JSON payloads. Recently, there have been attempts to submit malicious requests that exploit environment variables, request privileged users, or bypass our token validation.

Your task is to write a Python 3 classification script at `/home/user/filter_vm_requests.py` that determines if a given VM request JSON file is benign ("clean") or malicious ("evil").

The script must accept a single command-line argument: the path to the JSON file to inspect.
- If the request is benign, the script must exit with status code `0`.
- If the request is malicious, the script must exit with status code `1` (or any non-zero value).

A request is considered **benign** if and only if ALL of the following conditions are met:
1. **User Validation**: The `username` specified in the JSON must already exist on the local system. Furthermore, the user must NOT be a member of the `sudo` or `wheel` groups (neither as their primary group nor as a supplementary group).
2. **VNC Configuration**: The `vnc_display` field must be an integer between `1` and `99` (inclusive), representing standard QEMU VNC displays (ports 5901-5999). 
3. **Environment Variables**: The `env` dictionary field must not contain any keys that include the substrings `PRELOAD` or `BASH_ENV`.
4. **Token Validation**: The `vm_token` string field must be accepted by our legacy authorization binary. This binary is located at `/app/check_token`. It is a stripped executable. You must pass the token to it as the first command-line argument (`/app/check_token <vm_token>`). The binary will return exit code `0` if the token is valid, and a non-zero exit code if it is invalid.

If ANY of these conditions are violated, the request is considered **malicious**.

Here is an example of a JSON request format:
```json
{
  "username": "devuser",
  "vnc_display": 12,
  "env": {
    "VM_RESOURCES": "medium",
    "QEMU_AUDIO_DRV": "none"
  },
  "vm_token": "z9x8c7"
}
```

You are provided with a small sample of test cases in `/home/user/corpora/clean/` and `/home/user/corpora/evil/` which you can use to develop and test your script. Note that an automated test suite will later run your script against a much larger, hidden evaluation corpus to verify that it perfectly discriminates between clean and evil requests.

Ensure your script is executable (`chmod +x`) and begins with an appropriate Python shebang.