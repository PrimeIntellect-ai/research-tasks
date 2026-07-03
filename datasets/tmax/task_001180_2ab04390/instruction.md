You are a site administrator tasked with automating the generation and version control of user profile configurations. You will use Expect, C, Bash, and Git to create a secure, automated workflow.

Follow these steps exactly:

1. There is an interactive script located at `/home/user/tools/create_profile.sh` that prompts for user details and generates a profile file in `/home/user/profiles/`. 
   Write an Expect script at `/home/user/build_profiles.exp` that automates this interactive tool to create the following three users:
   - Username: `admin1`, Role: `sysadmin`, Status: `ACTIVE`
   - Username: `user1`, Role: `developer`, Status: `ACTIVE`
   - Username: `baduser`, Role: `guest`, Status: `BANNED`
   Run your Expect script so the three `.txt` files are generated in `/home/user/profiles/`.

2. We want to ensure that "BANNED" profiles are never committed to our version control system. 
   Write a C program at `/home/user/check_ban.c`. The program must:
   - Accept exactly one command-line argument: the path to a profile text file.
   - Read the file.
   - If the file contains the exact string `Status: BANNED`, the program must print "Banned user detected" to standard output and exit with status code `1`.
   - If the string is not found, it must exit with status code `0`.
   Compile this program to the executable `/home/user/check_ban`.

3. Initialize a Git repository in the `/home/user/profiles/` directory.

4. Create a Git client-side hook at `/home/user/profiles/.git/hooks/pre-commit` (ensure it is executable). The hook must:
   - Find all `.txt` files currently staged for commit (using text processing pipelines like `git diff` and `grep`).
   - Run the `/home/user/check_ban` executable on each staged `.txt` file.
   - If `/home/user/check_ban` exits with code 1 for any file, the hook must abort the commit (exit with code 1).
   - If all staged files pass, the hook should allow the commit (exit with code 0).

5. Add all three generated `.txt` files to the Git staging area in `/home/user/profiles/` and attempt to commit them. The commit should fail due to your hook.

6. Unstage `baduser.txt` so it is not included in the commit. Successfully commit the remaining files (`admin1.txt` and `user1.txt`) with the exact commit message: `Initial profiles`.

7. Run `git log -1 --format=%s` in `/home/user/profiles/` and save the output to `/home/user/success_log.txt`.