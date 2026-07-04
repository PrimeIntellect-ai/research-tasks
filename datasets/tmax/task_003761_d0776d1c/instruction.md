You are tasked with fixing a broken web application stack and reverse-engineering a lost utility.

You are provided with a local Git repository at `/home/user/app-config`. This repository tracks our custom Nginx configuration file, `nginx.conf`. 

Currently, our Nginx server runs as the `user` and listens on port 8080, but it is returning a 502 Bad Gateway error when accessed. The backend application is already running locally and listening on a Unix socket, but the Nginx configuration is pointing to the wrong socket path. 

Your tasks are as follows:

1. **Fix the Nginx Configuration**: Inspect the running system to find the correct Unix socket path for the backend application (a Python process). Update `nginx.conf` in the `/home/user/app-config` repository to use the correct upstream socket path.
2. **Setup Git Hook**: Configure a Git bare repository at `/home/user/deploy.git` and set up the `/home/user/app-config` repository to push to it. Create a `post-receive` hook in the bare repository that automatically copies the pushed `nginx.conf` to `/home/user/nginx/nginx.conf` and reloads Nginx (`nginx -c /home/user/nginx/nginx.conf -s reload`). Push your fixes so that Nginx is reloaded and successfully serves the backend.
3. **Reverse Engineer the Token Generator**: We have a stripped binary located at `/app/token_generator`. It is used to generate access tokens from usernames. The source code was lost. You must analyze this binary and write a Python script at `/home/user/token_generator.py` that replicates its exact behavior. Your script should accept a single string argument and print the exact same output token as the binary. We will test your script against the binary using hundreds of random strings to ensure bit-exact equivalence.

Ensure that your `token_generator.py` is executable and includes the correct shebang. The script must output nothing but the final token to standard out.