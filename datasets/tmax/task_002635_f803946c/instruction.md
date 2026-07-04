You are a Site Reliability Engineer (SRE) building an offline configuration validation and monitoring tool. You need to write a C++ program that parses system configuration files to ensure the correct filesystem mounts and network routes are defined, and then generates a status report using a specific timezone.

Your task:
1. Write a C++ program at `/home/user/sre_monitor.cpp`.
2. The program must parse two mock configuration files located in `/home/user/sys_config/`:
   - `/home/user/sys_config/fstab` (a mock `/etc/fstab` file)
   - `/home/user/sys_config/routes` (a mock routing table, similar to `route -n` output)
3. The program must extract:
   - All mount points (the second column) that use the `ext4` filesystem type (the third column) from the `fstab` file.
   - The IP address of the default gateway (the Gateway column where Destination is `0.0.0.0`) from the `routes` file.
4. The program must generate a log file at `/home/user/system_status.log` with exactly the following format:
   ```
   Time: <YYYY-MM-DD HH:MM:SS JST>
   Gateway: <IP_ADDRESS>
   EXT4 Mounts: <comma_separated_list_of_mount_points>
   ```
   - For the `Time` line, the program must set the timezone to `Asia/Tokyo` internally (e.g., using the `TZ` environment variable within the C++ code before getting the time) and output the *current* time formatted exactly as shown. 
   - The `EXT4 Mounts` list must be comma-separated without trailing commas, in the order they appear in the file.
5. Compile your program to an executable named `/home/user/sre_monitor` (using standard `g++`).
6. Run the executable to generate the log file.

Note: Do not hardcode the extracted values in your C++ code. The test suite will replace the `fstab` and `routes` files with different contents to verify your parsing logic.