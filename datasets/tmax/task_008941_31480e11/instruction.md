You are a compliance analyst generating an audit trail for a recent SSH server access review. 

You have been provided with the following files in `/home/user/`:
1. `/home/user/auth_events.log`: Contains simulated SSH login events, including the public key fingerprints used for authentication.
2. `/home/user/pubkeys/`: A directory containing the authorized SSH public keys for various users (e.g., `alice.pub`, `bob.pub`).
3. `/home/user/tokens.txt`: A file containing session tokens for the users in the format `username:timestamp:checksum`.

Your task is to generate a compliance audit report by completing the following steps:

1. **Log Parsing & Correlation**: Extract the fingerprints of the keys used for successful logins ("Accepted publickey") from `/home/user/auth_events.log`. Match each fingerprint to a user by inspecting the public keys in `/home/user/pubkeys/` (hint: use `ssh-keygen -l`).
2. **Token Validation**: Write a C program at `/home/user/validate.c` and compile it to `/home/user/validate`. The program should take two command-line arguments: a `<username>` and a `<timestamp>`, and an `<expected_checksum>`. 
   The validation rule is: The token is valid if the sum of the ASCII values of all characters in the `username` and `timestamp` strings, modulo 256, equals the `expected_checksum`.
   (e.g., if username is "abc" and timestamp is "123", the sum is 97+98+99+49+50+51 = 444. 444 % 256 = 188. If expected_checksum is 188, it is valid).
3. **Audit Trail Generation**: Use shell commands and your compiled C program to process the logged-in users and their tokens from `/home/user/tokens.txt`. Generate a final audit report at `/home/user/compliance_audit.csv`.

The output file `/home/user/compliance_audit.csv` must contain exactly one line for every successful login found in `auth_events.log`, in the exact order they appear, with the following comma-separated format:
`Username,Fingerprint,TokenValid`

Where `TokenValid` is either `Yes` or `No`.

For example:
```
alice,SHA256:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx,Yes
bob,SHA256:yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy,No
```

Do not include a header row in the CSV.