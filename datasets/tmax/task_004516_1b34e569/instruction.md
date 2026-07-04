You are taking over a project where the automated build is currently failing. The project is located in `/home/user/project`. 

When you run `python3 build.py`, it fails. The previous developer left two notes before leaving:
1. "I recently removed a hardcoded CI token from the code for security reasons and switched it to read from an environment variable (`CI_TOKEN`). I forgot to document the actual token value, but it should still be in the git history somewhere."
2. "I also recently reorganized the test directories, but I might have messed up the paths in the build script during my last commit."

Your task is to:
1. Recover the lost CI token from the git history.
2. Fix the misconfigured test directory path in `build.py`.
3. Provide the token to the build script via the `CI_TOKEN` environment variable and run the build successfully.

When `build.py` runs successfully, it will automatically generate a file at `/home/user/success.txt`. Leave this file in place, as it will be used to verify that the build completed successfully.