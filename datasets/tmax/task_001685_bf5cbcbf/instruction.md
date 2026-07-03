You are an incident responder investigating a series of corrupted sensor logs. Recently, a regression was introduced in the logging pipeline (a repository with 200 commits is available for your inspection at `/app/log_repo`, though you don't need to fix the repo, just understand the bug). The bug causes some logs to contain out-of-bounds values due to integer overflows or floating-point precision loss, and occasionally corrupts the file's text encoding.

We need to quarantine the corrupted logs. An image containing the original engineering specifications for the sensors is located at `/app/specs.png`. You must extract the maximum safe threshold from this image.

Your task:
Write a standalone Bash script at `/home/user/filter.sh` that acts as a classifier. 
It must accept a single argument: the path to a log file.
- If the log file is valid (properly encoded UTF-8 and all numeric readings are strictly less than or equal to the threshold found in the image), the script must exit with status code `0`.
- If the log file is corrupted (contains invalid byte sequences, or contains any reading exceeding the threshold due to the boundary/overflow bug), the script must exit with status code `1`.

You have been provided with two directories to test your script:
- `/app/clean/`: Contains 50 valid log files.
- `/app/evil/`: Contains 50 corrupted log files.

Your script must exclusively use Bash and standard CLI utilities (like `awk`, `grep`, `bc`, `file`, `iconv`, etc.). Python, Perl, or other scripting languages are not allowed in `filter.sh`. Ensure your script correctly handles floating-point comparisons and edge cases (e.g., off-by-one errors) as well as encoding validation. Make sure to `chmod +x /home/user/filter.sh`.