You are a FinOps analyst working on an automated cloud cost optimization system. We have a C++ daemon that analyzes resource states stored in a local Git repository, but our custom bash service script keeps failing because it suffers from a missing dependency: it tries to run the analyzer before the repository backup has been restored.

Your goal is to fix the service script, compile the analyzer, set up a Git hook for continuous monitoring, and trigger an analysis.

Perform the following tasks:

1. **Compile the Analyzer:** 
   Compile the C++ source file located at `/home/user/analyzer.cpp` into an executable named `/home/user/analyzer`.

2. **Fix the Service Script (Robust Scripting & Restore):**
   The script `/home/user/start_service.sh` currently just attempts to blindly run `/home/user/analyzer`, which fails because the target directory doesn't exist yet. 
   Rewrite `/home/user/start_service.sh` to be a robust wrapper with the following logic:
   - Check if the directory `/home/user/cloud_repo` exists.
   - If it does not exist, attempt to restore the backup by extracting `/home/user/cloud_backup.tar.gz` into `/home/user/`.
   - If the extraction command fails, the script should exit immediately with exit code `2`.
   - If the extraction succeeds (or if the directory already existed), execute `/home/user/analyzer`.
   Run your fixed `/home/user/start_service.sh` to restore the repository.

3. **Configure Git Hook & Permissions:**
   We want the analyzer to run automatically whenever cloud state is updated. 
   In the restored `/home/user/cloud_repo` repository, create a `post-commit` hook. 
   The hook must:
   - Append the exact text `HOOK_FIRED` to a log file at `/home/user/hook_log.txt`.
   - Execute `/home/user/analyzer`.
   Ensure the hook has the correct file permissions so Git can execute it.

4. **Trigger the Pipeline:**
   Navigate into `/home/user/cloud_repo`. Create a new empty file named `new_resource.json`, stage it, and commit it with the message "Add new resource".
   This must trigger your hook, which will write to `/home/user/hook_log.txt` and cause the analyzer to generate the final report at `/home/user/cost_report.txt`.