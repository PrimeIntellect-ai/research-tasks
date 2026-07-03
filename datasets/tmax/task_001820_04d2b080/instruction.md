You are a penetration tester reviewing a custom web authentication mechanism. You have intercepted an older version of the session token generation binary used by the server, located at `/app/token_legacy`. 

The developers recently updated the authentication scheme to "V2". They left a screenshot of the new design notes on the server at `/app/update_notes.png`. 

Your task is to analyze the legacy binary to understand the base token generation algorithm, read the image to identify the changes made in V2, and write a standalone C program that perfectly replicates the new V2 token generation mechanism.

Requirements:
1. Write your C source code to `/home/user/token_v2.c`.
2. Compile it to `/home/user/token_v2`.
3. Your compiled binary must take exactly one command-line argument (the input payload string) and print the final generated V2 token to standard output (with a trailing newline).
4. Do not use external libraries other than standard C library functions (you can implement base64 or other encodings yourself if needed).
5. The output of your program must perfectly match the behavior of the new server-side implementation.