You are a container specialist managing a local configuration pipeline for legacy microservices. You need to automate a deployment process using Git hooks and interactive scripting, as the legacy deployment tool requires interactive prompts.

Your objective is to set up a local Git-based deployment pipeline that automatically checks out configuration files and deploys them using a provided interactive script.

Here are the requirements:
1. Initialize a bare Git repository at `/home/user/microservices.git`.
2. Configure a `post-receive` Git hook in this repository.
3. When triggered, the hook must checkout the latest main branch into a working directory at `/home/user/deploy_workspace`. (You must create this directory and ensure the Git hook populates it correctly).
4. After checking out the files, the hook must programmatically execute the existing legacy deployment script located at `/home/user/legacy_deploy.sh`. 
5. The `legacy_deploy.sh` script is strictly interactive. Your hook must use an Expect script (or a language of your choice like Python with pexpect) to interact with it:
   - The script will first prompt exactly with: `Token: `
   - You must read the secret token from `/home/user/.secrets/deploy_token.txt` and send it to the prompt.
   - The script will then prompt exactly with: `Proceed with filesystem sync? (yes/no): `
   - You must send `yes`.
6. To complete the task, clone the bare repository to `/home/user/local_clone`, create a file named `app_config.json` containing `{"version": "2.0"}`, commit it to the `main` branch, and push it to the bare repository at `/home/user/microservices.git`.

If your setup is correct, pushing the commit will trigger the hook, interact with the legacy script, and successfully write the deployment artifacts to `/home/user/deploy_out/`. Ensure all scripts you write have executable permissions.