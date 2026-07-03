You are a systems engineer investigating a severe memory leak in a long-running C-based event processing daemon. Recently, the daemon has been crashing in production after prolonged periods of handling cancelled events. 

We have captured a core dump from a recent crash, located at `/home/user/crash.core`. The exact binary that produced this core dump is located at `/home/user/event_daemon_crash_bin`.

Additionally, the source code repository for the daemon is located at `/home/user/event_daemon/`. The test suite includes a specific test case for event cancellation, which can be run via `make test_cancel`.

Your task is to debug the issue and compile a forensic report. Specifically, you need to:
1. Analyze the core dump (`/home/user/crash.core`) to identify the exact name of the C function where the segmentation fault occurred.
2. Analyze the Git repository (`/home/user/event_daemon/`) to identify the precise commit that introduced the memory leak. The leak is triggered during event cancellation. You may use tools like `valgrind` alongside `make test_cancel` to pinpoint when the leak first appeared in the commit history.
3. Identify the name of the C `struct` that is being leaked in that commit.

Save your findings in a JSON file at `/home/user/debug_report.json` with the following exact schema:

```json
{
  "crashing_function": "exact_function_name_from_core_dump",
  "leaking_commit_hash": "full_40_character_git_commit_hash",
  "leaked_struct_name": "name_of_the_leaked_struct"
}
```

Make sure your JSON is perfectly formatted. Do not modify the Git repository's current branch or commit state in your final output, though you may checkout different commits during your investigation.