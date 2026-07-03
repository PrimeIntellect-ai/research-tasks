You are a security auditor tasked with building a strict command-line filter to prevent privilege escalation and enforce process isolation on a restricted Linux sandbox.

We have a set of user-submitted command logs. You must write a Python script that acts as an intrusion detection pattern matcher. Your script will evaluate if a given command violates our strict security boundary.

You have been provided with two directories to help train and test your filter:
- `/home/user/corpora/clean/`: Contains files, each with a single safe command. Your filter MUST accept all of these.
- `/home/user/corpora/evil/`: Contains files, each with a command attempting privilege escalation, sandbox escape, or unauthorized access. Your filter MUST reject all of these.

Additionally, our strict institutional policies are not fully documented in text. An old scan of the security mandate is located at `/app/policy_scanned.png`. You must extract the text from this image (e.g., using `tesseract`) to discover the *secret forbidden keywords and directories* that must also be explicitly blocked by your filter. 

**Requirements:**
1. Create a Python script at `/home/user/audit_filter.py`.
2. The script must take exactly one argument: the path to a file containing a command.
3. The script must read the file and evaluate the command against standard privilege escalation vectors (e.g., `sudo`, `su`, `chmod +s`, accessing shadow/passwd, etc.) AND the specific secret rules extracted from the scanned policy image.
4. The script must output EXACTLY the string `SAFE` to standard output if the command is allowed, or `VIOLATION` if it breaks any rule or attempts privilege escalation. No other text should be printed.
5. Your script must achieve a 100% pass rate on both the `clean` and `evil` corpora. 

Ensure your pattern matching is robust enough to handle the specific adversarial examples in the evil corpus without inadvertently flagging the clean corpus.