You need to complete a custom Rust-based "manifest operator" that manages an Nginx reverse proxy routing to multiple local backend services. The services are already started via a multi-service setup script.

The multi-service environment located at `/home/user/app/start_services.sh` brings up:
1. `backend-a` listening on 127.0.0.1:8081
2. `backend-b` listening on 127.0.0.1:8082
3. `nginx` reverse proxy running as a local user, with its config at `/home/user/app/nginx/nginx.conf`, listening on port 8080.

Your objectives:
1. **Fix the Rust Operator**: In `/home/user/app/operator/`, there is a Rust project. It is supposed to read a routing manifest at `/home/user/app/manifest.yaml`, generate an Nginx configuration, back up the old configuration, write the new one, and reload Nginx. 
   - Edit `src/main.rs` to correctly read the environment variables `MANIFEST_PATH`, `NGINX_CONF_PATH`, and `BACKUP_DIR`.
   - Implement the backup logic in Rust: before overwriting the Nginx configuration, copy the existing config to the `BACKUP_DIR` with the name format `nginx.conf.bak.<unix_timestamp>`.
   - Complete the Nginx config templating logic in the Rust code to correctly map the `path` to the `port` using `proxy_pass` directives.

2. **Environment Variable Setup**: 
   - The operator relies on environment variables. Set them up persistently by appending them to `/home/user/.bash_profile`:
     - `MANIFEST_PATH=/home/user/app/manifest.yaml`
     - `NGINX_CONF_PATH=/home/user/app/nginx/nginx.conf`
     - `BACKUP_DIR=/home/user/app/backups`
   - Ensure the `BACKUP_DIR` directory is created.

3. **Manifest Format**:
   Create the manifest file at `/home/user/app/manifest.yaml` with the following content to route traffic properly:
   ```yaml
   routes:
     - path: /api/a
       port: 8081
     - path: /api/b
       port: 8082
   ```

4. **Integration**: Compile and run the Rust operator so that it generates the new Nginx configuration and reloads Nginx. Ensure that Nginx successfully routes HTTP requests for `/api/a` to port 8081 and `/api/b` to port 8082. Nginx is running locally, and you can reload it using `nginx -c /home/user/app/nginx/nginx.conf -s reload` (the Rust operator should ideally do this or you can test it manually, but the final state must be correctly loaded in the running Nginx on port 8080).

Verify your setup by ensuring `curl http://127.0.0.1:8080/api/a` and `curl http://127.0.0.1:8080/api/b` return successful responses from the respective backends.