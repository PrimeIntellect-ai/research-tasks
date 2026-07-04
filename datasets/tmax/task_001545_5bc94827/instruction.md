You are a monitoring specialist tasked with setting up a local Git server that automatically intercepts and alerts on developers accidentally pushing private keys. Like a misconfigured SSH server that silently rejects key-based logins, we want to actively reject problematic commits before they hit the codebase, using a centralized hook structure.

Please perform the following steps on this system:

1. **Repository & Directory Setup:**
   - Initialize a bare Git repository at `/home/user/alert_repo.git`.
   - Create a directory called `/home/user/global_git_hooks`.
   - Replace the default `hooks` directory inside `/home/user/alert_repo.git` with a symbolic link pointing to `/home/user/global_git_hooks`.

2. **System Config Management:**
   - Modify the Git configuration for the `/home/user/alert_repo.git` repository to set `receive.denyDeletes` to `true`.

3. **Multi-Language Alert Hooks:**
   - Inside `/home/user/global_git_hooks`, create an executable bash script named `pre-receive`.
   - Also inside `/home/user/global_git_hooks`, create a Python script named `secret_scanner.py`.
   - The `pre-receive` hook must read the standard input provided by Git (lines containing `<oldrev> <newrev> <refname>`).
   - For each ref updated, the hook should generate the patch diff of the incoming changes (you can assume we are only updating existing branches, so you can use `git log -p <oldrev>..<newrev>`).
   - The bash script must pipe this diff to your `secret_scanner.py` script.
   - The Python script must scan the diff. If any newly added line (a line starting with exactly one `+`, excluding `+++` headers) contains the exact string `CRITICAL_PRIVATE_KEY_123`, the Python script should exit with a non-zero exit code.
   - If the Python script exits with a non-zero code, the `pre-receive` hook must:
     a) Append exactly this line to `/home/user/rejected_pushes.log`:
        `ALERT: Push rejected due to secret key in ref <refname>`
        *(Replace `<refname>` with the actual ref name, e.g., `refs/heads/master`)*
     b) Exit with a non-zero status to reject the push.
   - If no secrets are found, the push should be accepted.

Make sure your hook is fully executable and handles standard `pre-receive` input properly. Do not hardcode the repository paths inside the hook, as Git will execute the hook from within the bare repository.