You are tasked with configuring a Git hook for a simulated Kubernetes operator that manages deployments.

A local Git repository exists at `/home/user/operator-repo`. This repository contains Kubernetes deployment manifests, specifically a file named `manifest.yaml`. 

Your objective is to create a Python-based Git `post-commit` hook that acts as a deployment monitor and alert system. 

Write a Python script at `/home/user/operator-repo/.git/hooks/post-commit` and ensure it is executable. The hook must perform the following actions every time a commit is made:
1. Read the contents of `manifest.yaml` from the working directory.
2. Extract the integer value of `replicas:` from the file (the line will look exactly like `  replicas: X`).
3. Append a log entry to `/home/user/operator.log` in the exact format: `DEPLOY: replicas=<X>` (where `<X>` is the extracted integer).
4. Simulate an email alert for large scaling operations. If the replica count is strictly greater than 5, append a message to `/home/user/alerts.mail` in the exact format: `ALERT: High replica count detected (<X>)`

Do not use external libraries like `pyyaml` or `ruamel.yaml`; use standard Python text/regex parsing, as the YAML format will strictly follow the simple `replicas: X` structure. 

Ensure the script runs successfully with standard Python 3 (`#!/usr/bin/env python3`).