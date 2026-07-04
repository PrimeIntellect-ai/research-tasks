You are acting as a security engineer analyzing intercepted HTTP requests for a web application. The application uses a custom encrypted session cookie.

We have provided a vendored package for handling these custom cookies located at `/app/crypt_auth_lib-2.1`. However, a junior developer recently made a mistake in the package, and it currently crashes during decryption. 

Your objectives are:
1. Identify and fix the bug in `/app/crypt_auth_lib-2.1`. The package uses AES-CBC, but something is wrong with how it extracts the Initialization Vector (IV) from the ciphertext.
2. Install the fixed package into your environment.
3. Write a Python detector script at `/home/user/detector.py` that analyzes HTTP request files.

The script `/home/user/detector.py` must:
- Accept a single command-line argument: the path to an HTTP request log file (e.g., `python3 /home/user/detector.py /path/to/request.req`).
- Read the file, which contains raw HTTP headers (one per line, `Key: Value` format).
- Extract the `Session-Token` cookie from the `Cookie` header.
- Decrypt the `Session-Token` using the fixed `crypt_auth_lib` package. The decryption key to use is `SuperSecretKey123!`. The decrypted value is a JSON string.
- Inspect the decrypted JSON cookie values AND all HTTP header values for Injection and XSS vulnerabilities. Specifically, flag the request as malicious if any of the following substrings (case-insensitive) are found anywhere in the header values or the decrypted JSON values:
  - `<script>`
  - `javascript:`
  - `onload=`
  - `' or 1=1`
  - `union select`
  - `../`
- Print exactly the word `EVIL` to standard output if any malicious payloads are detected.
- Print exactly the word `CLEAN` to standard output if the request is benign.

You must ensure your detector correctly classifies all files in the provided corpora:
- Malicious requests are located in `/app/corpus/evil/`
- Benign requests are located in `/app/corpus/clean/`

Ensure your script handles standard errors gracefully and strictly adheres to the output format.