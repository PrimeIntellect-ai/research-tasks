I am a network engineer troubleshooting connectivity in a simulated containerized environment. We recently lost our software-defined firewall configuration script due to a bad deployment. However, I managed to recover a screenshot of the firewall rule matrix, which is located at `/app/firewall_rules.png`.

I need you to write a robust replacement script that can be used by our container lifecycle manager to validate outbound connections. 

Create an executable script at `/home/user/fw_check` (you may write it in Bash, Python, or any language of your choice, but it must have the appropriate shebang and be marked executable). 

The script will be invoked with two arguments:
Usage: `/home/user/fw_check <source_service> <destination_ipv4>`

Your script must:
1. Extract the allowed routing rules from the image at `/app/firewall_rules.png`.
2. Check if the provided `<source_service>` is listed in the rules.
3. Check if the provided `<destination_ipv4>` is a strictly valid IPv4 address AND falls within the allowed CIDR block for that specific source service.
4. Print exactly `ALLOW` to standard output if the connection is permitted.
5. Print exactly `DROP` to standard output if the connection is not permitted, if the source service is unknown, if the IP is invalid, or if the wrong number of arguments is provided.

Do not print any additional text, debugging info, or newlines other than the single word `ALLOW` or `DROP`. The script must gracefully handle invalid IPs, malformed inputs, and missing arguments without crashing.