A subtle regression was introduced in the C++ project `event_logger`, located at `/home/user/repo`. The repository has about 200 commits.

The application compiles successfully and exits with code 0 across all recent commits. However, a timezone-related bug was introduced at some point: instead of trying to open the system's valid timezone file `/etc/localtime`, the program tries to open a misspelled path due to a broken Makefile flag. 

Because the C++ program has a silent fallback mechanism, it does not print any error messages or change its exit code when it fails to open the timezone file. 

Your task:
1. Write a test script that compiles the program (`make`) and uses system call tracing (e.g., `strace`) to determine whether the built `./event_logger` attempts to open the correct `/etc/localtime` file or the buggy path.
2. Use `git bisect` (or a custom delta debugging approach) along with your test script to automatically find the first commit that introduced the regression. The good commit is the very first commit in the repository. The bad commit is the current `HEAD`.
3. Save the full 40-character commit hash of the *first bad commit* to a file named `/home/user/bad_commit.txt`.

Do not modify the git history.