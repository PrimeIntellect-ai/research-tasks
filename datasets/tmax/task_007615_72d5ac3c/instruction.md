You are a network security engineer tasked with auditing and securing a Rust-based traffic inspection dashboard tool. 

You have been given access to the source code of the tool in the `/home/user/traffic_dashboard` directory. The tool reads a simulated HTTP traffic log (`/home/user/traffic_dashboard/traffic.log`), filters it based on a user-provided search term, and generates an HTML report to stdout.

Upon initial inspection, you suspect the code is vulnerable to multiple security flaws, specifically related to improper handling of the search term (Command Injection) and improper handling of extracted HTTP headers (Cross-Site Scripting). Furthermore, the generated HTML lacks proper Content Security Policy (CSP) enforcement.

Your task is to:
1. **Identify Vulnerabilities**: Audit `src/main.rs`. Create a file named `/home/user/audit_report.txt`. For each vulnerability you find, write exactly one line in this format: `CWE-XXX` (where XXX is the official CWE number for OS Command Injection and Cross-Site Scripting).
2. **Fix the Rust Code**: Modify `/home/user/traffic_dashboard/src/main.rs` to resolve the vulnerabilities:
   - Fix the command injection vulnerability by using the `std::process::Command` API safely (do not invoke a shell like `sh -c`).
   - Fix the XSS vulnerability by HTML-escaping the extracted User-Agent strings before embedding them in the HTML. Specifically, replace `<` with `&lt;`, `>` with `&gt;`, `&` with `&amp;`, `"` with `&quot;`, and `'` with `&#x27;`.
   - Enforce Content Security Policy: Add a `<meta>` tag in the `<head>` of the generated HTML report that sets the `Content-Security-Policy` to exactly `default-src 'self';`.
3. **Build and Run**: Compile the fixed code using `cargo build`. Run the binary using the search term `admin`, and redirect the stdout to `/home/user/report.html`. Example: `cargo run -- admin > /home/user/report.html`.

Ensure that:
- `/home/user/audit_report.txt` contains the correct CWE IDs.
- The compiled Rust program safely escapes malicious payloads in the `traffic.log`.
- The `report.html` file contains the required CSP meta tag and no unescaped HTML tags from the User-Agent field.