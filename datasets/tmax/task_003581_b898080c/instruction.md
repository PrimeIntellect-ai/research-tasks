You are a site administrator responsible for managing user accounts. The account management system is controlled by a custom local daemon written in C. 

Currently, the daemon is supposed to listen on `127.0.0.1` port `8888`, but automated scripts are failing to connect to it (returning "Connection refused"). The source code for this daemon is located at `/home/user/account_daemon.c`.

Your task is to:
1. Diagnose the connectivity issue. Fix the bug in `/home/user/account_daemon.c` that prevents it from correctly binding to port `8888`.
2. Compile the fixed C code to `/home/user/account_daemon` (using `gcc`) and start it in the background.
3. Write an Expect script at `/home/user/add_user.exp` that connects to the daemon using `nc 127.0.0.1 8888`. 
4. The Expect script must interact with the daemon to create a new user account. The interaction flow of the daemon is:
   - Daemon sends: `Welcome to AccountMgr. Enter command (ADD/DEL/QUIT): `
   - Client replies: `ADD`
   - Daemon sends: `Username: `
   - Client replies: `admin_xyz`
   - Daemon sends: `Success. Account created.` and closes the connection.
5. Run your Expect script and redirect all of its standard output to `/home/user/result.log`.

Requirements:
- Do not modify the prompt strings or the interaction logic in the C program, only fix the network binding issue.
- The Expect script must successfully complete the interaction and exit cleanly.
- Ensure the daemon continues to run in the background after your tasks are complete.