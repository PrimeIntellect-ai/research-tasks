You are acting as a capacity planner analyzing resource usage for a simulated local CI/CD artifact storage environment. Your goal is to write an idempotent Python script that calculates directory sizes, manages a directory structure using symlinks for top consumers, and sets up environment variables for the pipeline.

Please perform the following tasks:

1. Write a Python script at `/home/user/analyze_capacity.py`. The script must:
   - Scan all immediate subdirectories within `/home/user/projects`.
   - Calculate the total size in bytes of each subdirectory (including all files within them).
   - Ensure the directory `/home/user/capacity_review` exists (create it if it doesn't).
   - Create symlinks inside `/home/user/capacity_review` pointing to the **top 2 largest** project directories.
     - The symlink names must be formatted as `rank_1_<project_dirname>` (for the largest) and `rank_2_<project_dirname>` (for the second largest).
     - The symlinks must use **relative paths** to point to the project directories.
     - The symlink creation must be idempotent (if the script runs twice, it should not fail, and the links should remain correct).
   - Generate a JSON report at `/home/user/capacity_review/report.json` containing the sizes of all scanned projects, sorted from largest to smallest. The format must exactly match:
     ```json
     {
       "projects": [
         {
           "name": "project_name",
           "size_bytes": 12345
         }
       ]
     }
     ```
   - Idempotently append the environment variable `export CAPACITY_REVIEW_DIR="/home/user/capacity_review"` to `/home/user/.profile`. It should only append it if the string `CAPACITY_REVIEW_DIR` does not already exist in the file.

2. Create a bash script at `/home/user/pipeline.sh` that acts as a simple CI pipeline step.
   - It must execute the Python script `/home/user/analyze_capacity.py`.
   - It must redirect the standard output and standard error of the Python script to `/home/user/pipeline.log`.
   - Ensure the bash script is executable.

Execute your pipeline script (`/home/user/pipeline.sh`) at least once to ensure all links, reports, and configurations are generated successfully.