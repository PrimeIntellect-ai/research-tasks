You are a backup operator tasked with testing an automated restore pipeline. 

We have a legacy interactive restore tool located at `/home/user/legacy_restore`. It cannot take command-line arguments for its inputs. When run, it prompts:
1. `Enter restore password: ` (The password is `backup2023`)
2. `Enter staging directory: ` (You should provide `/home/user/staging`)

After providing these, it will simulate a restore and place a file named `restored_data.txt` into the staging directory.

Your task is to fully automate this staged restore and deployment process using Expect and Rust:

1. Create an Expect script at `/home/user/auto_restore.exp` that automates the interaction with `/home/user/legacy_restore`. It should spawn the tool, wait for the exact prompts, send the correct responses, and wait for the process to exit cleanly.
2. Write a Rust program at `/home/user/deploy_restore.rs` and compile it to `/home/user/deploy_restore` (using `rustc`).
3. The Rust program must:
   - Spawn a child process to run `/usr/bin/expect /home/user/auto_restore.exp`.
   - Monitor and wait for the child process to complete successfully.
   - Once the expect script finishes successfully, act as a staged deployment step: read the contents of `/home/user/staging/restored_data.txt`, and copy the file to `/home/user/prod/restored_data.txt`.
4. Run your compiled Rust program to complete the restore.

Constraints:
- Do not modify `/home/user/legacy_restore`.
- Make sure the target directories exist before running your tools (`/home/user/staging` and `/home/user/prod`).
- Ensure your Expect script properly waits for EOF.