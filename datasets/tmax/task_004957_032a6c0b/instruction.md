You are a FinOps analyst tasked with optimizing our cloud cost alerting system. Currently, our internal mailing list is being flooded with false-positive billing alerts and spam, causing automated scale-down scripts to fire incorrectly. 

To fix this, you need to implement a user-space email filter and a port-forwarding automation script.

Here are your requirements:

1. **Extract Policy from Image:**
   Read the corporate FinOps alerting policy from the image located at `/app/finops_policy.png`. You may use `tesseract` to read the text. This policy dictates exactly which emails are considered valid ("clean") and which should be rejected ("evil"). 

2. **Develop the C Email Filter:**
   Write a C program at `/home/user/mail_filter.c` and compile it to `/home/user/mail_filter`. 
   - The program must read a raw email message from standard input (stdin).
   - It must analyze the headers and body against the policy extracted from the image.
   - It must exit with status `0` if the email is VALID (clean).
   - It must exit with status `1` if the email is INVALID (evil).
   
   To help you develop this, we have provided two sets of sample emails:
   - `/app/corpus/clean/`: Contains 50 valid alert emails.
   - `/app/corpus/evil/`: Contains 50 invalid/spam/noisy alert emails.
   Your filter must perfectly accept all clean emails and reject all evil emails.

3. **Automation and Port Forwarding Script:**
   Write a bash script at `/home/user/start_forwarder.sh` that automates this workflow without requiring root privileges. 
   - The script must listen on local TCP port `10025` for incoming raw text (simulating an incoming email).
   - Upon connection, it should pipe the incoming data to your `/home/user/mail_filter` binary.
   - If the filter accepts the email (exit code 0), the script must automatically forward the *exact same raw email data* to local TCP port `10026` (where our actual mailing list daemon is listening).
   - If the filter rejects the email (exit code 1), the connection should be dropped and nothing forwarded.
   - The script should run continuously in the background (you can use tools like `socat` or `nc` in a loop).

Ensure your C code is robust and compiles without warnings.