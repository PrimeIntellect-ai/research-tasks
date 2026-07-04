You are an alert specialist tasked with creating a custom, standalone health-checker and emergency backup tool.

The system has a critical service that usually runs on `127.0.0.1` port `9090`, storing its data in `/home/user/app_data/`. 

Your task is to write a C++ program that checks the connectivity of this service and takes emergency action if it is down.

Please do the following:
1. Write a C++ program and save it exactly at `/home/user/watchdog.cpp`.
2. The program must use POSIX sockets to attempt a TCP connection to `127.0.0.1` on port `9090`.
3. If the connection is SUCCESSFUL:
   - The program should silently terminate and return an exit code of `0`.
4. If the connection FAILS (the port is unreachable):
   - The program must append exactly the following string (with a trailing newline) to `/home/user/alert.log`:
     `[ALERT] Port 9090 is unreachable`
   - The program must execute a shell command internally (e.g., using `system()`) to create a compressed tar archive of the `/home/user/app_data/` directory. The archive must be saved exactly as `/home/user/data_backup.tar.gz`.
   - The program must then terminate with an exit code of `1`.
5. Compile your code using `g++` to produce an executable file located at `/home/user/watchdog`.

Do not run the program in a continuous loop; it should perform a single check and exit. Automated tests will invoke `/home/user/watchdog` to verify its behavior under different port states.