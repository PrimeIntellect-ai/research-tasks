You are managing a user account generation system that acts as a localized CI/CD pipeline for account onboarding. The pipeline relies on a custom Python-based process supervisor to manage the background jobs. However, the pipeline is currently failing due to race conditions and a lack of fault tolerance.

The system is located in `/home/user/account_system/`.

There are two worker scripts:
1. `/home/user/account_system/db_init.py` - Initializes the temporary database schema.
2. `/home/user/account_system/profile_gen.py` - Generates user profiles based on the database.

Currently, the custom supervisor script at `/home/user/account_system/supervisor.py` launches both scripts simultaneously. `profile_gen.py` instantly fails because it tries to access the database before `db_init.py` has finished setting it up (conceptually similar to a missing `After=` dependency in systemd). Additionally, `profile_gen.py` is known to be flaky and sometimes crashes on its first run due to temporary network simulation errors.

Your task is to fix the pipeline by completing the following steps:

1. **Process Supervision & Dependency (Python):** 
   Modify `/home/user/account_system/supervisor.py` so that it starts `profile_gen.py` **only after** `db_init.py` has completed successfully (exit code 0). 

2. **Restart Policy (Python):**
   Update `/home/user/account_system/supervisor.py` to implement a robust restart policy for `profile_gen.py`. If `profile_gen.py` fails (exits with a non-zero exit code), the supervisor must restart it. It should attempt a maximum of 3 restarts (i.e., up to 4 total attempts). If it still fails after the maximum attempts, the supervisor itself should exit with code 1.

3. **CI/CD Pipeline Construction & Permissions (Bash):**
   Create a shell script at `/home/user/account_system/ci_run.sh` that orchestrates the final pipeline. This script must:
   - Run the updated `supervisor.py` (using `python3`).
   - If the supervisor succeeds, secure the generated user profiles located in `/home/user/account_system/profiles/`. Set the permissions of all *files* inside this directory to exactly `0640` and all *directories* to exactly `0750`.
   - Package the `profiles/` directory into a tarball named `/home/user/account_system/release.tar.gz`.
   - Write a summary log to `/home/user/account_system/ci_status.log` containing exactly the word `SUCCESS` if everything worked, or `FAILURE` if any step failed.

Ensure that `/home/user/account_system/ci_run.sh` has executable permissions.