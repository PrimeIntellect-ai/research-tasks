We are deploying a lightweight virtualization appliance, and I need your help to automate the provisioning and network setup, as well as write a Go-based proxy filter.

You have been provided with an image file located at `/app/vm_config.png`. This image contains the expected SSH tunneling port and the VM instance ID that you need to provision.
Please perform the following steps:

1. **Information Extraction**:
   Extract the SSH port number and the VM instance ID from `/app/vm_config.png`.

2. **Directory and Link Setup**:
   Create a directory structure under `/home/user/provision/` named after the extracted VM instance ID. Within it, create a symbolic link named `latest-disk` pointing to `/app/base.qcow2`.

3. **SSH Tunneling**:
   Set up a local SSH port forward using the extracted port number, mapping local port `8080` to `localhost:<extracted_port>`. Save the PID of the tunneling process to `/home/user/tunnel.pid`.

4. **Go Proxy Filter**:
   Write a Go program at `/home/user/proxy_filter.go` that reads lines from standard input and writes to standard output. For each line, it should replace any occurrence of the word "DEV" with the extracted VM instance ID. Compile it to `/home/user/proxy_filter`. We will test this binary for exact equivalence against our reference implementation by sending it random input lines.

Ensure all file paths are exact and the compiled Go binary is executable.