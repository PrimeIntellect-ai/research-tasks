You are a bioinformatics analyst working on a sequence scoring pipeline. 

We have a custom C program used for processing sequence similarity matrices, but it needs to be compiled. Additionally, our pipeline script currently produces slightly different final scores on different machines due to floating-point addition not being strictly associative. The shell script passes unsorted file paths to the scoring program, so the filesystem's default directory traversal order dictates the reduction order of the sequence scores.

Your tasks:
1. Compile the C source code located at `/home/user/src/score_seq.c` into an executable binary at `/home/user/bin/score_seq`. Use standard `gcc` with no special flags. (Create the `bin` directory if it does not exist).
2. Fix the Bash script `/home/user/run_pipeline.sh`. It currently uses `find` to pass `.dat` files from `/home/user/seq_data/` to the scoring program. Modify the script so that the file paths are sorted strictly alphabetically before being piped to the `score_seq` executable. Ensure the pipeline uses the newly compiled binary at `/home/user/bin/score_seq`.
3. Execute the fixed `/home/user/run_pipeline.sh` and save its standard output to `/home/user/reproducible_output.txt`.

Ensure `/home/user/run_pipeline.sh` remains a valid, runnable Bash script.