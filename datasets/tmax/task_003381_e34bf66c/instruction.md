You are a Site Reliability Engineer tasked with setting up an automated deployment pipeline for a monitoring service. 

An architecture diagram and specification has been provided as an image at `/app/monitor_spec.png`. You must extract the configuration from this image (you can use tools like `tesseract`) which will contain three key-value pairs in the format:
```
PORT=<port_number>
BACKUP_DIR=<absolute_path>
TOKEN=<secret_token>
```

Your objective is to build a Git-based deployment workflow that manages the lifecycle of this monitoring service and creates backups.

1. **Git Server Configuration:**
   - Create a bare Git repository at `/home/user/config.git`.
   - Configure a `post-receive` hook in this repository. 
   - The hook must automatically check out the pushed files into a working directory at `/home/user/app_state`.
   - After updating the working directory, the hook must execute a deployment script located at `/home/user/deploy.sh`.

2. **Deployment Script (`/home/user/deploy.sh`):**
   - Write this script using Bash.
   - It must ensure the `BACKUP_DIR` (extracted from the image) exists.
   - It must create a tarball backup of the current `/home/user/app_state` directory inside `BACKUP_DIR` (e.g., `backup-$(date +%s).tar`).
   - **Process Management:** It must terminate any previously running instance of the monitoring service to prevent port conflicts or ghost processes.
   - **Service Launch:** It must start the monitoring service in the background and detach it so the Git hook can complete successfully.

3. **Monitoring Service Requirements:**
   - The service must listen on the `PORT` specified in the image.
   - It must handle HTTP requests. When an HTTP `GET` request is made to the `/status` endpoint, it must respond with an HTTP 200 OK status.
   - The response body must contain exactly: `TOKEN=<secret_token>` (using the token extracted from the image).
   - You may implement this service using standard tools available in the environment (e.g., Python 3 standard library, `socat`, or `nc`).

4. **Integration and Execution:**
   - After fully configuring the repository, the hook, and the deployment script, you must trigger the pipeline.
   - Clone the bare repository, add a dummy configuration file (e.g., `touch config.txt`), commit it, and push it to the bare repository at `/home/user/config.git`.
   - Ensure the service is running successfully in the background and the backup is created.

Verify your service locally before concluding the task. The automated system will test your service by issuing real HTTP requests to the configured port.