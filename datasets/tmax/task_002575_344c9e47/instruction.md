As a compliance analyst, you are auditing a legacy microservice architecture for a potential JWT vulnerability. A recent security scan flagged that the backend API might be accepting JWTs with no signature (`alg: none`) or tokens that are improperly formatted.

You have two tasks to secure the system:

1. **Fix the API Gateway (Nginx):**
   The system consists of an Nginx reverse proxy (running on port 8080) and a backend Flask API (running on port 5000). The Nginx configuration file is located at `/app/nginx.conf`. Currently, Nginx is stripping the `Authorization` header before forwarding requests to the backend. Modify `/app/nginx.conf` so that the `Authorization` header is correctly passed to the Flask application. You must apply the changes and reload or restart Nginx.

2. **Create an Audit Filter Script:**
   You must write a Bash script at `/home/user/filter.sh` that takes a single argument: the path to a file containing a single JWT token.
   The script must analyze the token and:
   - **Exit with code 0** (Success) if the token is properly structured (contains exactly three base64url-encoded parts separated by periods) AND the algorithm specified in the header is NOT `none` (the check for `none` must be case-insensitive, e.g., `None`, `NONE`, `none` should all be rejected).
   - **Exit with code 1** (Failure) if the token's algorithm is `none` OR if the token is missing the signature part (e.g., ends in a period or has fewer than three parts).

You may use standard Linux command-line utilities (like `jq`, `base64`, `awk`, `cut`, `grep`, etc.) within your Bash script. Make sure your script is executable.

Ensure that the Nginx service on port 8080 properly forwards traffic to port 5000 with the `Authorization` header intact.