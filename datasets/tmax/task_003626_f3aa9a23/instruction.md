You are a DevOps engineer debugging a monitoring pipeline. Our latency monitoring service uses a compiled binary to calculate the variance of request response times. Recently, the variance metrics have been returning wildly inaccurate results (sometimes even negative) for certain high-baseline latency services, causing false alerts.

To make matters worse, the original log file that triggered the latest alert was accidentally deleted from the disk. However, we have a backup of the filesystem partition image where it resided at `/app/data.img`. 

Your tasks are:
1. **Deleted File Recovery**: Recover the deleted file `latency_data.log` from the ext4 filesystem image at `/app/data.img`. Save it to `/home/user/recovered_latency.log`.
2. **Format Parsing Edge-Case Repair**: The recovered log contains timestamps and latency values (in milliseconds), but the log format is slightly corrupted due to a bug in the log forwarder. Delimiters between the timestamp and the latency value vary (commas, pipes, spaces), and some lines have trailing garbage characters. Clean the file to extract just the numeric latency values.
3. **Numerical Instability Diagnosis**: The stripped binary `/app/variance_calc` calculates the variance of the numbers provided to it via standard input (one number per line). Run the cleaned data through it. You will see that it produces an incorrect result (likely due to catastrophic cancellation in its naive variance implementation, since the latency values are very large and clustered together).
4. **Stable Implementation**: Write a Bash script at `/home/user/stable_variance.sh` that takes the path to a file of numbers as its first argument and safely computes the sample variance (using a numerically stable method, like Welford's algorithm or an equivalent multi-pass approach). You may use standard Unix text processing tools like `awk` within your Bash script.
5. **Regression Test Construction**: Write a script `/home/user/regression.sh` that generates a small dataset demonstrating the numerical instability in `/app/variance_calc`, tests your `/home/user/stable_variance.sh` against it, and exits with code 0 if your script succeeds where the binary fails.

Your final script `/home/user/stable_variance.sh` must print only the calculated sample variance to standard output, formatted to 4 decimal places.

Deliverables:
- `/home/user/recovered_latency.log` (The raw recovered file)
- `/home/user/stable_variance.sh` (The robust Bash script)
- `/home/user/regression.sh` (The regression test)