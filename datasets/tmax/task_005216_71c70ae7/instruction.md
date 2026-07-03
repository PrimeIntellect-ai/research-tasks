You are tasked with building a tool to organize and orchestrate a multi-language microservices project. 

In `/home/user/`, there is a file called `manifest.json` which describes several services, their dependencies, the language they are written in, and the local port they will run on. Some services are web endpoints, while others are just build-time tasks.

Your task is to write a Rust program in `/home/user/organizer/` (create the cargo project) that does the following:
1. Parses `/home/user/manifest.json`. You may add `serde` and `serde_json` to your `Cargo.toml`.
2. Performs a **topological sort** on the services based on their `deps` (dependencies) field to determine the correct build/execution order.
3. Outputs a comma-separated list of the service names in the resolved topological build order to `/home/user/build_order.txt`.
4. Generates a shell script at `/home/user/build_all.sh` that contains dummy build commands for each service in the resolved order. The build command depends on the `lang` field:
   - For `rust`, echo `cargo build --release --bin <service_name>`
   - For `node`, echo `npm install && npm run build --prefix <service_name>`
   - For `bash`, echo `bash <service_name>.sh`
5. Generates an Nginx reverse proxy configuration at `/home/user/nginx.conf` that routes traffic to the web services. 
   - The Nginx server must listen on port `8080`.
   - Only include services that have a non-null `route` and `port`.
   - The generated configuration must follow this exact format:
```nginx
events {}
http {
    server {
        listen 8080;
        location <route> { proxy_pass http://127.0.0.1:<port>; }
        # ... other locations sorted alphabetically by route
    }
}
```

Make sure to compile and run your Rust program so that `build_order.txt`, `build_all.sh`, and `nginx.conf` are created successfully.

Here is the structure of `manifest.json` you need to parse:
```json
{
  "services": [
    { "name": "auth-service", "lang": "rust", "port": 8081, "deps": ["db-migration"], "route": "/auth" },
    { "name": "api-gateway", "lang": "rust", "port": 8082, "deps": ["auth-service", "user-service"], "route": "/api" },
    { "name": "db-migration", "lang": "bash", "port": null, "deps": [], "route": null },
    { "name": "user-service", "lang": "rust", "port": 8083, "deps": ["db-migration"], "route": "/users" },
    { "name": "frontend", "lang": "node", "port": 3000, "deps": ["api-gateway"], "route": "/" }
  ]
}
```
*(Assume no circular dependencies exist in the manifest).*