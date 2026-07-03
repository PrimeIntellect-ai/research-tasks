You are a platform engineer maintaining CI/CD pipelines for a large web application. Security policies for the Web Application Firewall (WAF) are submitted by different development teams as simple text files containing Allow lists. 

Before deploying to production, your pipeline needs an automated step to merge these access requests, remove duplicates, sort them, and ensure no requested paths violate the global security constraints (e.g., exposing internal or admin endpoints).

Write a Bash script located at `/home/user/build_acl.sh` that accomplishes this. The script must be executable and accept exactly three arguments in this order:
1. File path for Team A's ACL requests
2. File path for Team B's ACL requests
3. File path for the global constraints

Requirements for the script:
1. Read the contents of both Team A and Team B files. These files contain lines formatted as `ALLOW <path>` (e.g., `ALLOW /api/login`).
2. Merge the rules from both files, remove any exact duplicate lines, and sort the resulting list alphabetically.
3. Read the global constraints file. This file contains lines formatted as `DENY <path_prefix>` (e.g., `DENY /admin`).
4. Filter the merged, sorted list: If any `ALLOW` path starts with a `DENY` prefix, it must be completely removed from the final list. (For example, if the constraint is `DENY /internal`, then `ALLOW /internal/metrics` must be removed).
5. Write the final, filtered, deduplicated, and sorted list of `ALLOW` rules to `/home/user/final_acl.txt`.

Ensure your script handles standard text processing cleanly and creates the `/home/user/final_acl.txt` file when run. You can test your script by manually creating sample input files, but the automated test will provide its own files as arguments to your script.