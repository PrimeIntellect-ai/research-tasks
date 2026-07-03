You are an AI assistant acting as a configuration manager. We need to track configuration drift between our local baseline configs and the newest configurations currently stored in a remote backup directory. 

Your task is to write a Python script that processes these configurations, implements quality gates, calculates similarity, and produces a final report.

Here are the requirements:
1. **Local-Remote Transfer:** 
   Copy all files from the "remote" directory `/home/user/remote_configs` to a new local processing directory `/home/user/incoming`.
   The local baseline configs are located in `/home/user/local_configs`. 
   For every app, there will be a file named `<app_name>.json` in both `/home/user/local_configs` and `/home/user/incoming`.

2. **Validation Checkpoints (Quality Gates):**
   Iterate through each `<app_name>`. Read the corresponding JSON files from both the local configs and incoming configs. 
   You must validate that both files contain strictly valid JSON. 
   - If both are valid, the status is `VALID`.
   - If the local file is invalid JSON, the status is `INVALID_LOCAL`.
   - If the incoming file is invalid JSON, the status is `INVALID_INCOMING`.
   *(Assume for this task that both won't be simultaneously invalid).*

3. **Distance & Similarity Computation:**
   For apps with a `VALID` status, calculate the **Jaccard similarity** of the top-level JSON keys between the local config and the incoming config. 
   *Note: Jaccard similarity between two sets of keys A and B is defined as the size of their intersection divided by the size of their union.*
   If the status is invalid, the similarity score must be exactly `0.00`.
   Round all similarity scores to 2 decimal places.

4. **Sorting and Reporting:**
   Generate a CSV report located exactly at `/home/user/config_drift_report.csv`.
   The CSV must have the following header: `app_name,status,similarity_score`
   The rows must be sorted alphabetically by `app_name`.

Example row format:
`app_example,VALID,0.67`
`app_other,INVALID_INCOMING,0.00`

Write the necessary scripts and bash commands to complete this entire workflow.