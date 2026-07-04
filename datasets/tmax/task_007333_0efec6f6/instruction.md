Hello! I need a tool to identify the default network interface on our Linux servers based on the routing table, and I need a wrapper script to run it properly. 

Please perform the following steps:

1. Create a C program at `/home/user/src/gateway_finder.c`. This program must:
   - Read the system routing table from `/proc/net/route`.
   - Find the line representing the default gateway (where the `Destination` column is exactly `00000000`).
   - Extract the interface name (the first column, e.g., `eth0` or `ens3`).
   - Read the environment variable `GW_OUT_FILE`.
   - Write the extracted interface name (just the name and a newline) to the file path specified by `GW_OUT_FILE`.
   - Exit cleanly.

2. Compile the C program and output the executable to `/home/user/bin/gateway_finder`. Make sure you create the `/home/user/bin` and `/home/user/src` directories first.

3. Create a bash wrapper script at `/home/user/run_finder.sh` that does the following:
   - Creates the directory `/home/user/output` if it does not already exist.
   - Sets and exports the environment variable `GW_OUT_FILE=/home/user/output/iface.log`.
   - Executes the `/home/user/bin/gateway_finder` binary.
   - Make the script executable and run it to ensure `/home/user/output/iface.log` is generated.

4. We also need to set up a shell profile variable. Append a line to `/home/user/.bash_profile` that exports the variable `DEFAULT_GW_CHECK=1`.

Please ensure the C program handles potential errors gracefully (e.g., if the environment variable is not set, or if the file cannot be opened) and that all scripts have the correct execute permissions.