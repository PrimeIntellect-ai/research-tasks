You are a DevSecOps engineer tasked with implementing a strict "Policy as Code" auditing tool. Your team is enforcing a new set of security standards that span both web infrastructure (Content Security Policy) and compiled artifacts (ELF binaries). 

To begin, you have received an audio briefing from the Chief Information Security Officer (CISO) located at `/app/policy_brief.wav`. You need to transcribe or listen to this audio file to extract the exact numerical constraints for our CSP headers (specifically the `max-age` for HSTS or CSP directives) and the specific CWE identifier that our ELF auditor must flag.

Once you have the constraints from the audio, your objective is to create a Python-based auditing script at `/home/user/policy_auditor.py`. 

This script must operate exactly as follows:
1. It takes a single command-line argument: a JSON string.
2. The JSON string contains two keys: `"csp_header"` (a string containing a web server's Content Security Policy) and `"elf_metadata"` (a string containing comma-separated ELF segment flags, e.g., "RWE, RW, R").
3. The script must parse these inputs and determine if they comply with the CISO's policy.
4. It must output exactly `1` to `stdout` if the inputs are compliant, and `0` if they contain the specific CWE vulnerability (e.g., executable stack implied by "RWE") or fail the CSP constraints mentioned in the audio. No other output should be printed.

Your script must perfectly match the behavior of our proprietary pre-compiled oracle binary. We will test your script using thousands of randomized inputs to ensure bit-exact output equivalence with our internal standards.