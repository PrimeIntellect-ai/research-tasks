You are acting as a systems engineer for a capacity planning team. We need to set up a local Git-based deployment pipeline that extracts resource requirements from application code whenever a new version is deployed. 

You must implement a Git `post-receive` hook written entirely in **Rust**.

Here are your instructions:

1. **Repository Setup**:
   - Create a bare Git repository at `/home/user/app.git`.
   - Create a deployment directory structure: `/home/user/deploy/releases`.

2. **The Rust Git Hook**:
   - Create a Rust project to build your hook.
   - The compiled binary must be placed at `/home/user/app.git/hooks/post-receive` and be executable.
   - When a `git push` occurs, the `post-receive` hook receives lines on standard input in the format: `<oldrev> <newrev> <refname>`.
   - For each line read from stdin, your Rust hook must:
     a. Extract the `<newrev>` (the commit hash).
     b. Create a directory for the release: `/home/user/deploy/releases/<newrev>`.
     c. Check out the files of `<newrev>` into that release directory. (Hint: use `git --work-tree=... --git-dir=... checkout -f <newrev>`).
     d. Force-update a symlink at `/home/user/deploy/current` to point to `/home/user/deploy/releases/<newrev>`. This simulates a rolling deployment.
     e. Read the contents of the file `capacity_reqs.txt` from the newly deployed release directory.
     f. Append a single line to `/home/user/deploy/planner_log.txt` with the exact format:
        `DEPLOYMENT <newrev> REQUIRES <contents of capacity_reqs.txt>`
        (Assume `capacity_reqs.txt` contains a single line of text with no trailing newline, or strip the trailing newline if present).

3. **Test the Pipeline**:
   - Clone the bare repository to `/home/user/workspace`.
   - In `/home/user/workspace`, create a file named `capacity_reqs.txt` containing exactly: `CPU: 4 cores, RAM: 16GB`
   - Commit this file with the message "Initial capacity specs".
   - Push the commit to the bare repository at `/home/user/app.git`.
   - Modify `capacity_reqs.txt` to: `CPU: 8 cores, RAM: 32GB`
   - Commit this change with the message "Scale up capacity".
   - Push this second commit to the bare repository.

By the end of this task, the automated test will verify that:
- The `post-receive` hook is a compiled Rust binary.
- The `/home/user/deploy/current` symlink points to the latest commit's release directory.
- The `/home/user/deploy/planner_log.txt` contains exactly two lines formatted as specified above, corresponding to your two pushes.