You are a monitoring specialist setting up an automated deployment pipeline for a custom process alert tool. 

A target process is currently running on the system, and its Process ID (PID) has been saved in `/home/user/target.pid`. 
A bare Git repository has been initialized at `/home/user/monitor.git`.

Your task is to implement the monitoring tool in C++ and set up a deployment hook so that pushing the code automatically compiles it.

Perform the following steps:
1. Create a `post-receive` hook in the bare repository (`/home/user/monitor.git/hooks/post-receive`). The hook must do the following when code is pushed:
   - Create the directories `/home/user/deploy` and `/home/user/bin` if they do not exist.
   - Checkout the pushed code into the work tree at `/home/user/deploy` (using `git checkout -f`).
   - Compile a file named `monitor.cpp` located in `/home/user/deploy` into an executable at `/home/user/bin/monitor` using `g++`.
   - Set the permissions of `/home/user/bin/monitor` to `755` (rwxr-xr-x).
   - Ensure the hook itself is executable.

2. Clone the bare repository to `/home/user/workspace`.

3. Inside `/home/user/workspace`, write a C++ program named `monitor.cpp`. The program must:
   - Read the PID from `/home/user/target.pid`.
   - Read the process command name from `/proc/<PID>/comm` (where `<PID>` is the integer read from the file).
   - Strip any trailing whitespace or newlines from the command name.
   - Append exactly the following string to `/home/user/alerts.log`:
     `ALERT: Process <name> (PID <pid>) detected` followed by a newline.
     (For example: `ALERT: Process sleep (PID 1234) detected`)

4. Commit `monitor.cpp` to the repository and push it to the `master` branch of the bare repository (the remote).

5. Finally, manually execute the newly deployed binary `/home/user/bin/monitor` to generate the log entry in `/home/user/alerts.log`.