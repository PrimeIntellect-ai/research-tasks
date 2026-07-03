You are a site administrator tasked with building a tool to fetch user disk quotas from a legacy remote system.

The legacy system consists of two parts:
1. A jump host running an SSH server on port 2222.
   - Username: `admin`
   - Password: `siteadmin`
2. A legacy Quota Management Service running on the jump host's local loopback interface (127.0.0.1) on TCP port 9090.

The legacy Quota Management Service uses an interactive text-based protocol:
- Upon connection, it sends: `Enter username: `
- Client sends the requested username followed by a newline (`\n`).
- It sends: `Enter password: `
- Client sends the hardcoded service password `querypass` followed by a newline.
- It returns: `QUOTA <used_bytes> <limit_bytes>\n` (or an error message) and then closes the connection.

Your tasks:
1. Establish a persistent SSH port forward (tunnel) so that local port 8080 on your machine forwards to 127.0.0.1:9090 on the jump host.
2. Write a C++ program that acts as a CLI client for this service.
   - The program must read a single username from standard input (stdin).
   - It must connect to local port 8080.
   - It must navigate the interactive protocol (you may use C++ socket programming, or execute an Expect script from within the C++ code).
   - It must print the result to standard output (stdout).

Output format:
Your C++ program must format the output perfectly. To ensure your output is exactly correct, we have provided a stripped reference binary (an oracle) at `/app/oracle_bin`. 
Your compiled program must be placed at `/home/user/quota_cli`.
For ANY given username provided on stdin, the stdout of `/home/user/quota_cli` must be BIT-EXACT equivalent to the stdout of `/app/oracle_bin` given the same input. You can run `/app/oracle_bin` yourself to reverse-engineer the exact expected output format and error handling.

Constraints & Requirements:
- The SSH tunnel must remain running in the background listening on local port 8080 so that subsequent automated tests can use it.
- Your C++ source code should be saved at `/home/user/quota_cli.cpp` and compiled to `/home/user/quota_cli`.
- You may install any necessary C++ libraries or expect/tcl packages using the system package manager.