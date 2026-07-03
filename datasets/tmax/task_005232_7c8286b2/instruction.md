You are an observability engineer tasked with tuning dashboards by extracting metrics from a legacy, interactive router CLI. The router CLI does not have an API, so you must automate an interactive session, configure a mock interface, extract traffic metrics, and generate a JSON dashboard configuration.

Your task:
1. Create a Python script at `/home/user/dashboard_updater.py`. You may install necessary packages like `pexpect` locally using `pip install --user pexpect`.
2. The script must interact with the legacy router CLI located at `/home/user/router_cli`.
3. The CLI behaves as follows:
   - It initially prompts for a password: `Password: ` (The password is `adminpass`)
   - The standard prompt is `Router> `
   - Enter `enable` to reach the privileged mode (`Router# `)
   - Enter `configure terminal` to reach configuration mode (`Router(config)# `)
   - Enter `interface tun0` to configure a tunnel interface (`Router(config-if)# `)
   - Set the IP address and subnet mask by sending: `ip address 10.0.0.1 255.255.255.0`
   - Use `exit` to back out of configuration modes until you return to the `Router# ` or `Router> ` prompt.
4. Once the interface is configured, send the command `show interface tun0 metrics` to fetch the raw metric text.
5. Parse the output of this command (using Python string processing, regex, or by piping to external tools like `awk`/`grep` from within your script) to extract the integer values for `Rx_Bytes`, `Tx_Bytes`, and `Drops`.
6. Finally, the Python script must write a JSON file to `/home/user/dashboard.json` with the exact following structure:

```json
{
  "panels": [
    {
      "title": "tun0 Traffic",
      "metrics": {
        "rx_bytes": <integer value of Rx_Bytes>,
        "tx_bytes": <integer value of Tx_Bytes>,
        "drops": <integer value of Drops>
      }
    }
  ]
}
```

Ensure your Python script works autonomously from start to finish. Once you have written and tested your script, run it so that `/home/user/dashboard.json` is generated successfully.