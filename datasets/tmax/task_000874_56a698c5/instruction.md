You are a debugging engineer investigating a regression and a memory leak in a long-running C service that parses timestamps from incoming telemetry. 

The source code is located in a Git repository at `/app/repo`. Recently, a subtle bug was introduced that causes timestamp parsing to fail under certain conditions, and the service has also started leaking memory. 

Additionally, the previous engineer left a voice memo in `/app/voice_memo.wav` detailing the specific timezone offset that the production server uses. 

Your tasks are to:
1. Analyze the audio file `/app/voice_memo.wav` (you may use tools like `whisper` or `ffmpeg` available in the environment) to extract the spoken timezone offset.
2. Perform a `git bisect` in `/app/repo` to identify the exact commit that introduced the parsing regression. The repository includes a `test_regression.sh` script which fails on the bad commits.
3. Once you identify the root cause of the regression, modify `parser.c` to fix it. 
4. Analyze `parser.c` for a memory leak (you may want to use `valgrind` or system call tracing) and fix the memory leak so that the program safely processes strings without leaking memory.
5. Apply the timezone offset extracted from the audio file to the parsing logic in `parser.c` (there is a macro or constant you should update).
6. Compile the fixed program to the exact path: `/app/repo/parser`. 

The compiled executable must take a single command-line argument (the telemetry string) and print the processed timestamp. 

We have provided a stripped oracle binary at `/app/oracle_parser` which represents the mathematically correct, leak-free version of the program with the correct timezone offset applied. Your final compiled executable `/app/repo/parser` must produce output that is strictly bit-exact equivalent to `/app/oracle_parser` for any given telemetry string.