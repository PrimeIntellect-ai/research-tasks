You are tasked with finding a regression in a data processing application using `git bisect`.

The repository is located at `/home/user/data_processor`.
The application is built using `make`, which produces an executable called `data_processor`.
It processes an input file provided as a command-line argument.

Recently, a regression was introduced between the tags `v1.0` (known good) and `v2.0` (known bad). When processing the corrupted input file located at `/home/user/corrupted_input.csv`, the `v1.0` application safely ignores the corrupted rows and exits gracefully. However, the `v2.0` application intermittently hangs or crashes due to a race condition in the error recovery logic.

Your goal is to find the exact commit that introduced this intermittent failure. 

Because the bug is intermittent and some commits in the repository fail to compile, you should write a bash script to automate the `git bisect run` process. Your script must adhere to the following rules:
1. Attempt to build the application with `make`. If there are compiler or linker errors (i.e., `make` fails), you must tell `git bisect` to **skip** the commit.
2. If the build succeeds, test the `./data_processor` executable against `/home/user/corrupted_input.csv`.
3. Because the failure is intermittent, run the executable up to 20 times for a given commit.
4. If the executable exits with a non-zero status or takes longer than 1 second to run *at least once* during the 20 attempts, consider the commit **bad**.
5. If it successfully exits with a zero status 20 times in a row within the time limit, consider the commit **good**.

Once you have identified the first bad commit, write its full Git SHA hash to the file `/home/user/bad_commit.txt`.

**Note:** You must create `/home/user/corrupted_input.csv` with some dummy text data (e.g., `id,value\n1,100\nERR,200`) before running your tests, as the application requires a file to read.