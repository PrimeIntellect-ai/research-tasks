You are a DevSecOps engineer tasked with enforcing security policies as code for a legacy web service. We need to deploy a lightweight Web Application Firewall (WAF) filter written entirely in Bash to sanitize incoming payload strings before they reach the backend.

Your task is to write a Bash script that implements the filtering and normalization rules defined in the architecture policy diagram.

1. Inspect the WAF policy diagram located at `/app/waf_policy.png`. This image contains a text flowchart detailing the exact rules and transformations to apply.
2. Create a Bash script at `/home/user/waf.sh` that takes exactly one argument (the input payload string).
3. Implement the rules *in the exact order* they appear in the image.
4. For any rule that specifies rejecting the payload, your script must output exactly `BLOCKED` to stdout and exit with status code `1`. Note that the rejection matching must be **case-insensitive**.
5. For payloads that are not rejected, apply the specified text transformations, print the final normalized payload to stdout, and exit with status code `0`.
6. Ensure your script is executable (`chmod +x /home/user/waf.sh`).

Your script will be tested against thousands of randomly generated adversarial payloads to ensure its behavior is bit-exact equivalent to our reference implementation. Pay close attention to edge cases like empty strings, strings with special characters, and multiple consecutive spaces.