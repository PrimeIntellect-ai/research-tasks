You are a penetration tester performing an offline vulnerability analysis on a set of intercepted JWT (JSON Web Tokens) from a vulnerable web application. The application is known to suffer from an authentication bypass vulnerability where it accepts tokens with the algorithm set to "none" (`alg: "none"`). 

Your task is to write a C++ program that automates the exploit payload generation and performs sensitive data redaction on the intercepted data.

You have been provided with a file containing intercepted JWTs at `/home/user/tokens.txt`. Each line contains one complete JWT (Header.Payload.Signature) encoded in Base64Url format.

Write a C++ program at `/home/user/jwt_exploit.cpp` that does the following:
1. Reads the JWTs from `/home/user/tokens.txt`.
2. Decodes the Base64Url-encoded Header and Payload of each token. 
3. Crafts a forged JWT exploit for each token:
   - Change the algorithm in the Header to `"none"`. So the decoded header should be exactly `{"alg":"none"}`.
   - Modify the Payload to elevate privileges: change the `"role"` field from `"user"` (or whatever it is) to `"admin"`. Leave all other fields in the payload unchanged.
   - Re-encode the forged token. Since the algorithm is "none", the signature part of the forged token must be empty. The final forged token format must be `Base64Url(ForgedHeader) + "." + Base64Url(ForgedPayload) + "."`
4. Redacts sensitive data from the **original** payload: 
   - Parse the original payload. If there is a `"credit_card"` field, replace its string value entirely with `"REDACTED"`.
5. Outputs the results to a JSON file at `/home/user/pwned_tokens.json`. 

The output file `/home/user/pwned_tokens.json` must contain a strictly valid JSON array of objects, one for each token in the same order as the input file, with the following structure:
```json
[
  {
    "username": "<username extracted from original payload>",
    "forged_token": "<the crafted JWT string ending in a period>",
    "redacted_original_payload": "<the original JSON payload string with the credit card redacted>"
  }
]
```

Notes:
- You must use C++ as the primary language for this tool. You can compile it using `g++ -std=c++17 /home/user/jwt_exploit.cpp -o /home/user/jwt_exploit`.
- Standard Base64Url encoding uses `-` instead of `+` and `_` instead of `/`, and omits any trailing `=` padding characters.
- Your program should execute cleanly and create the required output file without manual intervention. Do not use external C++ libraries that are not available in standard Linux repositories (standard library headers are preferred).