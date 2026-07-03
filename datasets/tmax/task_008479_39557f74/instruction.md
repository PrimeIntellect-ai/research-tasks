As a security auditor, you have been assigned to test a custom authentication CLI tool developed by the internal infrastructure team. The team uses this tool to manage local configurations, but there are concerns about its security. 

You have been provided with the redacted source code of the tool and the compiled binary:
- Redacted Source Code: `/home/user/audit/admin_cli.go`
- Compiled Executable: `/home/user/audit/admin_cli`

Your objectives are to:
1. Analyze the redacted Go source code to understand the custom authentication token flow and identify the vulnerability class (CWE-798).
2. Reverse engineer or extract the hardcoded secret key from the compiled `admin_cli` binary.
3. Write a Go program at `/home/user/forge.go` that generates a valid token for the username `admin` with the role `superuser`.
4. Run the compiled binary using your forged token to request the restricted flag. The command format is expected to be `./admin_cli --token <YOUR_TOKEN> --action get_flag`.
5. Save the exact generated token to `/home/user/forged_token.txt`.
6. Save the output flag from the binary to `/home/user/flag.txt`.

Ensure your Go code in `forge.go` compiles and runs successfully, and that all requested output files are strictly plain text containing only the expected strings.