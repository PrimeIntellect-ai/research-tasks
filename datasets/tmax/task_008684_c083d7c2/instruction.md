You are a Linux Systems Engineer tasked with hardening the local deployment configuration for a new service. You will need to prepare a backup strategy using virtual disk images, fix a C++ configuration generator, provision TLS certificates, and generate a secure port-forwarding proxy script.

Perform the following tasks in the `/home/user` directory. You do not have root access.

1. **Virtualization & Backup Preparation**
   Create a directory `/home/user/backup`.
   Using `qemu-img`, create a base QCOW2 virtual disk image named `/home/user/backup/base.qcow2` with a size of exactly `50M`.
   Then, create a second QCOW2 image named `/home/user/backup/snapshot.qcow2` that uses `base.qcow2` as its backing file.

2. **TLS Certificate Generation**
   Create a directory `/home/user/certs`.
   Using `openssl`, generate a self-signed RSA 2048-bit certificate and unencrypted private key.
   Save the certificate as `/home/user/certs/cert.pem` and the key as `/home/user/certs/key.pem`.
   Set the Common Name (CN) of the certificate to `localhost`. Leave other subject fields at their defaults.

3. **C++ Configuration Generator Fix & Execution**
   You have been provided with a broken C++ source file at `/home/user/src/port_manager.cpp`.
   This program is supposed to output a `socat` command that sets up a TLS-terminating proxy, but it contains syntax errors and missing includes.
   Fix the C++ code so that it successfully compiles and prints exactly this string to standard output, followed by a newline:
   `socat openssl-listen:8443,reuseaddr,fork,cert=/home/user/certs/cert.pem,key=/home/user/certs/key.pem,verify=0 tcp:127.0.0.1:9090`
   
   Compile your fixed code to `/home/user/bin/port_manager` (create the `bin` directory if it does not exist).
   Finally, execute the compiled binary and redirect its output into a new shell script at `/home/user/start_proxy.sh`. Make `/home/user/start_proxy.sh` executable.