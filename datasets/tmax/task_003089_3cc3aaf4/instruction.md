You are tasked with writing a Bash script that acts as a simulated Kubernetes operator handling network manifests. 

There is an incoming directory at `/home/user/manifests` where YAML files defining custom cluster configurations are dropped. You need to write a script at `/home/user/k8s-operator.sh` that processes these files. 

Your script must perform the following actions for every `.yaml` file found in `/home/user/manifests/`:

1. **Extract Routing Information:** Find the `podCIDR` value inside the YAML file. The YAML files contain a block like this:
   ```yaml
   spec:
     podCIDR: 192.168.100.0/24
   ```
2. **Generate Network Config:** Append a routing command to `/home/user/apply_routes.sh` for each extracted CIDR. The command appended should exactly match the format: 
   `ip route add <CIDR> via 10.96.0.1`
   (e.g., `ip route add 192.168.100.0/24 via 10.96.0.1`).
3. **Manage Permissions:** Once a manifest is processed, move it to `/home/user/processed_manifests/`. To ensure immutability, change the permissions of the moved file in the destination directory so that it is read-only for the owner, and has no permissions for anyone else (octal `0400`).
4. **Logging:** Append a line to `/home/user/operator.log` with the exact format: 
   `PROCESSED <filename> <CIDR>` 
   (where `<filename>` is just the base name of the file, e.g., `cluster-alpha.yaml`).

**Requirements:**
- Ensure `/home/user/apply_routes.sh` is created if it doesn't exist, and is made executable (`chmod +x`).
- Process the files in alphabetical order by filename.
- After writing `/home/user/k8s-operator.sh`, execute it once so the initial files in the directory are processed. 

*Note: You do not need root access to write these user-space files or modify their permissions. Standard shell utilities (grep, awk, sed, etc.) are sufficient.*