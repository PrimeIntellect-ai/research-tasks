You are acting as a compliance analyst tasked with generating secure audit trails for user-provided SSH public keys. We need to build a robust filtering mechanism to prevent malicious or non-compliant keys from entering our infrastructure.

Attackers often use weak keys, incorrect file permissions, or hide encoded malicious payloads in the SSH key comment fields. We have a legacy stripped binary, `/app/decoder`, which was previously used to decode the proprietary encoding scheme used by our adversaries in the comment fields.

Your task is to write a Go program at `/home/user/audit_filter.go` and compile it to `/home/user/audit_filter`. This executable will act as a strict classifier for SSH public keys.

The executable must take exactly one argument: the absolute path to an SSH public key file.
It must exit with status `0` if the key is "clean" (compliant and safe), and exit with status `1` if it is "evil" (non-compliant or malicious).

Your Go program must enforce the following rules:
1. **File Permission & Access Control**: The file must have exactly `0600` or `0400` permissions. Any broader permissions (e.g., `0644`) must result in rejection.
2. **SSH Hardening**: The file must contain a valid SSH public key. You must parse it. Reject the key if it is a deprecated DSA key (`ssh-dss`) or an RSA key with a length of less than 2048 bits. Ed25519 and ECDSA keys are acceptable.
3. **Payload Decoding**: Extract the comment field from the SSH public key. Use the provided black-box binary `/app/decoder` to decode the comment. Pass the comment string as the first command-line argument to `/app/decoder`. 
4. **Malicious Payload Detection**: Read the standard output of `/app/decoder`. If the decoded output contains the exact substring `EVIL`, the key must be rejected.

If the file passes all checks, your program should exit with `0`. If it fails any check, it should exit with `1`.

We have provided a set of test files in `/app/corpus/`. You can use them to test your binary, but your final solution must be compiled and located at `/home/user/audit_filter`.