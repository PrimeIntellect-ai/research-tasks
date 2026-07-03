You are a container specialist managing a microservices-based mailing list infrastructure. We are deploying a new local SMTP relay and a custom Bash-based email routing service. 

There are two distinct parts to this task:

Part 1: Build and deploy the vendored SMTP relay
We have vendored the source code for `msmtp-1.8.24` at `/app/msmtp-1.8.24`. 
However, a junior developer accidentally introduced a typo into the build system which prevents it from installing correctly.
Your task:
1. Identify and fix the build system perturbation in `/app/msmtp-1.8.24/Makefile.in` (the `install` target has been deliberately broken).
2. Configure (using `--prefix=/home/user/local`), compile, and install the package without using the internet.
3. Create a user-level systemd service unit file at `/home/user/.config/systemd/user/msmtp-relay.service` that runs the installed `msmtpd` daemon. You do not need to start it, but the unit file must exist and point to the correct installed binary.

Part 2: Email Routing Fuzz Equivalence
We use a Bash script to parse incoming email headers and determine which downstream container (represented by a local port) the message should be routed to.
Write a script at `/home/user/mail_router.sh` that takes a single file path as its first argument. The file contains a raw email message.
Your script must output exactly one line in the format: `ROUTE_TO: <PORT>`

The routing rules are:
1. If the `List-Id:` header contains `dev.local`, route to `8081`.
2. If the `List-Id:` header contains `announce.local`, route to `8082`.
3. If there is no `List-Id:` header, but the `Subject:` contains `[URGENT]`, route to `8089`.
4. All other emails should route to the default port `8080`.
Note: Header matching should be case-insensitive.

Your script must be strictly compatible with the expected routing output. An automated fuzzer will run your script against 500 randomly generated email headers and compare the output to a pre-compiled oracle. 

Ensure your script handles standard input securely and efficiently.