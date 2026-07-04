You have inherited a legacy codebase located in `/home/user/legacy_tool`. Your job is to debug the build pipeline, fix a shell script bug, and recover a lost test asset from the repository's history.

Please perform the following steps:

1. **Fix the build:** The build script `/home/user/legacy_tool/build.sh` currently fails to compile the C program `process.c`. Diagnose the compiler/linker error and fix `build.sh` so that it successfully produces the executable `./process`.
2. **Fix the wrapper script:** The script `/home/user/legacy_tool/run.sh` is supposed to pass a single filename argument to the `./process` executable. However, it currently breaks when the provided filename contains spaces. Fix `run.sh` so that it safely handles filenames with spaces.
3. **Recover the lost test data:** Look through the git history of the repository to find a test file that was deleted. This file has a space in its filename. Recover this exact file from the git history and place it in `/home/user/legacy_tool` under its original name.
4. **Process the data:** Run your fixed `run.sh` and pass the recovered test file as the argument. Redirect the standard output of this run to `/home/user/output.txt`.

Do not hardcode the output or bypass the scripts. Both `build.sh` and `run.sh` must be correctly patched to work in general, and the C program must be the entity performing the processing.