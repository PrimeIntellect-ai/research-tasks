You are an infrastructure engineer automating the provisioning of a local user-level mailing list pipeline. 

We are required to use a proprietary, closed-source mailing list routing engine located at `/app/legacy_mailer`. This is a stripped C binary. It processes raw RFC 5322 email files passed via command-line argument (e.g., `/app/legacy_mailer email.eml`).

However, `legacy_mailer` is highly unstable. It is known to crash (segfault/abort) or hang infinitely on certain poorly formatted or malicious emails. Since it runs as part of our automated infrastructure, these failures disrupt the entire pipeline.

Your objective is to build a robust C-based pre-processor and wrap the pipeline in a systemd service.

**Step 1: Analyze the Legacy Binary**
You have been provided a set of sample emails in `/home/user/training_corpus/clean/` and `/home/user/training_corpus/evil/`. 
Analyze `/app/legacy_mailer` (using tools like `objdump`, `strings`, `gdb`, or simply by feeding it inputs) to deduce the exact rules that cause it to fail. 
Additionally, the pipeline policy dictates that the `To:` header must ONLY contain usernames that exist in the local `/etc/passwd` file.

**Step 2: Write the Filter in C**
Write a C program at `/home/user/filter.c` and compile it to `/home/user/filter`.
- The program must accept exactly one argument: the file path to an email.
- It must read and analyze the email.
- If the email is perfectly safe for `legacy_mailer` AND adheres to the `To:` local user policy, it must exit with status `0`.
- If the email will crash/hang the legacy binary, or violates the `To:` policy, it must exit with status `1`.

**Step 3: Provision the Service**
Create the following directory structure:
- `/home/user/spool/incoming/`
- `/home/user/spool/processed/`
- `/home/user/spool/quarantine/`

Write a shell script at `/home/user/daemon.sh` (ensure it is executable) that:
1. Continuously watches `/home/user/spool/incoming/` for new files.
2. For each file, runs `/home/user/filter <file>`.
3. If the filter returns `0`, it runs `/app/legacy_mailer <file>` and moves the file to `processed/`.
4. If the filter returns `1`, it moves the file directly to `quarantine/` without invoking the legacy binary.

Configure a systemd user service named `mailer-daemon.service` (placed in `/home/user/.config/systemd/user/`) that executes `/home/user/daemon.sh`. Enable and start this service using `systemctl --user`.

**Verification:**
An automated test will run your compiled `/home/user/filter` against a secret evaluation corpus of hundreds of emails to ensure it flawlessly distinguishes safe emails from those that exploit the legacy binary or violate policy.