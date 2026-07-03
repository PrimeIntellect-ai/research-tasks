As a site administrator, you need to automate the provisioning of user accounts into a legacy backend system. The backend system only accepts connections over an interactive text-based protocol, and due to recent firewall changes, it is only accessible via a forwarded port.

Your objective is to build a small automation pipeline utilizing C++, Bash, SSH port forwarding, and Expect.

Here are the requirements:

1. **Input Data**: You have a file at `/home/user/pending_users.txt` containing a list of users to be created, one per line, in the format `username:role` (e.g., `alice:admin`).
2. **C++ Parser**: Write a C++ program at `/home/user/parser.cpp` and compile it to `/home/user/parser`. This program must read `/home/user/pending_users.txt` and output the exact string `ADD_USER [username] AS [role]` to standard output for each line in the input file (e.g., `ADD_USER alice AS admin`).
3. **SSH Tunneling**: The legacy backend is running locally on port `9999`. You must write a robust bash script at `/home/user/run_pipeline.sh` that sets up a local SSH port forward so that local port `8888` is forwarded to `localhost:9999`. 
    * Note: SSH keys for `user@localhost` are already configured for passwordless entry. Ensure the tunnel runs in the background and is properly cleaned up when the script exits (use bash `trap`).
4. **Interactive Automation**: Inside `/home/user/run_pipeline.sh`, after establishing the tunnel, you must automate an interactive session with the backend using `nc localhost 8888` and an Expect script (which you should write to `/home/user/interact.exp`).
    * When connected, the backend will prompt: `READY>`
    * For each line outputted by your compiled C++ `/home/user/parser`, your expect script must send that line to the backend.
    * After sending a user command, the backend will reply `SUCCESS` and then prompt `READY>` again.
    * Once all users have been sent, your expect script must send `QUIT` to terminate the connection gracefully.

Your final deliverable is the successfully executed bash script `/home/user/run_pipeline.sh` which leaves the backend successfully updated. Ensure the bash script compiles the C++ code, starts the tunnel, invokes the expect script with the parsed data, and cleans up the SSH tunnel upon completion.