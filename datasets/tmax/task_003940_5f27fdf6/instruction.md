You are a deployment engineer rolling out updates for our email infrastructure's load balancing layer. Currently, our reverse proxy uses a legacy, proprietary compiled binary to route incoming email addresses to specific backend server IDs. 

We are migrating our configuration management and service lifecycle to a pure Python stack. Your task is to reverse-engineer the routing logic from the legacy binary and write a functionally equivalent Python script.

Here are the details:
1. The legacy binary is located at `/app/email_router_bin`. It is a stripped ELF executable.
2. It takes exactly one command-line argument: a string representing an email address (e.g., `admin@example.com`).
3. It prints a single integer to standard output (the backend server ID, which is always between 0 and 9), followed by a newline.
4. You must analyze this binary to figure out the exact mathematical hashing algorithm it uses to assign an email to a backend.
5. Create a Python script at `/home/user/router.py`.
6. Your script must take the email address as its first command-line argument (`sys.argv[1]`) and print the exact same backend ID as the legacy binary for any given input string.

The automated system will test your script by passing thousands of randomly generated email addresses to both `/app/email_router_bin` and `python3 /home/user/router.py` to ensure their standard outputs match exactly bit-for-bit.