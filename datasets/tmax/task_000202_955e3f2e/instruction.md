You are an incident responder investigating a security issue on a Linux server. 

A background process called `audit_daemon` is currently running on the system. It was started with a highly sensitive authentication token passed as its first command-line argument. This is a severe security vulnerability because command-line arguments are visible to other users via the `/proc` filesystem.

Your task has two parts:

1. **Investigate and Extract:**
   Find the running `audit_daemon` process, extract the sensitive token it was started with from its command-line arguments, and save exactly this token (without any extra whitespace or newlines) to `/home/user/leaked_secret.txt`.

2. **Remediate the Code:**
   The source code for the daemon is located at `/home/user/src/audit_daemon.c`. 
   Modify this C code to perform **sensitive data redaction**. Immediately at the beginning of the `main` function, you must overwrite every character of the string passed in `argv[1]` with the asterisk character (`*`). 
   *Note: Do not change the length of the string, just replace the existing characters in-place.*
   
   Once modified, compile the fixed C code using `gcc` and output the compiled binary to `/home/user/fixed_daemon`.

Ensure your compiled binary works correctly and successfully redacts its command-line arguments when inspected via `/proc`.