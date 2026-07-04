You are a support engineer tasked with diagnosing and fixing a log processing pipeline. 

We have a script located at `/home/user/merge_timeline.sh` that is designed to merge logs from two different services and reconstruct a unified chronological timeline. The script is currently experiencing two issues:
1. It occasionally crashes on certain input lengths.
2. It has an off-by-one error that causes it to drop the very last log entry when merging.

Your task is to:
1. Write a simple fuzzing script at `/home/user/fuzz.sh` in bash that generates dummy log files of various lengths (e.g., 0 to 10 lines) and passes them to `/home/user/merge_timeline.sh` to identify any input lengths that cause a crash (non-zero exit code). You don't need to submit the fuzzer output, just the script itself.
2. Diagnose and fix the off-by-one error and the crashing boundary condition in `/home/user/merge_timeline.sh`. You may modify the script directly using any language or tool, but standard bash/Unix tools are recommended.
3. Once fixed, run the script against the real logs located at `/home/user/logs/srv1.log` and `/home/user/logs/srv2.log`.
4. Save the successfully reconstructed timeline to `/home/user/final_timeline.log`.

The real log files are formatted with a Unix timestamp followed by a message, e.g.:
`1672531200 [INFO] Service started`

Verify your fix ensures the output contains all lines from both input files, sorted numerically by the timestamp, with no missing entries at the end.