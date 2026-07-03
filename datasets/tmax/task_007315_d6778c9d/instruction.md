You are a DevOps engineer tasked with recovering and processing some critical logs on a Linux system.

A background process called `log_generator.sh` has been running and writing logs to a file. However, another team member accidentally deleted the log file while it was still being written to. Because the background process is still running and holds the file open, the data is not lost, but it is no longer visible in the filesystem.

Your tasks are:

1. **Recover the deleted log file**:
   Identify the process writing the deleted log file, recover the contents from memory/procfs, and save the recovered logs to exactly `/home/user/recovered_log.txt`.

2. **Fix the build script**:
   We have a C tool `/home/user/filter_tool.c` used to calculate severity scores for log messages. The script `/home/user/build_tool.sh` is supposed to compile it to `/home/user/filter_tool`, but it currently fails with a compiler/linker error. Interpret the error, fix `build_tool.sh`, and successfully compile the tool.

3. **Fix the log processor script**:
   The script `/home/user/process_logs.sh` reads a log file and uses `filter_tool` to calculate a score for `[ERROR]` messages. However, it has two critical bugs:
   - A logic flaw causes an infinite loop (it never terminates when it reaches the end of the file).
   - A format parsing edge-case: it incorrectly passes log messages to the `filter_tool`. Log messages may contain spaces and quotes (e.g., `Failed to load "config.json" - retrying`), which causes the tool to only process the first word or fail. You must ensure the *entire* message string (everything after the level) is passed as a single argument to `filter_tool`.

4. **Generate the final output**:
   Once all fixes are in place, run the repaired script against the recovered logs and redirect the output:
   `./process_logs.sh /home/user/recovered_log.txt > /home/user/final_output.txt`

Ensure that the final output file `/home/user/final_output.txt` is created and contains the correctly computed error scores.