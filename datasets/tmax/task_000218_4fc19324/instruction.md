You are tasked with setting up a Git-based task automation system to manage user accounts. As a site administrator, you want to manage users by pushing a `users.json` file to a Git repository, which then automatically generates a bash script with the required user account and group administration commands. 

Since you do not have root access in this environment, you will not run the actual `useradd`/`userdel` commands. Instead, your task is to create the Git server, configure the hook, and write the Python logic that parses the configuration and writes the shell script for a root user to execute later.

Follow these specific steps:

1. Initialize a bare Git repository at `/home/user/account_manager.git`.
2. Create a Git `post-receive` hook written in **Python 3** at `/home/user/account_manager.git/hooks/post-receive`. Ensure the hook is executable.
3. The `post-receive` hook must read the standard input provided by Git (which contains `oldrev newrev refname` separated by spaces).
4. For the pushed commit (`newrev`), the hook must read the contents of the file named `users.json` from the repository. You can use a command like `git show <newrev>:users.json` within your Python script to extract its content.
5. Parse the `users.json` file. It will contain a JSON list of dictionaries. Each dictionary will have:
   - `"username"`: The string username.
   - `"action"`: Either `"add"` or `"remove"`.
   - `"groups"`: A list of string group names (only present if action is `"add"`).
6. Based on the parsed JSON, the hook must generate a bash script exactly at `/home/user/apply_users.sh`.
7. The generated script `/home/user/apply_users.sh` must:
   - Start with `#!/bin/bash`
   - For every `"add"` action, output commands to create the groups first, then the user. 
     - For each group in the user's `"groups"` list, output exactly: `groupadd -f <group_name>`
     - Then output exactly: `useradd -m -G <group1>,<group2>,... <username>` (groups must be comma-separated in the exact order they appeared in the list). If the user has no groups, omit the `-G` flag and its argument entirely.
   - For every `"remove"` action, output exactly: `userdel -r <username>`
   - The commands must be generated in the exact order the users appear in the JSON list.
8. The hook must set the file permissions of `/home/user/apply_users.sh` to exactly `700` (`-rwx------`) using Python's `os.chmod` or a shell command.

Your solution will be tested by cloning the bare repository, committing a `users.json` file, pushing it to the `master` branch, and inspecting the generated `/home/user/apply_users.sh` file.