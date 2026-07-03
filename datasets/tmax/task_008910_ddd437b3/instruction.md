You are a developer tasked with debugging a critical regression in a Go project located at `/home/user/data-parser`.

The project is a CLI tool that parses and decodes incoming data payloads. Recently, our automated integration tests started failing because the tool cannot decode certain legacy payloads. 

We know the following:
1. The repository currently sits at the `main` branch HEAD, which is broken.
2. The project was working perfectly at the `v1.0.0` tag (which is about 200 commits behind `HEAD`).
3. The failing payload is stored at `/home/user/payload.txt`. 
4. You can run the program using `go run main.go -f /home/user/payload.txt`. When successful, it should exit with code 0 and print the decoded string. Currently, it throws a decoding error.

Your goals are:
1. Perform a `git bisect` between `v1.0.0` and `HEAD` to find the exact commit that introduced the decoding regression. 
2. Write the full 40-character SHA-1 hash of the offending commit to `/home/user/regression_commit.txt`.
3. Fix the bug on the `main` branch. Modify the source code so that `go run main.go -f /home/user/payload.txt` completes successfully.
4. Leave the Git repository on the `main` branch with your uncommitted fix in the working directory.

Important Notes:
- Around halfway through the commit history, a colleague introduced a CGO dependency for performance reasons in another module. If you try to build or run the code in recent commits without the correct environment variables, you will encounter compiler and linker errors (specifically related to a missing math header). You will need to repair the build environment to successfully test commits during your bisection. 
- You may use any bash tools and write wrapper scripts for `git bisect run` to automate the search.