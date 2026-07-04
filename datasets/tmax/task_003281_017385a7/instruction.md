You are tasked with building the core filtering component of a simulated Kubernetes Mutating Webhook operator. 

We have a policy document that was provided as a screenshot: `/app/operator_policy.png`. This image contains a specific security policy regarding SSH configurations inside Kubernetes manifests, inspired by an incident where an SSH config silently rejected key-based logins. 

Your objective is to:
1. Extract the policy logic from `/app/operator_policy.png` using any available tools (e.g., `tesseract` is installed).
2. Write a highly robust Python script at `/home/user/manifest_filter.py` that implements this exact logic.
3. The script must read a JSON-formatted Kubernetes manifest from standard input (`stdin`) and output the processed JSON manifest to standard output (`stdout`).
4. Ensure the script gracefully handles missing fields and malformed JSON, defaulting to passing the input unmodified if it doesn't match the specific conditions outlined in the policy image.

The script must be executable (`chmod +x /home/user/manifest_filter.py`) and use `#!/usr/bin/env python3`.

Your implementation will be tested against a massive array of randomly generated manifests to ensure it performs bit-for-bit identical transformations compared to our internal reference implementation.