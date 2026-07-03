You are a security auditor tasked with verifying an open redirect vulnerability in a local web application's login flow. 

You have been provided with the application's source code at `/home/user/server.py` and a recent debug log file at `/home/user/logs/debug.log`. The application attempts to secure its `redirect` parameter by requiring an MD5-based signature, appending a secret key to the URL before hashing.

However, the application is vulnerable because:
1. The secret key was accidentally leaked in the debug logs.
2. The signature mechanism is simplistic and can be easily forged once the key is known.

Your task is to:
1. Analyze `/home/user/server.py` to understand the exact signature generation logic.
2. Extract the leaked secret key from `/home/user/logs/debug.log`.
3. Craft a malicious login URL that exploits the open redirect to send users to `http://attacker.com/steal`.
4. The crafted URL must be formatted exactly as `http://localhost:8080/login?redirect=<url>&sig=<signature>`.

Save the final crafted URL into a file located at `/home/user/exploit_url.txt`. Ensure the file contains only the URL string and nothing else.