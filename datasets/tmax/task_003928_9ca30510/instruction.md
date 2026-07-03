You are acting as a network engineer troubleshooting connectivity for a set of headless QEMU virtual machines. You need to automate the detection of network failures and alert the administration team.

To accomplish this, write a custom Go application and set it up under process supervision. 

Your tasks are:

1. **Write a Go Program**
Create a Go program at `/home/user/net_troubleshooter.go` and compile it to `/home/user/net_troubleshooter`. The program must do the following in order:
* **Mount/fstab configuration parsing**: Parse the file `/home/user/fstab.conf`. Find the line where the device name is exactly `/dev/vdb1`. Extract the mount point directory from that line (it will be the second whitespace-separated field).
* **Network log analysis**: Inside that extracted mount point directory, read the file named `network.log`. Count the exact number of times the string `ERROR: CONNECTIVITY_LOST` appears.
* **QEMU/VNC parsing**: Parse the file `/home/user/qemu.opts` which contains command-line arguments for the VM. Find the `-vnc` argument (e.g., `-vnc 127.0.0.1:3`). Calculate the actual TCP port for VNC (base 5900 + display number, so display `:3` is port `5903`).
* **Email Alert generation**: If the connectivity lost count is greater than 0, write an email file to `/home/user/mailspool/alert.eml` with exactly this format (replace bracketed items with your calculated values):
  ```
  To: admin@local
  Subject: Network Alert
  
  Connection lost <count> times.
  VNC Port: <port>
  ```
  If the file already exists, overwrite it.
* **Exit code**: If the count was greater than 0, the program must exit with status code `1`. If the count is 0, exit with status code `0`.

2. **Process Supervision Configuration**
Create a systemd user service unit file to supervise this Go binary.
* Path: `/home/user/.config/systemd/user/net-watcher.service`
* The service must run the compiled binary: `/home/user/net_troubleshooter`
* Set the restart policy to restart the service only if it fails (`Restart=on-failure`).
* Set the restart delay to 5 seconds (`RestartSec=5`).
* Make sure it is part of the `default.target` (in the Install section).

Ensure the Go code compiles without errors and the systemd unit file is valid. Do not attempt to start the systemd service (as you do not have a running systemd user instance in this container), just place the configuration file properly.