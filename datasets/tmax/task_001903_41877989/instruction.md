You are a network engineer tasked with creating a precise traffic modification proxy script. We recently intercepted some traffic and received an audio briefing about a new redaction requirement.

You have been provided with an audio file at `/app/intercepted.wav`. Listen to this briefing (you may use tools like `whisper` or write a script using available Python libraries to transcribe it) to understand the exact encryption scheme, key, and redaction rules for our system's cookies.

Your objective is to write a Python script at `/home/user/redactor.py` that processes raw HTTP requests and redacts sensitive data from the encrypted `AuthToken` cookie.

Requirements for `/home/user/redactor.py`:
1. It must read a raw HTTP request from standard input (`sys.stdin.read()`) until EOF.
2. It must inspect the HTTP headers to find the `Cookie:` header and specifically extract the `AuthToken` value (which is hex-encoded).
3. It must decrypt the `AuthToken` value using the cipher and key specified in the audio briefing.
4. It must perform the redaction exactly as specified in the audio briefing.
5. It must re-encrypt the redacted string using the same cipher and key, and hex-encode it (using UPPERCASE hex characters).
6. It must replace the original `AuthToken` value in the HTTP request with the new hex string, leaving all other headers, cookies, whitespace, line endings, and the request body EXACTLY as they were.
7. It must print the fully modified raw HTTP request to standard output.

To help you test, we have provided a reference binary at `/app/oracle_redactor`. Your Python script's output must be bit-exact equivalent to the output of `/app/oracle_redactor` for any given valid input. 

Write your script carefully, ensuring edge cases like varying line endings (`\r\n`) and other cookies in the header are preserved perfectly.