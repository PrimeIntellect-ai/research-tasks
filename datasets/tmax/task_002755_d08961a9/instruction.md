You are an AI assistant helping a compliance officer audit access control systems. We are reviewing historical transaction logs of role delegations to ensure they adhere to strict separation of duty and dependency policies.

You have been provided with an image of the current compliance policy at `/app/policy.png`. Read and understand the policy rule detailed in this image. 

We have sample transaction logs (in JSON format) containing historical authorization events. These are located in:
- `/app/corpus/clean/` (logs that comply with the policy)
- `/app/corpus/evil/` (logs that violate the policy)

Your task:
1. Analyze the JSON files in the corpora to reverse-engineer the data model for the transaction logs.
2. Based on the policy specified in the image, write a Bash script at `/home/user/audit.sh`.
3. The script must take exactly one argument: the path to a JSON transaction log file.
4. The script must output exactly `EVIL` to stdout if the log violates the policy, or `CLEAN` to stdout if it complies. 
5. Make sure the script is executable (`chmod +x /home/user/audit.sh`).

Your script will be tested against both the clean and evil corpora to ensure it accurately classifies 100% of the files without false positives or false negatives. Use standard shell utilities (e.g., `jq`, `awk`, `tsort`, `grep`) to implement the detection pipeline.