You are an infrastructure engineer tasked with automating the provisioning of a custom health-check monitoring service. You need to write a monitoring agent in Go, set up a local mail spool with strict POSIX ACLs, and write a deployment script (a mini CI/CD pipeline) to build and run the service.

Your objective is to complete the following components in the `/home/user/app` directory (you may need to create it):

1. **The Go Monitoring Agent** (`/home/user/app/monitor.go`)
   Write a Go program that acts as a continuous health monitor.
   - It should loop infinitely, pausing for 1 second between iterations.
   - In each iteration, it should read the contents of `/home/user/app/target_status.txt`.
   - If the file contains exactly the string `CRITICAL` (ignoring surrounding whitespace), the monitor must generate an email alert file at `/home/user/app/mail_spool/alert.eml`.
   - The email file must contain exactly the following RFC 5322 formatted text:
     ```
     To: admin@local
     From: monitor@local
     Subject: Service Critical

     The monitored service reported a CRITICAL state.
     ```
   - Immediately after writing the alert file, the Go program must overwrite `/home/user/app/target_status.txt` with the word `OK` to acknowledge the alert and prevent duplicate emails.

2. **The Deployment Pipeline** (`/home/user/app/deploy.sh`)
   Write a bash script that performs the following provisioning and build steps:
   - Create the directories `/home/user/app/bin` and `/home/user/app/mail_spool`.
   - Use `setfacl` to configure default POSIX Access Control Lists (ACLs) on `/home/user/app/mail_spool`. You must ensure that any new file created in this directory automatically inherits the following permissions: read and write for the user (`rw-`), read-only for the group (`r--`), and no permissions for others (`---`).
   - Initialize `/home/user/app/target_status.txt` with the word `OK`.
   - Compile `/home/user/app/monitor.go` into an executable at `/home/user/app/bin/monitor`.
   - Start the compiled monitor executable in the background. It must not block the deployment script.
   - Save the Process ID (PID) of the background monitor process into `/home/user/app/monitor.pid`.

**Constraints and Rules:**
- Do not use root (`sudo`). All commands must be run as the default `user`.
- Ensure `deploy.sh` is executable and run it to start your service before completing your turn.
- Make sure to use absolute paths as specified.
- The Go program should use standard libraries only.