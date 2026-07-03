You are a Linux systems engineer responsible for hardening the configuration pipeline of a fleet of edge devices. The devices receive their configuration updates via a local Git-based deployment system. Recently, an incident occurred where services were improperly exposed because a developer pushed a configuration with an incorrect network mode.

Your task is to build a local Git-based CI/CD validation pipeline that strictly prevents insecure configurations from being pushed to the repository.

You must implement the following:

1. **Git Repository Setup:**
   Create a bare Git repository at exactly `/home/user/config-repo.git`.

2. **Configuration Validator (C Program):**
   Write a C program at `/home/user/sec-validator.c` and compile it to `/home/user/sec-validator`.
   This program must:
   - Accept exactly one command-line argument: the path to a configuration file.
   - Read the file line by line.
   - Return an exit code of `0` (Success) ONLY IF:
     a) It contains at least one line that exactly matches `NETWORK_MODE=isolated` (ignoring trailing newlines).
     b) It DOES NOT contain any line that exactly matches `ROOT_LOGIN=true`.
   - If either condition fails, or if the file cannot be opened, the program must return an exit code of `1` (Failure).

3. **Git Pre-Receive Hook:**
   Create an executable bash script at `/home/user/config-repo.git/hooks/pre-receive`.
   This hook will automatically run when a user attempts to push code to the repository.
   The hook must:
   - Read from standard input to receive the `oldrev`, `newrev`, and `refname` (standard git pre-receive format).
   - Use text processing tools (`git diff-tree`, `awk`, `grep`, etc.) to identify all files ending with `.conf` that are being added or modified in the incoming push.
   - For each `.conf` file identified, extract its incoming content (from the new commit, not the working tree, since this is a bare repo) into a temporary file.
   - Run your compiled `/home/user/sec-validator` against this temporary file.
   - If `/home/user/sec-validator` returns `1` for *any* `.conf` file, the hook must print "Validation failed" to standard error and immediately exit with status `1`, thereby rejecting the entire push.
   - If all modified/added `.conf` files pass validation (or if no `.conf` files were modified), the hook should exit with status `0`, allowing the push.

You can test your setup by cloning the bare repository locally to another folder, adding valid and invalid `.conf` files, and attempting to push them back to `/home/user/config-repo.git`.

Ensure all file paths match exactly as requested, and that the hook has the appropriate execution permissions.