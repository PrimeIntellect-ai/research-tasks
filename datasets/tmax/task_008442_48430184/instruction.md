You are a deployment engineer tasked with automating a rolling deployment of a new Python application to a cluster of virtualized nodes. You must write a Python automation script that handles user authorization, virtual machine disk backups, and the staged rollout. 

You have three target nodes located at:
- `/home/user/nodes/node1`
- `/home/user/nodes/node2`
- `/home/user/nodes/node3`

Each node directory currently contains a virtual machine disk image named `disk.qcow2`.

You need to write and execute a Python script at `/home/user/deploy_automation.py` that strictly performs the following steps in order:

1. **User Authorization Check**:
   Read the custom group administration file located at `/home/user/admin_groups.txt`. This file has the format `groupname:user1,user2,user3`. 
   Extract the list of users belonging to the `deployers` group. 
   Write these usernames (one per line, alphabetically sorted) to `/home/user/deploy_auth.log`. If the `deployers` group is empty or missing, the script should exit immediately with an error.

2. **Rolling Backup and Deployment**:
   For each node (in numerical order: node1, then node2, then node3), perform the following actions sequentially:
   
   a. **Backup**: Create a copy-on-write snapshot backup of the QEMU virtual disk. Execute the `qemu-img` command to create a new image named `disk_backup.qcow2` in the node's directory, using the original `disk.qcow2` as its backing file. The new file must be in `qcow2` format.
   
   b. **Deploy**: Copy the new application payload from `/home/user/update_payload.py` into the node directory and name it `app.py`.
   
   c. **Verify**: Run the newly deployed `app.py` inside the node directory using Python. If the script exits with code 0, append the exact string `Node {X} deployed successfully` (where {X} is the node number, e.g., 1, 2, or 3) to `/home/user/deployment.log`. If it fails, the script should abort the deployment process for any remaining nodes.

Your script must handle the entire workflow. Ensure all log files and backups are placed exactly where requested. Run your script to perform the deployment.