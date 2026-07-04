You are tasked with building the core logic of a lightweight, filesystem-based "Kubernetes Operator" simulator using C. This operator manages reverse proxy traffic routing based on architectural diagrams and ensures manifest backups.

We have an architectural diagram at `/app/diagram.png`. This image dictates the required traffic splitting weights between two backend services: `service-v1` and `service-v2`. 

Perform the following steps:

1. **Environment Setup**:
   - Create a directory `/home/user/backup`.
   - Configure the user's `~/.bashrc` (or `~/.profile`) to export the environment variable `OPERATOR_BACKUP_DIR=/home/user/backup`.

2. **Information Extraction**:
   - Use `tesseract` (pre-installed) to read `/app/diagram.png` and extract the target traffic percentage weights for `v1` and `v2`.

3. **Operator Implementation (C)**:
   - Write a C program at `/home/user/operator.c` and compile it to `/home/user/operator`.
   - When run, this program must:
     a) Read the manifests in `/home/user/manifests` (assume this directory contains dummy `.json` files representing cluster state).
     b) Implement a backup strategy: before making any changes, the C program must archive and compress the `/home/user/manifests` directory into `$OPERATOR_BACKUP_DIR/manifests_backup.tar.gz`. (You may use system() calls to standard coreutils/tar).
     c) Generate a valid Nginx or HAProxy reverse proxy configuration file at `/home/user/proxy.conf`. This configuration must define a load balancer (upstream or backend cluster) that routes traffic to `127.0.0.1:8081` (service-v1) and `127.0.0.1:8082` (service-v2) using the exact proportional weights extracted from the image. 
     *Note: Ensure the load balancer weights in the generated configuration reflect the exact ratio specified in the image.*

Ensure you compile the C program and run it so that `/home/user/proxy.conf` and the backup archive are fully generated and present on the system.