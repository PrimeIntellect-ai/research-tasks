You are a system administrator tasked with maintaining a custom, user-space load balancing mechanism. We rely on a directory of symlinks to define active backend servers. When a backend goes down, its symlink needs to be removed from the pool so the load balancer stops routing traffic to it.

Currently, the active backend pool is located at `/home/user/pool/`. 
Inside this directory, there are several symlinks. Each symlink points to a text file in `/home/user/ports/`. The text file contains a single integer representing the port number on `127.0.0.1` that the backend service is listening on.

Your task is to write a C program that acts as an active health checker.

Requirements for the C program:
1. Source file must be saved to `/home/user/bin/healthcheck.c`.
2. Compile it to an executable at `/home/user/bin/healthcheck`.
3. The program must iterate through all items in `/home/user/pool/`.
4. For each symlink, it must read the target file to extract the port number.
5. It must then attempt to establish a standard TCP connection to `127.0.0.1` on that port.
6. If the TCP connection fails (e.g., port is closed / connection refused), the program must delete (unlink) the symlink from `/home/user/pool/`.
7. If the TCP connection succeeds, the program must gracefully close the socket and leave the symlink intact.

Once you have written and compiled the program, run it once to clean up the current pool.

Do not hardcode the specific port numbers or symlink names in your C code, as the pool is dynamic. Use standard POSIX directory and file I/O functions.