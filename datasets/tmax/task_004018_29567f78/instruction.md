You are an integration developer responsible for testing and deploying a legacy API routing system. We are migrating our API schemas to a new format, and we need a reliable way to validate incoming payloads before they hit the upstream services. 

You have two main objectives:

1. **Fix the Vendored Router Package:**
We use a third-party pure-bash API router called `bash-router`. Its source code is vendored at `/app/vendor/bash-router-1.2.0/`. However, the current vendored version has a bug preventing it from starting up properly in our unprivileged environment. Whenever we run `/app/vendor/bash-router-1.2.0/router.sh --health-check`, it crashes complaining about a missing config directory. You need to fix the `router.sh` script so that it respects the `ROUTER_CONFIG_PATH` environment variable if set, rather than forcing a hardcoded system path. Verify your fix by ensuring `ROUTER_CONFIG_PATH=/tmp/rconf /app/vendor/bash-router-1.2.0/router.sh --health-check` returns exit code 0.

2. **Implement the Payload Validator:**
We need an API payload validator script written entirely in Bash (using standard coreutils, `jq`, `grep`, `awk`, etc.). Create this script at `/home/user/api_validator.sh` and make it executable. 

The script must act as an interpreter for a custom constraint schema to evaluate incoming JSON payloads. It should take a single argument: the path to a JSON file.
Invocation: `/home/user/api_validator.sh <path_to_json>`

The script must enforce the following strict constraints (simulating our v2 schema migration):
- The JSON must contain a root key `"api_version"` which must be an integer strictly greater than 1.
- The JSON must contain a root key `"request_type"` which must be exactly the string `"mutation"` or `"query"`.
- The JSON must contain a root key `"payload"`.
- If `"request_type"` is `"mutation"`, the `"payload"` object MUST contain a key `"user_id"` (which must be a non-empty string starting with `"USR-"`) and a key `"action_code"` (which must be an integer between 100 and 199 inclusive).
- If `"request_type"` is `"query"`, the `"payload"` object MUST contain a key `"search_term"` (string, maximum length 20 characters).

Your script must exit with code `0` if the JSON file strictly satisfies all these constraints, and exit with code `1` if it violates any of them or if the JSON is malformed.

To help you develop and test your script, we have provided two directories containing sample JSON payloads:
- `/home/user/corpora/clean/`: Contains 5 valid JSON payloads.
- `/home/user/corpora/evil/`: Contains 15 invalid, malicious, or poorly formatted payloads designed to bypass simple regex checks.

Your `api_validator.sh` must successfully accept ALL files in the clean corpus and reject ALL files in the evil corpus. You can use these directories to iteratively refine your validator.