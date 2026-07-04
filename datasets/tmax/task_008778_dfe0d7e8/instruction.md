You are a cloud architect migrating a legacy system. We are running a local staged deployment pipeline for a data migration job. We have a Rust application (`rust_app`) that depends on a mock database service script (`init_db.sh`). 

Currently, the deployment pipeline fails because the Rust application starts up and tries to connect to the database before the database initialization script has finished creating its lockfile (a missing dependency/race condition issue). Additionally, the database script prompts for a password interactively, which breaks our automated CI/CD pipeline.

All files are located in `/home/user/migration_project`.

Here are your tasks to fix the deployment pipeline:

1. **Task Automation (Expect Scripting)**: 
   The script `/home/user/migration_project/db_service/init_db.sh` requires interactive input. Write an `expect` script at `/home/user/migration_project/init_db_auto.exp` that executes `init_db.sh` and automatically provides the password `migrate123` when prompted with "Enter admin password to initialize DB: ".

2. **Environment Variable Setup**: 
   Create a shell script at `/home/user/migration_project/env_setup.sh`. When sourced, this script must export the environment variable `DATA_PATH` set to `/home/user/migration_project/data`.

3. **Rust Code Modification (Handling the Race Condition)**: 
   The Rust application at `/home/user/migration_project/rust_app/src/main.rs` attempts to read a flag file (`$DATA_PATH/db_ready.flag`) to confirm the database is ready. Currently, it panics immediately if the file is missing. 
   Modify the Rust application to retry reading the file up to 10 times, sleeping for 1 second between attempts (using `std::thread::sleep` and `std::time::Duration`). 
   If it succeeds, it must append the exact string "Connection established\n" to `/home/user/migration_project/app.log`. 
   If it fails after 10 attempts, it should panic or exit with a non-zero status.

4. **Staged Deployment Script**: 
   Create the final deployment orchestrator at `/home/user/migration_project/deploy.sh`. This bash script must:
   - Source `/home/user/migration_project/env_setup.sh`.
   - Compile the Rust application (using `cargo build --release` inside the `rust_app` directory).
   - Start the compiled Rust binary in the **background**.
   - Execute the `init_db_auto.exp` script to initialize the database (this script artificially delays for a few seconds to simulate database startup).
   - `wait` for the backgrounded Rust application to complete its execution.

Ensure all your newly created shell and expect scripts are executable (`chmod +x`). Once you have completed all steps, run `./deploy.sh` to verify your solution works. If successful, `/home/user/migration_project/app.log` will contain the required output.