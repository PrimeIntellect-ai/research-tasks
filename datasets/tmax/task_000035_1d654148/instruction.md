You are a platform engineer maintaining a CI/CD pipeline that compiles and deploys a multi-file Rust project. Recently, we discovered that attackers are trying to exploit our internal webhook REST API (which triggers the build system) by injecting malicious parameters, exploiting character encoding bypasses, and sending unauthorized deployment requests.

Your task is to build a Bash-based reverse proxy webhook filter that sanitizes and validates incoming JSON payloads. 

First, we have rotated the deployment authorization token. The new token was sent via a voice memo. 
1. Transcribe the audio file located at `/app/authorization_memo.wav` to discover the new token. The token is a single continuous string mentioned at the end of the recording.

Second, write a Bash script at `/home/user/filter.sh` that takes a single argument: the path to a JSON webhook payload file.
The script must act as a strict validator for the webhook payload. 
The JSON payload has the following structure:
```json
{
  "action": "trigger_build",
  "auth_token": "TOKEN_STRING",
  "branch": "BRANCH_NAME",
  "build_env": {
     "RUSTFLAGS": "...",
     "CARGO_PROFILE": "..."
  }
}
```

Your `/home/user/filter.sh` script MUST implement the following rules:
1. Parse the JSON (you may use `jq`).
2. Validate that `auth_token` matches EXACTLY the token extracted from the audio file.
3. Validate the `branch` field. To prevent directory traversal and encoding attacks, the `branch` must ONLY contain alphanumeric characters, hyphens (`-`), and underscores (`_`). If it contains URL-encoded characters (like `%2e`), slashes, or anything else, reject it.
4. Validate the values within the `build_env` object. To prevent shell injection during the Rust compilation step, NO value in the `build_env` object may contain the characters `$`, `;`, `|`, `&`, `<`, `>`, or backticks.

If the payload violates ANY of these rules, your script must exit with a non-zero status code (e.g., `exit 1`).
If the payload is completely valid and safe, your script must exit with status code `0`.

To help you test your filter, we have provided two directories containing sample webhook payloads:
- `/app/corpus/clean/`: Contains 20 perfectly valid webhook payloads that your script MUST accept (exit 0).
- `/app/corpus/evil/`: Contains 20 malicious or invalid webhook payloads that your script MUST reject (exit > 0).

Your goal is to achieve 100% accuracy: preserve (exit 0) all clean payloads, and reject (exit >0) all evil payloads.

Ensure your script is executable (`chmod +x /home/user/filter.sh`).