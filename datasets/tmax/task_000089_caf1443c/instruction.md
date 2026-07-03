You are a forensics analyst investigating a compromised Linux host. The attacker utilized an authentication bypass vulnerability (CWE-287) in a custom token service by enforcing an `alg: none` header, allowing them to forge tokens. We have recovered fragments of their privilege escalation tool. 

Your task is to reconstruct the attacker's payload decoder and brute-force tool in C.

**Step 1: Fix the Vendored Dependency**
The attacker used `cJSON` for parsing. We have recovered the source tree at `/app/cJSON-1.7.15`, but the attacker intentionally sabotaged it to hinder analysis. 
1. Navigate to `/app/cJSON-1.7.15`.
2. Identify and fix the deliberate compilation error (a misspelled standard library header inclusion in `cJSON.c`).
3. Compile it to produce the static library `libcjson.a` (using `make` or `gcc` directly).

**Step 2: Write the Decoder & Cracker**
Write a C program at `/home/user/analyzer.c` and compile it to `/home/user/analyzer`. Ensure it statically links the repaired `libcjson.a`.

The program must read exactly one line from `stdin` containing an attacker token in the following format:
`<HeaderJSON>|<PayloadJSON>`

Your program must implement the following logic strictly:
1. Split the input into the Header JSON string and the Payload JSON string at the first `|` character. If no `|` is present, print `ERR: FORMAT` to `stdout` and exit with code `1`.
2. Parse the Header JSON. If it does not contain the key `"alg"` with the exact string value `"none"`, print `ERR: INVALID_ALG` to `stdout` and exit with code `1`.
3. Parse the Payload JSON. It must contain `"user"` (a string) and `"pin_hash"` (an integer). If either is missing, print `ERR: MALFORMED_PAYLOAD` to `stdout` and exit with code `2`.
4. **Password Cracking:** The attacker protected the original 4-digit PIN (from `0000` to `9999`) using a simple XOR. You must brute-force the PIN (as an integer `p` from 0 to 9999). The correct PIN satisfies: `(p ^ 0x5A5A) == pin_hash`.
5. If a matching PIN is found, print `RECOVERED user=<user> pin=<4-digit zero-padded pin>` (e.g., `RECOVERED user=root pin=0042`) to `stdout` and exit with code `0`. 

There is a reference oracle binary compiled by the attacker at `/app/oracle`. Your `/home/user/analyzer` binary must be bit-exact equivalent in behavior (stdout, exit codes) for all possible inputs compared to this oracle.