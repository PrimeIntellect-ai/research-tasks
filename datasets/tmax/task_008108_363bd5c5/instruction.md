You are acting as a compliance officer auditing an organization's internal IT systems. You have been provided with access logs and role-mapping data exported to the directory `/home/user/audit_data/`. 

Your task is to use standard Bash tools (awk, grep, sort, join, etc.) to analyze these relationships, validate the schema, and produce compliance reports. 

Here are the requirements:

1. **Schema Validation**: 
   The `/home/user/audit_data/` directory contains several `.csv` files. You must check that the first line (headers) of specific files match the expected schema exactly:
   - `users.csv` expected header: `user_id,username`
   - `user_roles.csv` expected header: `user_id,role_id`
   - `roles.csv` expected header: `role_id,role_name`
   - `role_access.csv` expected header: `role_id,system_id,permission_level`
   
   If ANY `.csv` file in that directory does NOT match its expected header (or is not one of these 4 expected files and thus has an unrecognized header), append its base filename (e.g., `bad_file.csv`) to `/home/user/invalid_schemas.log`.

2. **Graph Analytics (System Centrality)**:
   By linking users -> user_roles -> role_access, figure out which `system_id` is the most "central" or accessible. Specifically, find the `system_id` that is accessible to the highest number of *distinct* usernames (regardless of permission level). 
   Write only the `system_id` string to `/home/user/most_accessible_system.txt`.

3. **Cross-query Aggregation (Admin Report)**:
   Generate a report of users with "admin" access to systems. By traversing the tables, map `username`s to the `system_id`s they have `admin` privileges on. Count the number of distinct systems each user has `admin` access to.
   Create a file `/home/user/admin_summary.txt` containing the username and their admin system count, separated by a colon (e.g., `alice:2`). 
   - Only include users who have admin access to at least 1 system.
   - Sort the output descending by the count. If there's a tie, sort alphabetically by username.

All processing must be done using bash/shell commands. Do not write a Python script or use other scripting languages.