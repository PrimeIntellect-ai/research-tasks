You are acting as an infrastructure engineer automating user provisioning verification. We need a lightweight, scheduled monitoring tool to ensure required service accounts exist on our newly provisioned servers.

Please complete the following tasks:

1. **Write a C++ program:** Create a file at `/home/user/filter_users.cpp`. The program must:
   - Read expected usernames from a file named `/home/user/expected_users.txt` (one username per line).
   - Read actual existing usernames from standard input (`stdin`), one per line.
   - Compare the two lists and determine which expected users are *missing* from standard input.
   - Append the missing usernames to `/home/user/missing_users.log` in the exact format: `Missing: <username>` (one per line, sorted alphabetically).
   - Compile this program to an executable at `/home/user/filter_users`.

2. **Create an automation script:** Write a bash script at `/home/user/check_users.sh`. The script must:
   - Use a text processing tool (like `awk` or `cut`) to extract all usernames from `/etc/passwd` that have a UID greater than or equal to 1000.
   - Pipe this list of usernames directly into your compiled `/home/user/filter_users` executable.
   - Ensure the script is executable.

3. **Schedule the task:** Add a cron job for the current user (`user`) that runs `/home/user/check_users.sh` exactly at the top of every hour (e.g., 00 minutes).

Ensure that if `/home/user/check_users.sh` is run manually, the `/home/user/missing_users.log` is created and correctly lists any missing users from `expected_users.txt`.