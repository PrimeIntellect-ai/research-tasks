You are a deployment engineer rolling out a new software update across several application components. Before deploying, you must verify that there is enough disk quota available for each component's directory. 

You have been provided with two files:
1. `/home/user/quota_report.txt`: A legacy storage monitoring report containing raw, unformatted text. The file has lines that look like: `DIR /path/to/dir USAGE <used_MB> QUOTA <max_MB>`.
2. `/home/user/update_dirs.txt`: A simple text file containing a list of target directories for the upcoming deployment (one directory per line).

Your task is to create a robust text processing pipeline and a C++ analyzer to determine if the deployment can proceed. The incoming update will add exactly **350 MB** of new files to *each* target directory.

Perform the following steps:
1. Write a C++ program at `/home/user/quota_analyzer.cpp` that reads filtered text from standard input (stdin). Each line of input will contain a directory path, its current usage in MB, and its quota in MB (you can decide the exact format it expects, as you will pipe data to it). The C++ program must calculate whether adding 350 MB to the usage exceeds the quota. 
2. The C++ program must output a report directly to a file named `/home/user/deployment_status.log`. For every directory processed, it must write exactly one line in this format:
   `[<STATUS>] <DIR> requires <X> MB more quota`
   - `<STATUS>` must be `OK` if usage + 350 <= quota, or `EXCEEDS` if usage + 350 > quota.
   - `<DIR>` is the directory path.
   - `<X>` is the shortfall in MB if the quota is exceeded, or `0` if it is OK.
   - The output lines in the log must be sorted alphabetically by directory name.
3. Write a robust Bash script at `/home/user/deploy_check.sh` that:
   - Compiles the C++ program into an executable at `/home/user/quota_analyzer`.
   - Uses text processing tools (`grep`, `awk`, `sed`, etc.) to extract only the lines from `/home/user/quota_report.txt` that correspond to the directories listed in `/home/user/update_dirs.txt`.
   - Pipes this cleaned/filtered data into the compiled `/home/user/quota_analyzer` executable.
   - Handles errors gracefully (e.g., exits with a non-zero code if compilation fails).
   
Execute your bash script so that the `/home/user/deployment_status.log` is generated.