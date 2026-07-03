You are a build engineer responsible for an artifact validation pipeline. You have inherited a project in `/home/user/project` containing a C program `artifact_filter` which evaluates whether an artifact should be approved based on its metadata. 

Currently, the project is in a broken state:
1. The `/home/user/project/Makefile` is broken (compilation fails).
2. The `artifact_filter.c` program has memory leaks and causes Valgrind to fail.

Your tasks:
1. **Fix the Makefile**: Edit `/home/user/project/Makefile` so that running `make` successfully compiles `artifact_filter.c` into an executable named `artifact_filter`. Ensure compilation includes debugging symbols (`-g`).
2. **Fix the C Code**: Modify `/home/user/project/artifact_filter.c` to fix any memory leaks. The program reads a single line from standard input in the format `size: <integer>` and takes a single command-line argument which is the maximum allowed size (integer). It prints `PASS` and exits with `0` if the size is strictly less than the maximum, otherwise it prints `FAIL` and exits with `1`.
3. **Create the CI Pipeline Script**: Write a bash script at `/home/user/ci_pipeline.sh` that automates the validation. The script must:
    - Run `make -C /home/user/project clean all`.
    - Validate that there are no memory leaks by running `valgrind --leak-check=full --error-exitcode=1 /home/user/project/artifact_filter 100` and feeding it `size: 50` via stdin. If Valgrind detects a leak or error, the script must exit immediately with code `1`.
    - Iterate over all `.txt` files in the directory `/home/user/artifacts/` (which contains files like `art1.txt`, `art2.txt`, each having a `size: <num>` line).
    - Run the `artifact_filter` on each file using a maximum size of `1000`.
    - Write the base names of the files (e.g., `art1.txt`) that result in `PASS` to `/home/user/approved.log`, one per line, sorted alphabetically.
    - Implement a simple rate limit: the script must `sleep 0.5` seconds immediately after executing the `artifact_filter` command for each file to simulate an API limit.

Make sure the script has executable permissions (`chmod +x /home/user/ci_pipeline.sh`). Run your script to generate `/home/user/approved.log`.