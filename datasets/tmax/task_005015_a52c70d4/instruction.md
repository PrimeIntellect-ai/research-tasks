You are a monitoring specialist tasked with setting up automated alerts for configuration file changes. 

A local bare Git repository exists at `/home/user/alerts_repo.git`. A cloned workspace exists at `/home/user/workspace`. Inside the workspace, there is an interactive bash script `/home/user/workspace/make_alert.sh` that prompts a user for input, generates an alert configuration file, commits it, and pushes it to the bare repository.

Your task is to automate this workflow and set up a server-side Git hook to log file modifications.

Perform the following steps:

1. Write an idempotent configuration script in Python at `/home/user/setup_hook.py`. When run, this script must install a `post-receive` hook into `/home/user/alerts_repo.git/hooks/post-receive`. 
   - The hook itself must be an executable Python script.
   - The hook must read standard input (which Git provides as `oldrev newrev refname`).
   - For every pushed commit, the hook must find the names of the files modified or added.
   - If a modified/added file has a `.txt` extension, the hook must append exactly the following line to `/home/user/hook_alerts.log`:
     `ALERT: File <filename> was modified`
   - Your `setup_hook.py` script must be idempotent (running it multiple times must result in the correct, working hook without infinitely appending text or corrupting the hook file). Execute this script.

2. Write an Expect script at `/home/user/trigger.exp`. This script must spawn `/home/user/workspace/make_alert.sh` and automatically interact with it by answering its prompts in order:
   - Prompt: `Enter alert filename: ` -> Answer: `critical.txt`
   - Prompt: `Enter severity: ` -> Answer: `HIGH`
   - Prompt: `Enter message: ` -> Answer: `Database connection lost`

3. Run your Expect script (`expect /home/user/trigger.exp`) so that it generates the commit and triggers the hook. 

Upon completion, `/home/user/hook_alerts.log` should contain the alert for the newly pushed text file.