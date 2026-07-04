You are an edge computing engineer deploying a simulated IoT gateway environment. Since you do not have root access on the build server, you need to configure a user-space QEMU virtual machine that maps custom network routing via host forwarding and dynamically reads host user configurations.

Your task is to write a Rust utility that generates a specific QEMU startup script. 

1. Create a configuration file at `/home/user/edge_config.txt` with the following exact contents:
```
MAC=52:54:00:11:22:33
VNC_DISPLAY=4
GUEST_PORT=80
HOST_PORT=8080
```

2. Write a Rust program at `/home/user/build_edge_node.rs`. This program must:
   - Read the `/home/user/edge_config.txt` file and parse the key-value pairs.
   - Read `/etc/passwd` to dynamically find the numeric UID of the user named `user`.
   - Generate a bash script at `/home/user/run_vm.sh` that contains exactly one line with the following QEMU command format (replace the bracketed placeholders with the dynamically parsed values):
     `qemu-system-x86_64 -m 256 -vnc 127.0.0.1:<VNC_DISPLAY> -netdev user,id=net0,hostfwd=tcp::<HOST_PORT>-:<GUEST_PORT> -device virtio-net-pci,netdev=net0,mac=<MAC> -fw_cfg name=opt/edge_uid,string=<UID>`

3. Ensure the Rust program makes the generated `/home/user/run_vm.sh` file executable (e.g., `chmod +x` equivalent in Rust, or running a shell command from Rust).

4. Compile the Rust program to the binary `/home/user/build_edge_node` using `rustc`.

5. Run your compiled binary so that `/home/user/run_vm.sh` is successfully generated.

Do not start the QEMU virtual machine yourself, just generate the executable startup script.