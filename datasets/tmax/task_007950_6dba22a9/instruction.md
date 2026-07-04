You are a cloud architect migrating a legacy network routing service to a new deployment architecture. Since you don't have root access on this jump server, you will build a simulated user-space CI/CD pipeline to test the deployment and configuration logic.

Your objective is to create a complete Git-based deployment workflow that compiles a C program, configures a mock routing table idempotently, and logs the pipeline's success.

Follow these exact steps:

1. **Git Server Configuration:**
   - Create a bare Git repository at `/home/user/router_repo.git`.
   - Configure a `post-receive` hook in this bare repository. The hook must:
     a. Extract the pushed code into a deployment directory at `/home/user/router_deploy`.
     b. Execute the deployment script `deploy.sh` (which will be part of the repository).
     c. Log the results to `/home/user/pipeline.log`.

2. **Repository Contents:**
   Create a local repository (e.g., in `/home/user/src`) and populate it with the following three files. You will push this repository to your bare repo to trigger the pipeline.
   
   **File A: `router.c`**
   - Write a C program that simulates a routing daemon.
   - It should accept exactly one command-line argument: a destination network (e.g., "10.0.5.0/24").
   - It must open and read the file `/home/user/mock_routes.conf`.
   - The configuration file will contain lines in the format `<DESTINATION> via <NEXT_HOP>`.
   - The program should search for the given destination network. If found, it prints ONLY the `<NEXT_HOP>` IP address to standard output. If not found, it prints "DROP".
   
   **File B: `config_routes.sh`**
   - Write an idempotent Bash script that manages the `/home/user/mock_routes.conf` file.
   - It must ensure the file exists and contains exactly these two routing entries (format: `<DESTINATION> via <NEXT_HOP>`):
     - `10.0.5.0/24 via 192.168.50.1`
     - `0.0.0.0/0 via 192.168.1.1`
   - **Crucial:** The script must be completely idempotent. If run 10 times, the file must still only contain exactly those two entries without any duplicates or blank lines.

   **File C: `deploy.sh`**
   - Write a bash script that the `post-receive` hook will execute.
   - It should be run from within the `/home/user/router_deploy` directory.
   - It must compile `router.c` into an executable named `router` using `gcc`.
   - It must execute `./config_routes.sh` to configure the routing file.
   - It must test the compiled C program by executing `./router 10.0.5.0/24`.
   - If the output of the C program is exactly `192.168.50.1`, it must append the exact string `PIPELINE_SUCCESS: 192.168.50.1` to `/home/user/pipeline.log`. If it fails, append `PIPELINE_FAILED`.

3. **Execution:**
   - Initialize the local repository, commit the three files (`router.c`, `config_routes.sh`, `deploy.sh`), and push to the `master` branch of the bare repository at `/home/user/router_repo.git`.
   - Ensure the hook triggers, the code compiles, the routes are idempotently configured, and the success message is logged.

Note: Set all necessary executable permissions for your scripts and hooks. Use absolute paths or correct relative paths based on the `post-receive` execution context.