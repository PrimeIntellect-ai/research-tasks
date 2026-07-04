You are acting as a security auditor tasked with processing authentication logs to identify vulnerabilities in a web application's token generation.

The application uses JSON Web Tokens (JWTs) for session management, but we suspect many of these tokens were signed using insecure, easily guessable symmetric keys (CWE-321: Use of Hard-coded Cryptographic Key). 

You have been provided with:
1. A JSON file containing 10,000 intercepted authentication records, each including a JWT: `/home/user/logs/jwt_audit.json`
2. A dictionary of known weak secrets commonly found in poorly configured environments: `/home/user/wordlists/weak_secrets.txt`

To perform this audit, you must use the `PyJWT` library. Due to strict offline air-gapped requirements, we have provided the source code for `PyJWT` (version 2.8.0) locally at `/app/PyJWT`.

However, the previous auditor mentioned they couldn't install it because of an environment constraint error during setup. 

Your task:
1. Identify and fix the perturbation in the vendored `/app/PyJWT` source code so it can be installed locally (e.g., using `pip install /app/PyJWT`).
2. Write a Python script to audit all 10,000 JWTs. For each token, attempt to verify its signature against every secret in the provided wordlist.
3. Keep track of any token that successfully decodes (verifies) using a weak secret.
4. Output your findings to a CSV file at `/home/user/cracked_jwts.csv` with exactly two columns: `id` and `secret`. The `id` is the `kid` (Key ID) found in the header of the JWT or the `id` field from the JSON wrapper, and `secret` is the matching weak key.

Ensure your script is efficient (data processing techniques like multiprocessing or batching are highly recommended, as brute-forcing thousands of tokens can be computationally heavy). Your final output will be automatically graded based on the F1-score of the vulnerable tokens you correctly identify.