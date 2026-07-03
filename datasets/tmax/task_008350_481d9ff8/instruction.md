You are a backup operator testing a recent backup restoration and virtualization pipeline. We need to verify that a restored QEMU VM disk and its VNC logs are processed correctly, and test connectivity to the reported VNC ports.

Perform the following tasks:

1. **Extract Backup:**
   Extract the archive located at `/home/user/archive/sys_backup.tar.gz` into a new directory `/home/user/restored/`. 

2. **Text Processing on Logs:**
   Inside the extracted backup, there is a log file named `qemu_vnc.log`. Use standard shell text processing tools (e.g., `awk`, `grep`, `sed`) to extract only the port numbers from lines containing the exact phrase `VNC server running on 127.0.0.1:`. 
   Save these port numbers (one per line) to `/home/user/vnc_ports.txt`.

3. **Connectivity Verification using Rust:**
   Write a Rust program at `/home/user/test_connectivity.rs` and compile it to an executable named `/home/user/test_connectivity`. 
   The program must:
   - Read the port numbers from `/home/user/vnc_ports.txt`.
   - Attempt to establish a TCP connection to `127.0.0.1` on each of those ports.
   - For each port, write the result to a file at `/home/user/restored_vnc_status.txt` in the exact format:
     `PORT <port> IS UP` (if the TCP connection succeeds)
     `PORT <port> IS DOWN` (if the TCP connection fails or is refused)
   Run your compiled `/home/user/test_connectivity` binary to generate the status file.

4. **Fstab Configuration Mock:**
   Prepare an fstab entry for mounting the restored disk image. Create a file `/home/user/fstab_test` and write exactly one line into it containing the following fields (separated by spaces or tabs):
   - The absolute path to the extracted `disk.img` (which should be `/home/user/restored/disk.img`)
   - The mount point `/mnt/restored`
   - The filesystem type `ext4`
   - The mount options `loop,ro`
   - The dump and pass values `0 0`

Constraints:
- Do not use any external Rust crates (use only the standard library).
- Ensure all created output files have the exact names and paths specified above.