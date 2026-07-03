You are a security engineer tasked with handling a compromised credential incident and rotating keys for internal services. 

An internal API key, `EXPIRED_SYS_KEY_a8f9`, has been exposed. You have been given access to the system where several internal service configurations are stored, alongside an API access log.

Your objective is to write and execute a Rust program that automates the credential rotation, correlates compromised access, and generates network firewall rules to block attackers.

Here are the specifics of the environment and your task:
1. **Service Configurations**: There are several JSON configuration files located in `/home/user/services/`. Each file represents a service and contains keys like `"service_name"`, `"port"`, and `"api_key"`.
2. **Access Logs**: The file `/home/user/logs/api_access.log` contains recent access logs in the following format:
   `[YYYY-MM-DD HH:MM:SS] IP: <IP_ADDRESS> accessed PORT: <PORT> with KEY: <KEY> result: <SUCCESS|FAILURE>`

Create a Rust project in `/home/user/credential_manager` (you may use `cargo new`) and write a program that performs the following steps when executed:

**Step 1: Service Auditing & Credential Rotation**
Parse all `.json` files in `/home/user/services/`. For any service currently using `EXPIRED_SYS_KEY_a8f9` as its `"api_key"`, update the file in-place to use the new key: `ROTATED_SEC_KEY_b7c2`. Do not alter other fields in the JSON.

**Step 2: Log Parsing & Correlation**
Parse the `/home/user/logs/api_access.log` file. Identify all IP addresses that successfully authenticated (`result: SUCCESS`) using the compromised key (`EXPIRED_SYS_KEY_a8f9`). 

**Step 3: Firewall Policy Generation**
Generate a shell script at `/home/user/firewall_block.sh` to block the malicious IP addresses identified in Step 2.
* **Important Exception**: Any IP address starting with `10.5.` (e.g., `10.5.x.x`) is a known internal service and MUST NOT be blocked, even if it used the compromised key.
* The generated script must contain exactly one line per blocked IP, in this exact format:
  `iptables -A INPUT -s <IP_ADDRESS> -j DROP`
* Sort the `iptables` commands by the IP address in ascending alphabetical/lexicographical order.

Run your Rust program so that the configuration files are updated and the `firewall_block.sh` script is generated. Provide the necessary permissions (`chmod +x`) to the script, but you do not need to execute the firewall script (as you do not have root privileges).