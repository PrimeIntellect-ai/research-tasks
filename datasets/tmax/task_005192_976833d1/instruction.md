You are a compliance analyst responsible for securing and validating our infrastructure's privilege escalation audit trails. 

Our previous audit log validator was written in a scripting language and suffered from CWE-20 (Improper Input Validation) and CWE-798 (Hardcoded Credentials), causing it to crash on malformed logs and leak secrets. We need you to implement a robust, secure replacement in Rust that validates tokenized audit events, while dynamically deriving its secret from a physical visual log.

**Step 1: Visual Log Analysis**
We have a video recording of the compliance dashboard at `/app/audit_visual_log.mp4`. A privilege escalation event is visually indicated when the top-left pixel (x=0, y=0) flashes pure red (RGB: 255, 0, 0). 
Use `ffmpeg` or any suitable tool to analyze this video. Count the exact number of frames where this pixel is strictly `255, 0, 0`. This integer value is your `ESCALATION_SECRET`.

**Step 2: Secure Token Validator Implementation**
Create a new Rust binary project at `/home/user/audit_verifier`.
Implement the main logic in `/home/user/audit_verifier/src/main.rs`. 
The compiled binary must accept exactly one positional command-line argument: the audit log entry string.

The log entry is expected to follow this exact format:
`USER:<username>;ESCALATION:<level>;TOKEN:<token>`

Where:
- `<username>` is an alphanumeric string.
- `<level>` is an integer representing the privilege escalation tier.
- `<token>` is a 32-character hexadecimal string (lowercase).

**Validation Rules:**
1. The program must parse the string safely. It must strictly NOT panic or crash on missing fields, extra fields, invalid characters, or incorrect formatting (mitigating CWE-20).
2. If the format is correct, the program must recompute the expected token. The expected token is the MD5 hash of the concatenated string: `<username><level><ESCALATION_SECRET>`. 
   *(For example, if user is "admin", level is "2", and the secret is "15", the MD5 hash is computed over "admin215")*.
3. If the provided `<token>` exactly matches the expected MD5 hash, print `VALID` to standard output.
4. If the token does not match, or if the input string is malformed in any way, print `INVALID` to standard output.
5. The program must output exactly `VALID` or `INVALID` followed by a newline, and nothing else.

Compile your Rust program in release mode (`cargo build --release`). 

Your compiled binary will be tested against a heavily fuzzed oracle using thousands of inputs to ensure absolute equivalence and crash-resistance.