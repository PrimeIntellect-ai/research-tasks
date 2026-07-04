You are a penetration tester auditing a local highly-secure service. 

An HTTPS service is running on `localhost:8443`. It requires Mutual TLS (mTLS) authentication. 
You have been provided a directory of client certificates and keys in `/home/user/client_certs/`, along with the organization's Certificate Authority (CA) certificate at `/home/user/ca.crt`. 

However, there are three client certificates (`client1.crt`, `client2.crt`, `client3.crt`) and their corresponding keys (`client1.key`, `client2.key`, `client3.key`). Only one of these client certificates is actually valid and signed by the provided `ca.crt`.

Your tasks are:
1. Validate the certificate chains to identify which client certificate was signed by `/home/user/ca.crt`.
2. Connect to the local HTTPS service at `https://localhost:8443/payload` using the valid client certificate and its key. You should also verify the server's certificate using `ca.crt`.
3. The server will return a Base64-encoded string. Decode this payload.
4. The decoded payload will be in the format: `IP:<ip_address>;PORT:<port>;FLAG:<secret_flag>` (e.g., `IP:192.168.1.10;PORT:8080;FLAG:TEST_FLAG`).
5. Extract the `<secret_flag>` and save it to a new file exactly at `/home/user/flag.txt`.
6. Write a Bash script exactly at `/home/user/block_vuln.sh`. This script must contain exactly one `iptables` command that appends (`-A`) a rule to the `OUTPUT` chain to `DROP` all outbound `tcp` traffic destined for the `<ip_address>` and `<port>` extracted from the decoded payload.

Note: You do not need to execute the `block_vuln.sh` script (since you lack root privileges to modify actual firewall rules), but the file must be created and contain the correct command.