You are a developer tasked with debugging a failing build process. 

In your workspace at `/home/user/project`, there is a build script named `build.sh`. It queries a local SQLite database (`/home/user/project/build_state.db`) for a list of pending compilation tasks, processes them in parallel to save time, and then updates their status to 'done'. Finally, it checks if all tasks were completed successfully.

Currently, the build often fails with the script reporting that some modules are still pending, even though the mock compilation steps seem to execute. Your CI/CD logs suggest this is an intermittent concurrency issue.

Your objectives are:
1. Diagnose the root cause of the build failures in `/home/user/project/build.sh`. You may use bash debugging techniques (e.g., `set -x`, traps, or inspecting standard error output) to trace the race condition.
2. Fix the `build.sh` script so that it runs reliably without leaving any pending tasks and consistently exits with code 0. You must maintain the parallel execution of the build steps (the `&` backgrounding must remain).
3. Once you have fixed the script, run it to ensure the database correctly reflects all modules as 'done'. 
4. Write a brief report to `/home/user/fix_report.txt` containing exactly one line with the root cause of the bug in the format: `ERROR=<error_message_you_found>`. (Hint: look at the stderr of the database update commands).

Do not change the structure of the database or remove the parallel execution feature. Your fix should gracefully handle the concurrency issue using Bash or SQLite features.