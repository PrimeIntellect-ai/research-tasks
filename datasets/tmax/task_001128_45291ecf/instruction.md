You are acting as a storage administrator helping to manage disk space on a Linux server. We have a directory containing application logs at `/home/user/app_logs`, and we need to clean them up and archive the recent ones to save space.

Please perform the following steps:
1. Identify all log files in the `/home/user/app_logs` directory that have been modified more recently than the reference file `/home/user/last_run.stamp`.
2. For those recently modified log files ONLY, perform an in-place edit to remove all lines containing the exact string `[TRACE]`. Leave all other files untouched.
3. After cleaning, extract all remaining lines containing the exact string `[ERROR]` from these recently modified files and append them to a new file at `/home/user/error_summary.txt`.
4. Finally, package only these recently modified (and now cleaned) log files into a gzip-compressed tar archive located at `/home/user/processed_logs.tar.gz`. The archive should not contain absolute paths (i.e., when extracted, it should just extract the files or the `app_logs` directory relatively).

Ensure your operations strictly target only the files newer than `last_run.stamp`. Use standard bash utilities to accomplish this.