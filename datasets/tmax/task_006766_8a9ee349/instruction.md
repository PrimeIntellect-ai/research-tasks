You are tasked with building a deployment script for a simplified continuous delivery pipeline. We are simulating a Kubernetes operator's behavior by programmatically managing application manifest files.

You have been provided with two application manifests in JSON format (representing Kubernetes Deployments) and a CSV file representing the deployment pipeline plan.

Your environment contains the following files:
1. `/home/user/manifests/frontend.json`
2. `/home/user/manifests/backend.json`
3. `/home/user/plan.csv`

The `plan.csv` file has the following format:
```csv
app_name,stage
frontend,canary
backend,production
```

Your goal is to write a Python script named `/home/user/staged_rollout.py` that automates a staged deployment rollout. 
The script must:
1. Read `/home/user/plan.csv`.
2. For each row, load the corresponding JSON manifest from `/home/user/manifests/<app_name>.json`.
3. Modify the JSON object based on the `stage`:
   - If the stage is `canary`:
     - Set `.spec.replicas` to `1`.
     - Update the container image (located at `.spec.template.spec.containers[0].image`). If the image tag does not end with `-canary`, append `-canary` to it (e.g., `my-image:2.0` becomes `my-image:2.0-canary`).
   - If the stage is `production`:
     - Set `.spec.replicas` to `5`.
     - Update the container image. If the image tag ends with `-canary`, remove the `-canary` suffix (e.g., `my-image:1.5-canary` becomes `my-image:1.5`).
4. Ensure the output directory `/home/user/deploy_out/` exists.
5. Save the modified JSON object to `/home/user/deploy_out/<app_name>_<stage>.json` with an indentation of 2 spaces.

After creating the script, execute it so that the final state is present in the `/home/user/deploy_out/` directory. Do not leave any hardcoded values in your script specifically for 'frontend' or 'backend'; it should dynamically read the CSV.