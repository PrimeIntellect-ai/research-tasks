You are acting as a Configuration Manager for a fleet of Linux servers. You need to audit configuration drift across different environments by comparing configuration files.

You have been provided with:
1. A metadata file `/home/user/server_info.csv` containing the mapping of servers to their environments. The file has a header `ServerName,Environment`.
2. A directory `/home/user/configs/` containing the actual configuration files for each server, named `<ServerName>.conf`. 

Your task is to write and execute a Bash script that analyzes these configurations and generates a report of configuration drift. 

Specifically, you must:
1. **Join/Group by Environment**: Only compare servers that are in the *same* environment. 
2. **Hash-based Deduplication/Exact Match**: For each pair of servers in the same environment, check if their configuration files are exactly identical using a cryptographic hash (e.g., MD5 or SHA256). If the hashes match, they are an exact match.
3. **Similarity Computation**: If the hashes do NOT match, calculate the line-based Jaccard similarity between the two files. 
   - Jaccard Similarity = (Number of shared unique lines) / (Total number of unique lines across both files).
   - Ignore the order of the lines in the files.
   - For example, if File A has lines {x, y, z} and File B has lines {y, z, w}, the intersection is {y, z} (size 2) and the union is {x, y, z, w} (size 4). The Jaccard similarity is 2/4 = 0.50.
4. **Generate Report**: Produce a CSV report at `/home/user/environment_diffs.csv`.
   - The file must have the following header exactly: `Environment,Server1,Server2,IsExactMatch,JaccardScore`
   - `Server1` and `Server2` must be in alphabetical order (e.g., if comparing `zeta` and `delta`, `Server1` must be `delta` and `Server2` must be `zeta`).
   - `IsExactMatch` must be `1` if the file hashes are identical, and `0` otherwise.
   - `JaccardScore` must be formatted to exactly two decimal places (e.g., `1.00`, `0.67`, `0.40`).
   - The rows in the final CSV (excluding the header) must be sorted alphabetically by `Environment`, then `Server1`, then `Server2`.

Create the solution entirely using Bash and standard Linux command-line utilities. Make sure the final output file is generated correctly.