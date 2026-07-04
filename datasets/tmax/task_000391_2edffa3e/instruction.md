You are a red-team operator preparing to test a series of evasion payloads against a target's proprietary Web Application Firewall (WAF). To avoid noisy, live testing that could alert the blue team, you need to build a perfect local replica of the target's WAF logic. 

We managed to exfiltrate a brief screen recording of the target's WAF configuration dashboard. The video is located at `/app/intercept_leak.mp4`.

Your task is to analyze this video, extract the specific security rules, and write a WAF simulator in Rust.

**Step 1: Video Analysis**
Use `ffmpeg` to extract and analyze the frames of `/app/intercept_leak.mp4`. The video briefly flashes three critical WAF configuration values:
1.  **Allowed Ingress Port:** The specific internal port the service expects.
2.  **Cookie Prefix Requirement:** A mandatory string prefix for the `AuthToken` cookie.
3.  **CSP Whitelist:** A specific domain allowed in the Content-Security-Policy `script-src` directive.

**Step 2: WAF Simulator Implementation**
Write a Rust program at `/home/user/waf_simulator.rs` and compile it to `/home/user/waf_simulator`. 

The program must take a single command-line argument: the path to a JSON file representing an intercepted HTTP request.
The JSON format is:
```json
{
  "target_port": 1234,
  "headers": {
    "Cookie": "AuthToken=...",
    "Content-Security-Policy": "..."
  },
  "body": "..."
}
```

Your Rust program must parse this JSON and enforce the following rules extracted from the video:
1.  **Service Auditing:** The `target_port` MUST exactly match the allowed ingress port from the video.
2.  **Cookie Inspection:** The `headers.Cookie` MUST contain an `AuthToken=<value>` where `<value>` starts with the exact prefix shown in the video.
3.  **CSP Enforcement:** If the `headers.Content-Security-Policy` contains a `script-src` directive, it MUST ONLY contain domains present in the video's CSP Whitelist (or standard keywords like `'self'`). If it contains unauthorized domains, block it. 

**Execution and Exit Codes:**
- If the JSON request violates *any* of the rules above, the WAF simulator must reject the payload by exiting with status code `1`.
- If the JSON request passes all rules, it must accept the payload by exiting with status code `0`.

Compile your Rust code to ensure it is executable at `/home/user/waf_simulator` before finishing. You can test your code by creating sample JSON files that either follow or break the rules.