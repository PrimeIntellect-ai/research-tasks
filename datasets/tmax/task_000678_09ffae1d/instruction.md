You are a capacity planner analyzing network resource usage for a fleet of workstations. You have been provided with network usage logs and group assignments. Your goal is to identify the user group consuming the most total bandwidth, apply a new restricted quota to them using an interactive legacy CLI tool, and idempotently update a monitoring configuration file.

You need to perform the following steps:

1. **Analyze Network Usage**:
   - You have a CSV file at `/home/user/net_usage.csv` with the format: `User,IP_Address,Bytes_Transmitted,Bytes_Received`.
   - You have a group database at `/home/user/groups.db` with the format: `GroupName:User1,User2,...`.
   - Using Bash text-processing tools (like `awk`, `sed`, `grep`), calculate the total bandwidth (Bytes_Transmitted + Bytes_Received) for each group.
   - Identify the group with the highest total bandwidth usage. Calculate their target quota, which should be exactly 80% of their current total bandwidth usage.

2. **Automate Interactive Quota Management**:
   - There is a legacy interactive tool at `/home/user/quota_mgr`. When executed, it prompts:
     `Enter group to restrict:` (You must provide the highest-usage group name)
     `Enter new bandwidth limit:` (You must provide the 80% target quota calculated above)
   - Write an Expect script at `/home/user/update_quota.exp` that launches `/home/user/quota_mgr` and automatically answers these prompts. Run your expect script to apply the quota. 

3. **Idempotent Configuration Management**:
   - Write a Bash script at `/home/user/configure_alerts.sh` that updates a monitoring config file located at `/home/user/capacity_alerts.conf`.
   - Your script must add two lines to the file:
     `ALERT_GROUP=<Top_Group>`
     `THRESHOLD=<Target_Quota>`
   - This script must be strictly **idempotent**. If the script is run multiple times, it must ensure those exact key-value pairs exist but should never create duplicate lines or modify the file if the correct configuration is already present. (Assume the file might not exist initially, or might contain other unrelated settings). Run the script to generate the config file.

Ensure all artifacts (`/home/user/update_quota.exp`, `/home/user/configure_alerts.sh`, and `/home/user/capacity_alerts.conf`) are created and executed properly.