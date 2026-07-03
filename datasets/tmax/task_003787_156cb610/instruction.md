You are a compliance analyst tasked with securing a legacy C++ audit trail generator. The existing tool reads compliance logs, verifies their integrity using a custom checksum algorithm, and generates an HTML report. Unfortunately, it suffers from a Cross-Site Scripting (XSS) vulnerability and uses a weak hash function.

Your objective is to demonstrate the vulnerability by forging a log entry, and then fix the C++ code to secure the audit pipeline.

**Initial Setup:**
You are provided with the source code of the vulnerable program at `/home/user/audit_generator.cpp` (assume you must create it based on the description below, or write a script to analyze it).
The program uses the following custom hash function to verify logs:
```cpp
uint16_t compute_hash(const std::string& data) {
    uint16_t sum = 0;
    for (char c : data) {
        sum = (sum + c) % 65535;
    }
    return sum;
}
```
The generator only accepts logs where `compute_hash(log_content) == 25000`. If accepted, it wraps the log content directly into an HTML template without any encoding, resulting in an XSS vulnerability.

**Your Tasks:**
1. **Forge an Audit Log:** 
   Write a C++ program (or bash script) to craft a file named `/home/user/forged_log.txt`. 
   The contents of this file MUST start exactly with the payload: `<script>alert('COMPROMISED')</script>`. 
   You must append uppercase 'A' characters (ASCII 65) to this payload until the `compute_hash` of the entire string equals exactly `25000`. 

2. **Fix the Vulnerability:**
   Create a fixed version of the C++ program at `/home/user/audit_generator_fixed.cpp`.
   This program should:
   - Read from a file passed as the first command-line argument.
   - Calculate the hash using the `compute_hash` logic above.
   - If the hash is not `25000`, print "Invalid checksum" and exit with code 1.
   - If the hash is `25000`, it must HTML-encode the log content (replace `<` with `&lt;` and `>` with `&gt;`) and write the result inside `<body><p>` and `</p></body>` tags to a file named `audit_report.html` in the current working directory.

3. **Execution:**
   Compile your fixed C++ program: `g++ /home/user/audit_generator_fixed.cpp -o /home/user/audit_generator_fixed`
   Run it against your forged log: `/home/user/audit_generator_fixed /home/user/forged_log.txt`

The final state must include `/home/user/forged_log.txt` with the exact correct number of 'A's to equal 25000 in the custom checksum, and the securely encoded HTML file at `/home/user/audit_report.html`.