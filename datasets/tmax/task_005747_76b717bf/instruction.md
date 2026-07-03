You are an AI assistant helping a technical writer organize and process incoming documentation updates. 

The writer has an existing set of documentation in `/home/user/baseline/`. 
They have received a new set of documentation in a compressed archive located at `/home/user/incoming.tar.gz`.
However, the naming convention of the incoming files is outdated, and we only want to distribute the files that are actually new or have changed compared to the baseline.

Your task is to perform the following steps:
1. Extract the contents of `/home/user/incoming.tar.gz` into a new directory `/home/user/staging/`.
2. Read the JSON configuration file at `/home/user/rules.json`. This file contains a dictionary mapping old filename prefixes to new filename prefixes (e.g., `{"old_prefix_": "new_prefix_"}`).
3. Bulk rename all files inside `/home/user/staging/` by replacing their prefixes according to the rules in `/home/user/rules.json`. If a file's name does not start with any of the keys in the JSON, leave its name unchanged.
4. Compare the renamed files in `/home/user/staging/` against the files in `/home/user/baseline/`. Identify which files are "new" (do not exist in the baseline) or "modified" (exist in the baseline but the content differs).
5. Create a new compressed archive at `/home/user/incremental.tar.gz` containing ONLY the new or modified renamed files from `/home/user/staging/`. 
   - The files inside the `incremental.tar.gz` archive should not have any directory paths (i.e., just the filenames at the root of the archive).

You may use any programming language (e.g., Python, Bash) or standard Linux utilities to complete this task.