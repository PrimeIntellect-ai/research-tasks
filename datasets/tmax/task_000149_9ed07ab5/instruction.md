You are a DevSecOps engineer responsible for enforcing policy-as-code for our new sandboxed microservice architecture. Unfortunately, the exact configuration of our custom token validation and sandboxing policy was lost during a recent migration. All we have left is an incident response audit video (`/app/auth_policy_audit.mp4`) that recorded the terminal session where the policy was originally defined.

Your task is to:
1. Extract the missing authentication policy parameters from the video file located at `/app/auth_policy_audit.mp4`. The video contains a sequence of frames showing a hex-encoded configuration block that defines the allowed certificate issuers, the required token claim structures, and the specific restricted file paths for the sandbox.
2. Based on the extracted policy, write a Go program located at `/home/user/policy_evaluator.go`. This program must implement the token and certificate chain validation logic, as well as the file permission sandbox checks.
3. Compile your program to `/home/user/policy_evaluator`.

Your Go program must accept exactly two arguments:
`./policy_evaluator <token_string> <requested_file_path>`

The program must parse the token (a custom base64-encoded JSON format containing a signature, a certificate chain, and file access claims), validate the signature and certificate chain against the policy extracted from the video, and check if the requested file path is safely within the isolated sandbox boundaries defined in the policy (preventing path traversal).

If the token is fully valid, the certificate chain is trusted, and the file path is permitted, the program must print `ALLOW` to standard output and exit with code 0. If any validation fails, it must print `DENY` and exit with code 1.

Ensure your implementation is highly robust, as it will be strictly tested against thousands of randomized, adversarial inputs to ensure complete equivalence with our internal security standard.