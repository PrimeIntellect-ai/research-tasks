You are acting as a backup operator managing restore tests for our virtualization infrastructure. We have an automated system that serves raw VM disk backups over the network, and we need to securely port-forward the connection, download the disk image, and efficiently compress it into a QCOW2 format for archival.

Here is your workflow:

1. **Network Configuration**: We have generated an architecture diagram at `/app/diagram.png`. Read the image to find the "Gateway Port" and the "Internal Storage Port".
2. **Port Forwarding**: Set up a local port forwarder (using `socat` or a simple Python script) that listens on the Gateway Port and forwards all TCP traffic to the Internal Storage Port on localhost. 
3. **Backup Retrieval & Processing**: Write a Python script `/home/user/process_backup.py` that:
   - Connects to localhost on the Gateway Port.
   - Reads the raw disk image stream (the server will close the connection when the transfer of the 50MB raw disk is complete).
   - Converts the downloaded raw disk data into a highly compressed QCOW2 image saved at `/home/user/archived_disk.qcow2`.
   - *Hint:* You can save the raw stream to a temporary file and use system calls to `qemu-img` with compression enabled (`-c`), or implement it directly. 

Our automated verifier will inspect `/home/user/archived_disk.qcow2`. It will verify that it is a valid QCOW2 file representing the original disk image. 

The evaluation is based on a **compression metric**: the final file size of `/home/user/archived_disk.qcow2` must be strictly optimized. Since the raw disk is largely empty (sparse) with a few isolated data blocks, aggressive compression should significantly reduce its size.

To complete the task, ensure your Python script has run, the port forward is functional, and the final optimized `.qcow2` file exists in your home directory.