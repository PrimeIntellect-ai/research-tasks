You are a cloud architect migrating internal services to a new environment. As part of this, you are using a custom C-based application firewall daemon that authenticates users before allowing them to access a forwarded port. However, the migration is currently failing due to incomplete code and race conditions in the startup scripts.

Your objectives are:

1. **Implement the User Group Administration Logic in C:**
   You have a skeleton file at `/home/user/app_fw.c`. The daemon is mostly complete, but the function `int check_group(const char* username)` is empty.
   You must implement this function to open and read `/home/user/groups.txt`.
   The file `/home/user/groups.txt` contains lines in the format `username:group`.
   Your C function must return `1` if the provided `username` belongs to the `migrators` group, and `0` otherwise.
   Compile your finished code to `/home/user/app_fw` (e.g., `gcc -o /home/user/app_fw /home/user/app_fw.c`).

2. **Automate the Interactive Firewall Testing:**
   Write an Expect script at `/home/user/test_fw.exp`.
   This script must spawn a connection to the daemon using `nc localhost 7777`.
   The daemon will prompt exactly with: `Username: `
   Your expect script must send the username `alice` (who is a migrator).
   If successful, the daemon will respond with a line starting with `TOKEN: ` followed by a secret string.
   Your Expect script must capture this token line and write the exact line (e.g., `TOKEN: <the_secret>`) to `/home/user/success.log`.

3. **Fix the Startup Dependency (The Missing "After="):**
   There is a script at `/home/user/start.sh` that launches the firewall daemon in the background and then executes your Expect script. Currently, it fails sporadically because it attempts to run the Expect script before the C daemon has finished initializing and binding to port 7777 (similar to a missing `After=` dependency in systemd).
   Modify `/home/user/start.sh` so that it explicitly waits for port 7777 to be open and listening before it executes `/home/user/test_fw.exp`. Do not just use a static `sleep`; programmatically check that the port is open (e.g., using a loop with `nc -z`).

To complete the task, ensure `/home/user/app_fw` is compiled, `/home/user/test_fw.exp` is created, `/home/user/start.sh` is fixed, and then execute `/home/user/start.sh` so that `/home/user/success.log` is generated successfully.