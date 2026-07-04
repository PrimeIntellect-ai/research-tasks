We have a custom email routing backend that our local Nginx instance proxies requests to. Nginx is currently running on port 8080 (configured via `/home/user/nginx/nginx.conf`), but whenever we send an HTTP POST request with an email payload to `http://127.0.0.1:8080/route`, Nginx returns a 502 Bad Gateway error. 

The original backend service source code was lost, and all we have is a stripped binary located at `/app/email_router_oracle`. This binary accepts a raw email string via standard input and prints the routed mailing list destination to standard output. 

Your task is to:
1. Reverse engineer the `/app/email_router_oracle` binary to understand its routing logic (you can use `strings`, `objdump`, `gdb`, etc.).
2. Re-implement the exact same logic in a C++ program. Save the source code at `/home/user/email_router.cpp` and compile it to `/home/user/email_router`. It must behave identically to the oracle for any given input.
3. Fix the Nginx configuration at `/home/user/nginx/nginx.conf` and create a robust bash wrapper script at `/home/user/start_backend.sh` that uses `socat` or `nc` to serve your new `/home/user/email_router` binary on the port Nginx is expecting (127.0.0.1:9000), thereby fixing the 502 Bad Gateway error.
4. Ensure your script includes proper error handling.

The automated verification will fuzz your `/home/user/email_router` binary against `/app/email_router_oracle` to ensure bit-exact equivalence, and will also send a test HTTP request to Nginx to verify the 502 is resolved.