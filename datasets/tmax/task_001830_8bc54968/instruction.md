You are a network engineer troubleshooting a simulated deployment pipeline. Due to a recent security change, SSH key-based login for the internal Git server is silently bypassing keys and falling back to a custom interactive pin prompt, breaking our automated deployment scripts. 

Your objective is to fix the deployment pipeline by configuring the Git hook, resolving the network routing query, and automating the push using Expect.

Here are your tasks:

1. **Routing Information**: 
   Determine the default IPv4 gateway address of your current system. Create a file named `routing_info.txt` inside `/home/user/workspace` and write ONLY the IPv4 address of the default gateway into it. Commit this file to the local Git repository located in `/home/user/workspace` (the repository is already initialized and has a remote named `origin` pointing to `/home/user/central.git`).

2. **Git Hook Configuration**:
   Create a `pre-receive` hook in the bare repository at `/home/user/central.git/hooks/pre-receive`. Write this hook in **Python 3**. 
   The hook must:
   - Read the standard input (`oldrev`, `newrev`, `refname`).
   - Use `git show` or `git cat-file` to extract the contents of `routing_info.txt` from the incoming `newrev` commit.
   - Validate that the contents of `routing_info.txt` strictly match a basic IPv4 address format (e.g., 4 dot-separated integers).
   - Exit with status `0` if it is a valid IP, or print an error and exit with status `1` if it is missing or invalid.
   - Ensure the hook is executable.

3. **Expect Automation**:
   The `git push` command currently hangs because a wrapper script asks for a pin. 
   Write an Expect script at `/home/user/workspace/deploy.exp` that:
   - Spawns the `git push origin master` command from within `/home/user/workspace`.
   - Waits for the exact prompt `Enter Deployment Pin: `.
   - Sends the pin `8821` followed by a newline.
   - Waits for the push to complete successfully.

4. **Execution**:
   Run your Expect script and redirect its standard output to `/home/user/push.log`.

Verify that your `push.log` shows a successful Git push and that the remote repository has accepted the commit.