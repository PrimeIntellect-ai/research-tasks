You are tasked with debugging a failing custom Bash-based static site build system. The previous developer left the environment in a broken state, and the build script is crashing. 

The project is located at `/home/user/build_project`. You need to investigate the failure, recover any lost configuration, and identify the exact input causing the build to crash.

Here is what we know:
1. The main build script is `/home/user/build_project/build.sh`. When you run it, it currently fails immediately, complaining about a missing `config.inc` file.
2. The `config.inc` file was not deleted permanently; it was misplaced into a hidden backup directory somewhere inside `/home/user/build_project/` due to a recent misconfigured environment variable during a dry-run. You must find it and place it back at `/home/user/build_project/config.inc`.
3. Once the config file is restored, you will notice that `build.sh` requires a specific environment variable to be exported to run properly, otherwise it will exit safely. You will need to inspect the script, figure out what variable is expected, and export it.
4. After fixing the environment and configuration, running `./build.sh` will process 100 text files in `/home/user/build_project/src/`. However, the build crashes midway through with a cryptic `sed` error.
5. One (and only one) of the 100 files in the `src/` directory contains malformed syntax that breaks the fragile build script. 

Your goals:
1. Recover `config.inc` to `/home/user/build_project/config.inc`.
2. Determine the required environment variable and value to allow the build to proceed, and set it.
3. Use tracing (`bash -x` or similar) and delta debugging techniques to isolate the exact file in `src/` that causes the `sed` command to crash.
4. Once you have identified the problematic file, create a diagnostic report at `/home/user/debugging_report.txt` with the following strict format:

```text
MISSING_ENV_VAR=<The exact name of the environment variable you had to export>
POISON_FILE=<The exact filename of the bad file, e.g., file_010.txt>
POISON_CONTENT=<The exact text content of that bad file>
```

Ensure the final build runs successfully once the poison file is temporarily moved out of the `src/` directory. Leave the poison file outside of the `src/` directory (e.g., move it to `/home/user/build_project/`) so the build succeeds.