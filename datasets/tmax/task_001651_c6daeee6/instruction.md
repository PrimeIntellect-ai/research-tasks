You are a network security engineer investigating a custom C-based authentication tool used in your organization.

We have found the source code for the tool at `/home/user/validator.c` and the compiled binary at `/home/user/validator`. The tool takes a single JWT-like token as a command-line argument. We suspect that its custom token parsing implementation contains a critical vulnerability regarding how it handles the "alg" (algorithm) field in the token header.

Your task consists of three parts:

1. **Vulnerability Analysis & Exploit Crafting:**
   Analyze `/home/user/validator.c`. Write a C program at `/home/user/exploit.c` that, when compiled and executed, outputs a forged token to standard output. The forged token must bypass the signature verification by exploiting an `alg: none` vulnerability (or similar logic flaw in the C code) and claim the payload `{"role":"admin"}`.

2. **Payload Delivery:**
   Compile your exploit. Run the vulnerable validator using the output of your exploit and save the validator's output to `/home/user/flag.txt`.
   Example execution: `./validator $(./exploit) > /home/user/flag.txt`

3. **Pattern Matching (Intrusion Detection):**
   To prevent future exploitation over the network, we need to detect the base64url-encoded header that attempts to set the algorithm to "none". 
   Write exactly the base64url-encoded string of the minimal malicious JSON header `{"alg":"none"}` into a file named `/home/user/pattern.txt`. Do not include any padding characters (`=`) or newlines in the pattern string itself.

Ensure all requested files (`/home/user/exploit.c`, `/home/user/flag.txt`, and `/home/user/pattern.txt`) are created with the correct contents.