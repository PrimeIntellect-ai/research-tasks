I am developing a secure REST API in Rust using Axum and SQLx. The project is located in `/home/user/app`, and it will sit behind an Nginx reverse proxy. However, my project currently fails to compile due to missing module declarations and trait bounds, akin to a linker error in C. Furthermore, it's missing some security constraints and proper reverse proxy rate limiting.

Please perform the following tasks:

1. **Fix Compilation Errors:**
   - The Rust project in `/home/user/app` is failing to compile. Fix the code so that `cargo build` succeeds without errors. There is a missing module declaration in `src/main.rs` and missing serialization traits in `src/models.rs`. Do not change the overall architecture or add new dependencies.

2. **Update Request Validation Constraints:**
   - In the registration handler (`src/api.rs`), update the password length validation constraint. For security reasons, the minimum password length must be updated from its current value to require at least `12` characters.

3. **Schema Migration:**
   - There is a schema definition file at `/home/user/app/schema.sql`. Use the `sqlite3` CLI tool to apply this schema to a new database file located at `/home/user/app/data.db`. (Make sure to run this migration so the database has the correct tables).

4. **Nginx Reverse Proxy & Rate Limiting:**
   - I have an Nginx configuration file at `/home/user/nginx.conf`. It currently routes traffic to the Rust backend, but it's missing rate limiting.
   - Modify `/home/user/nginx.conf` to add a rate limit zone named `api_limit` keyed by `$binary_remote_addr` with a size of `10m` and a rate of `5r/s` (5 requests per second). 
   - Apply this rate limit to the `/api/` location block with a `burst` of `10` and the `nodelay` option.

When you have successfully fixed the code, performed the migration, and updated the Nginx configuration, write the word `SUCCESS` to `/home/user/status.log`.