You are a developer inheriting an unfamiliar, legacy Python codebase at `/home/user/auth_processor`. The service recently crashed during execution and left behind a raw memory dump file located at `/home/user/core.dmp`. 

The system was processing a highly sensitive authorization token right before it crashed. We need to recover this exact plaintext token.

From preliminary notes left by the previous developer, we know:
1. The application reads an authorization token, appends a system "salt", applies a specific string transformation, and then encodes the result.
2. The exact transformation logic is located in the codebase.
3. The hardcoded salt was recently removed from the repository for security reasons and replaced with an environment variable. However, the system crashed while running the older version of the code where the hardcoded salt was still in effect.
4. The transformed, encoded string of the last processed token is resident somewhere in the memory dump, prefixed by the exact string `PROCESSED_DATA:`.

Your objective:
1. Perform Git history forensics on the repository at `/home/user/auth_processor` to recover the original hardcoded salt.
2. Analyze the memory dump at `/home/user/core.dmp` to extract the encoded data payload.
3. Read and understand the data transformation pipeline in the codebase to figure out how to reverse the process.
4. De-obfuscate the extracted payload using the recovered salt to reveal the original plaintext token.

Once you have recovered the information, create a file at `/home/user/forensics_report.txt` containing exactly two lines in the following format:

SALT: <recovered_salt>
TOKEN: <recovered_plaintext_token>

Ensure there is no extra whitespace or additional text in the report file.