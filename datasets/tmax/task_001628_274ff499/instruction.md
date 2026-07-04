You are acting as a site administrator responsible for modernizing our user account management system. We manage our user definitions in a local Git repository, but we need to generate specific legacy access tokens for every user. 

We lost the source code to the proprietary user token generator, but we have a stripped, compiled version of it located at `/app/user_token_bin`. 

Your task involves the following multi-stage workflow:

1. **Reverse Engineer and Reimplement:**
   Analyze the binary `/app/user_token_bin`. It accepts exactly three arguments: `username` (string), `group` (string), and `uid` (integer). It outputs a token string to standard output. 
   Write a Go program at `/home/user/token_gen.go` and compile it to `/home/user/token_gen`. Your Go program must be EXACTLY behaviorally equivalent to `/app/user_token_bin` for any valid input combination. It must accept the same three command-line arguments and print the exact same token.

2. **Git Hook Configuration:**
   Create a bare Git repository at `/home/user/account_config.git`.
   Implement a `pre-receive` hook in this repository that uses your compiled `/home/user/token_gen` to validate incoming commits. (You don't need to strictly parse the commit contents for the test, just ensure the hook is executable, exists at `/home/user/account_config.git/hooks/pre-receive`, and invokes `/home/user/token_gen testuser testgroup 1000` logging the output to `/home/user/hook_test.log`).

3. **Idempotent Setup:**
   Write a bash script at `/home/user/setup_users.sh` that ensures two dummy users (`appuser1` and `appuser2`) exist on the system with their primary group set to `appgroup`. The script must be idempotent (safe to run multiple times without failure). You have `sudo` access without a password for user management commands if needed, though you can simulate this in a local directory if preferred. (Just write the script, you do not need to execute it).

Your primary goal is ensuring `/home/user/token_gen` is bit-exact equivalent to `/app/user_token_bin`. Our automated verifier will intensely fuzz your Go binary against the oracle.