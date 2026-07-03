You are a security researcher conducting a forensic analysis on a compromised machine. You have recovered two key artifacts from the incident:
1. A suspicious compiled C binary located at `/home/user/decryptor`.
2. A raw Ext4 filesystem image located at `/home/user/usb.img`, which the attacker formatted and used before unmounting.

Through initial intel, you know the attacker stored an encrypted payload on the USB drive but deleted it to cover their tracks. The `decryptor` binary is supposed to decrypt this payload, but it fails to run in its current environment. 

Your task is to:
1. Inspect the filesystem image (`/home/user/usb.img`) and recover the deleted payload file. Save the recovered file to `/home/user/recovered.bin`. (Hint: You do not need root privileges or a mountpoint to inspect an unmounted ext4 image. Standard filesystem debugging tools are available).
2. Analyze the `decryptor` binary. Use system call tracing to discover why it fails to execute and what environment dependencies or files it requires.
3. Use binary analysis / reverse engineering tools (like `strings`, `objdump`, or `gdb`) on the C binary to determine the exact contents of the missing dependency it checks for.
4. Recreate the necessary system state so the binary successfully runs.
5. Execute the binary against your recovered payload: `./decryptor /home/user/recovered.bin`.

If successful, the binary will output the decrypted text to `/home/user/flag_decoded.txt`. 

To complete the task, read the contents of `/home/user/flag_decoded.txt` and write the exact text (which should be a flag format like `FLAG{...}`) to `/home/user/solution.txt`.