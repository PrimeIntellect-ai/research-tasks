You are an AI assistant acting as an automated artifact manager. We have an incoming spool of binary artifacts that need to be curated based on a configuration file. Because a downstream process constantly polls the curated directory, you must use atomic writes (writing to a temporary file, then renaming with `mv`) to ensure no incomplete files are read.

Your objective is to write and execute a script (in any language you choose, though Bash or Python are recommended) that processes nested archives according to specific rules.

Here is the setup:
- **Incoming Directory:** `/home/user/incoming/`
  Contains several `.tar.gz` artifact files.
- **Curated Directory:** `/home/user/curated/`
  Where the processed artifacts must be placed.
- **Configuration File:** `/home/user/rules.ini`
  Contains rules for how to process each project. Format:
  ```ini
  [Rules]
  alpha = keep
  beta = extract_logs
  gamma = drop
  ```

**Artifact Structure:**
Each `.tar.gz` file in `/home/user/incoming/` contains:
1. A `meta.txt` file. This file contains a single line: `project=<project_name>` (e.g., `project=alpha`).
2. A `payload.zip` file. Inside this zip file, there are various files, including a `logs.tar.bz2` file.

**Processing Instructions:**
For each `.tar.gz` file in `/home/user/incoming/`:
1. Use compressed stream processing to read `meta.txt` without extracting the entire `.tar.gz` file to disk.
2. Determine the project name and look up its rule in `/home/user/rules.ini`.
3. If the rule is `keep`:
   - Copy the entire original `.tar.gz` file into `/home/user/curated/`.
4. If the rule is `extract_logs`:
   - Extract *only* the `logs.tar.bz2` file from within the nested `payload.zip` inside the `.tar.gz` file.
   - Save this file into `/home/user/curated/` with the name `<original_filename_without_extension>_logs.tar.bz2` (e.g., if original is `build_42.tar.gz`, the output is `build_42_logs.tar.bz2`).
5. If the rule is `drop` or the project is not in the rules:
   - Do nothing with this artifact.
6. **ATOMIC WRITES MANDATORY:** When writing *any* file to `/home/user/curated/`, you must first write/copy it to a temporary filename (e.g., `filename.tmp`) in the same directory, and then use `mv` to rename it to the final filename. 
7. Create a log file at `/home/user/curation.log` with one line per processed artifact in the format:
   `[<RULE_APPLIED>] Processed <filename>`
   (e.g., `[keep] Processed build_1.tar.gz` or `[extract_logs] Processed build_2.tar.gz`). Do not log dropped artifacts.

Write and run the script to complete the curation process.