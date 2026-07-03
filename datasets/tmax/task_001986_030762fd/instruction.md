You are an on-call engineer who just got paged at 3:00 AM. 

The nightly mathematical batch processing job is failing. The build pipeline for our variance calculation tool, located at `/home/user/stats_project`, has suddenly broken. 

Earlier this evening, a junior engineer ran a poorly written cleanup shell script (`cleanup.sh`) that was intended to remove old backup files. Unfortunately, the script failed to handle filenames with spaces correctly, and it accidentally deleted a critical source file. The junior engineer then blindly committed the changes to Git before signing off.

Your task is to fix the build and successfully process tonight's dataset.

Here is what you need to do:
1. Navigate to `/home/user/stats_project`.
2. Recover the deleted C header file. (Hint: check the Git history).
3. Diagnose and fix the build failure. The `Makefile` currently suffers from a dependency conflict between two statically linked math libraries (`liblegacy.a` and `libadvanced.a`). Update the `Makefile` to only link against the advanced library, resolving any symbol conflicts.
4. Compile the application successfully by running `make`.
5. Once built, run the compiled `./calc_variance` executable on `/home/user/stats_project/dataset.txt`.
6. Redirect the exact standard output of the program to `/home/user/stats_project/final_result.txt`.

Do not write any new C code; you should only need to recover the missing file, modify the `Makefile`, compile, and run the program.