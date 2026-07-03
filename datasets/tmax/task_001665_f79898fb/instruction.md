You are an incident responder investigating a recent server breach. The attackers exploited a file upload service to read sensitive system files. 

We have recovered the stripped binary `/app/upload_handler` that processed the file uploads. We know it contains a custom path sanitization function designed to prevent path traversal (e.g., preventing access to `/etc/passwd`), but it is flawed and the attackers bypassed it.

Your objective is to:
1. Analyze the `/app/upload_handler` binary (using black-box testing, `strings`, `objdump`, or `gdb`) to understand its sanitization logic and discover how it can be bypassed.
2. Develop a bash detection script at `/home/user/detect.sh`.
3. The script must read a list of file paths from standard input (one path per line).
4. For each path, print `1` if the path successfully bypasses the binary's sanitization to achieve path traversal (i.e., it would resolve to a parent directory after the binary processes it), and `0` if the path is benign or safely blocked by the filter. Output exactly one number per line.

Ensure your script has executable permissions (`chmod +x /home/user/detect.sh`).

An automated grading system will pass a held-out dataset of 1,000 paths (a mix of benign files, blocked traversal attempts, and successful bypass payloads) to your script via standard input. Your solution will be evaluated based on its classification accuracy. You must achieve an accuracy of at least 95% to pass.