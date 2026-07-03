You are a script developer building a utility to automate reverse proxy deployments for a set of microservices.

Your task is to write a script in a language of your choice that performs the following steps:

1. Read a YAML file located at `/home/user/routes.yaml`. This file contains a list of services, their API paths, and their target backend URLs.
2. Parse this structured data and extract the mapping of paths to target URLs.
3. Serialize this mapping into a raw JSON object (key: path, value: target) and save it to `/home/user/routes.json`.
4. Generate a valid Nginx configuration file at `/home/user/nginx.conf` that creates a reverse proxy for these services. 

The Nginx configuration MUST meet these requirements:
- It must be able to run entirely in user space (do not require root/sudo).
- It must contain an `events {}` block.
- It must contain an `http {}` block.
- Inside the `http` block, there must be a `server` block listening on port `9000`.
- Inside the `server` block, create a `location` block for each service defined in the YAML file.
- Inside each `location` block, use the `proxy_pass` directive to route traffic to the corresponding target URL.
- Make sure to set `error_log /home/user/error.log;` and `access_log /home/user/access.log;` in the http block so Nginx doesn't try to write to `/var/log`.

Once your script has generated `/home/user/nginx.conf`, verify its syntax using the `nginx -t` command to ensure it is valid. You do not need to start the Nginx server, but the config must pass the test.

Example of what the generated JSON might look like conceptually:
`{"/api/users": "http://127.0.0.1:8081", "/api/orders": "http://127.0.0.1:8082"}`