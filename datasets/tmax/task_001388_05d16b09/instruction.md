You are an AI assistant acting as a DevOps engineer to implement a staged deployment script for a simulated Kubernetes operator.

You need to write a Python script at `/home/user/deploy_operator.py` that manages a rolling deployment across multiple staging environments. The script must process Kubernetes manifest files, perform health checks by analyzing monitoring logs, and generate a final email notification payload.

Here are the requirements for your script:

1. **Manifest Location**: The Kubernetes YAML manifests are located in `/home/user/manifests/`. There are three files: `stage1.yaml`, `stage2.yaml`, and `stage3.yaml`. They currently use the image `myregistry.local/frontend:v1.0`.
2. **Rolling Deployment Logic**: Your script must process the stages sequentially (stage1, then stage2, then stage3).
3. **Health Checks**: Before deploying a stage (modifying its manifest), you must check its health by parsing `/home/user/monitoring.log`. 
   - Search the log for entries belonging to the current stage (e.g., `[stage1]`).
   - If the word `CRITICAL` appears anywhere in the log entries for that stage, the health check fails.
   - If a health check fails, your script must **abort** the deployment immediately. Do not modify the manifest for the failed stage, and do not proceed to any subsequent stages.
4. **Manifest Update**: If the health check passes, update the manifest file for that stage to use the image `myregistry.local/frontend:v2.0`. You may use Python's text processing or invoke shell tools (like `sed` or `awk`) via `subprocess`.
5. **Notification Email**: After the pipeline finishes (either successfully or aborted due to failure), your script must generate an email payload at `/home/user/deployment_email.eml`.

The email file must strictly follow this exact format:
```
To: devops-alerts@local.domain
Subject: Staged Deployment Report

Successful Deployments: [comma-separated list of successful stages, e.g., stage1, stage2]
Failed Stage: [name of the failed stage, e.g., stage3, or "None" if all succeeded]
```

Run your Python script to perform the deployment simulation and generate the outputs.