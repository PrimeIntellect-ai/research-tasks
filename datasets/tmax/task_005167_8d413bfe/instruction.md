You are an integration developer tasked with testing a custom authentication API. Recently, the API token specifications were updated to enhance web security, making the previous token generation script obsolete. 

You have an outdated Python script at `/home/user/auth_generator.py` that generates tokens using an old checksum algorithm and standard Base64 encoding.

You also have a patch file at `/home/user/api_update.patch` which contains a diff of the reference implementation showing the new security rules (which involve custom numerical hashing and specific character encoding constraints). However, due to diverging codebases, this patch cannot be directly applied to your `auth_generator.py` script cleanly (similar to a peer dependency conflict).

Your tasks:
1. Analyze `/home/user/api_update.patch` to understand the updated numerical algorithm for the checksum, and the strict character encoding rules (URL-safe, no padding, compact JSON).
2. Manually fix and update `/home/user/auth_generator.py` to correctly implement these new rules. 
3. Use your updated script to generate an authentication token for the following payload:
   - user: `integration_tester`
   - role: `admin`
   - exp: `1735689600`
4. Save the exact generated token string (with no extra whitespace or newlines) to `/home/user/final_token.txt`.

The final state will be verified by checking the contents of `/home/user/final_token.txt`.