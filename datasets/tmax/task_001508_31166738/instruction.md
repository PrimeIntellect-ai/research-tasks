You are an automation specialist tasked with creating a high-performance Bash pipeline to process and anonymize time-series system logs. 

We have a custom, highly optimized IP anonymization tool called `log-masker` (version 1.0.0). Its source code is vendored at `/app/log-masker-1.0.0`. Unfortunately, a recent commit introduced a build error in its `Makefile`, preventing it from compiling. 

Your objectives:
1. Identify and fix the build issue in the `log-masker` package at `/app/log-masker-1.0.0`. Compile and install it so the `log-masker` executable is available in your PATH or accessible to your script.
2. Write a Bash script at `/home/user/process_logs.sh` that processes a large dataset of raw logs located in `/home/user/data/raw_logs/`.
3. The raw logs contain unstructured text lines in the following format:
   `[YYYY-MM-DD HH:MM:SS] src_ip=<IP_ADDRESS> message="<SOME_TEXT>"`
4. Your Bash script must pipeline the processing to achieve the following:
   - Extract the date and hour (i.e., `YYYY-MM-DD HH`) and the `<IP_ADDRESS>` from each line.
   - Pass the extracted IP addresses through the fixed `log-masker` tool to mask them. (The `log-masker` tool reads from stdin and writes to stdout, replacing IPs with a deterministic masked version).
   - Group the data by the extracted hour and the masked IP address.
   - Count the number of occurrences for each `(Hour, Masked_IP)` pair.
   - Output the final aggregated results to `/home/user/output.csv` in the format: `YYYY-MM-DD HH,Masked_IP,Count`. The output should be sorted chronologically by hour, and then by Count (descending).

Your pipeline needs to be extremely efficient to handle large scale data, hence the reliance on Bash utilities (like `awk`, `sort`, `uniq`) and the custom C-based `log-masker` tool. 

The final evaluation will measure the F1 score of your `output.csv` against our verified golden dataset. You must achieve an accuracy metric of >= 0.99.