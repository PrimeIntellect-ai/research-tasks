You are a container specialist managing a custom microservice deployment pipeline. Your objective is to build a mini CI/CD pipeline from scratch in the terminal that compiles a C-based authentication daemon, tests it interactively using `expect`, and deploys it to a local filesystem directory. 

You must complete the following steps. Please create all necessary directories.

1. **Create the Microservice (C Programming)**
Create a C program at `/home/user/microservice/auth_daemon.c`. This program must:
- Read an environment variable named `AUTH_STORE` which contains the absolute path to a text file.
- If the environment variable is not set, or the file cannot be opened, exit with status code 1.
- Read the file, which contains one username per line.
- Enter an interactive loop where it prompts exactly: `Enter username: ` (without a newline after the colon, but with a space).
- Read the input from `stdin`.
- If the input matches a username in the file (exactly), print `Access Granted\n`.
- If the input does not match, print `Access Denied\n`.
- If the input is exactly `QUIT`, exit with status code 0.

2. **Create the Interactive Test (Expect Scripting)**
Create an expect script at `/home/user/microservice/test_auth.exp`. This script must:
- Spawn the compiled `./auth_daemon` executable.
- Wait for the `Enter username: ` prompt.
- Send the username `service_account` and expect `Access Granted`.
- Wait for the next `Enter username: ` prompt.
- Send the username `hacker` and expect `Access Denied`.
- Wait for the next `Enter username: ` prompt.
- Send `QUIT` and expect the program to exit cleanly.
- If all checks pass, exit with status 0. Otherwise, exit with status 1.

3. **Create the CI/CD Pipeline (Bash & Shell Setup)**
Create a bash script at `/home/user/microservice/ci_pipeline.sh`. The script must perform the following exactly:
- Create the directory `/home/user/data/` and a file `/home/user/data/users.txt` containing two lines: `admin` and `service_account`.
- Compile `/home/user/microservice/auth_daemon.c` using `gcc` to an executable named `auth_daemon` in the same directory.
- Export the environment variable `AUTH_STORE=/home/user/data/users.txt`.
- Execute the expect script `/home/user/microservice/test_auth.exp`.
- If the expect script exits with 0 (success):
  - Create the directory `/home/user/deploy/bin/`.
  - Copy `auth_daemon` to `/home/user/deploy/bin/auth_daemon`.
  - Create a log file at `/home/user/deploy/deploy.log` containing exactly the string: `CI pipeline passed`
- If the expect script fails, the script should exit and not deploy.

4. **Environment Setup**
Append the line `export PATH=$PATH:/home/user/deploy/bin` to the file `/home/user/.bashrc`.

Once you have written all the files, manually execute `/home/user/microservice/ci_pipeline.sh` so the pipeline runs, the C program is compiled, tested, and deployed.