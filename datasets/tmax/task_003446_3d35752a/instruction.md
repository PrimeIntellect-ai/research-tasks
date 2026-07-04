You are an IT support technician. We have received a critical ticket regarding our internal math processing pipeline. 

The pipeline relies on a Bash script located at `/home/user/ticket_repo/calculate.sh`. This script is supposed to calculate the Collatz conjecture stopping time for numbers 1 through N. However, the script is currently hanging indefinitely when executed, preventing our daily jobs from completing. 

Additionally, the development team accidentally lost a crucial database password. We know this password was previously hardcoded in `calculate.sh` but was removed in a past commit to the git repository located at `/home/user/ticket_repo`.

Your tasks are to:
1. Diagnose and fix the infinite loop bug in `/home/user/ticket_repo/calculate.sh` so that it correctly computes the Collatz stopping time for integers.
2. Once fixed, execute the script with the argument `20` (i.e., `./calculate.sh 20`) and save its exact standard output to `/home/user/collatz_20.txt`.
3. Perform forensic analysis on the git repository at `/home/user/ticket_repo` to find the deleted database password.
4. Save the recovered password exactly as it appeared (just the password string itself, no quotes or variable names) into `/home/user/recovered_password.txt`.

The output format of `calculate.sh N` should be a list of lines, each formatted as `<number>: <stopping_time>`, for example:
1: 0
2: 1
3: 7
...

Please complete these steps and ensure the output files are strictly formatted as requested.