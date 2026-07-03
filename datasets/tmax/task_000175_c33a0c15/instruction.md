You are helping a deployment engineer update the routing configuration for an internal microservice email delivery system. 

We have a new deployment metadata file located at `/home/user/deploy_data.json`. This file contains an array of service definitions. Each service definition specifies its network configuration and the domain it handles emails for. However, some entries are incomplete due to a misconfigured CI/CD pipeline.

You need to write a robust, idempotent Python script at `/home/user/update_mail_routes.py` that processes this JSON and updates the main email routing configuration file at `/home/user/mail_routing.conf`.

Here are the requirements for your script:
1. Parse `/home/user/deploy_data.json`.
2. For each service in the JSON:
   - Extract the `service_name`, `ip_address`, `port`, and `email_domain`.
   - If `email_domain` is missing, default it to `<service_name>.internal`.
   - If either `ip_address` or `port` is missing, do NOT add this service to the config. Instead, append an error message exactly in this format: `ERROR: Service <service_name> has incomplete network configuration` to `/home/user/deploy_errors.log`.
3. Update the `/home/user/mail_routing.conf` file. For valid services, the file must contain blocks formatted exactly as follows:
   ```
   [<service_name>]
   target = <ip_address>:<port>
   domain = <email_domain>
   ```
4. **Idempotency:** The script must be idempotent. If you run the script multiple times, it must not create duplicate blocks or duplicate error log entries for the same deployment run (for the error log, you can clear it at the start of the script). The `.conf` file might already contain existing blocks; you should update existing blocks if the service name matches, add new blocks, and leave unrelated existing blocks intact. Separate blocks in the `.conf` file with a single blank line.

Please write the script, run it to update the configuration, and ensure the `.conf` and `.log` files are correctly generated.