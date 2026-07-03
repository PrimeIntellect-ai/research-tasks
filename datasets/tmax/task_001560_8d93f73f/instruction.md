I am trying to set up an automated Git-based deployment for my documentation website, but I am running into several issues. My web server Nginx is returning a 502 Bad Gateway for the dynamic rendering endpoint, and 404 for the static content. I need you to fix the environment, write a security filter, and integrate it into my Git workflow.

Here is the setup and the problems:
1. **Nginx Nginx Nginx Configuration:** Nginx is running locally on port 8080 (run Nginx as my user, config at `/home/user/nginx.conf`). It is configured to serve static files from `/home/user/www` and proxy `/render` to a FastCGI wrapper on port 9000.
2. **Directory and Permissions Issues:** The `/home/user/www` directory is supposed to be a symlink pointing to the latest deployed Git commit in `/home/user/deploy/current`. However, the symlink is broken or missing, and the ACLs/permissions on `/home/user/deploy` are preventing Nginx from reading the files. Please fix the directory structure, create the correct symlink, and ensure the files have the correct read permissions.
3. **The 502 Bad Gateway:** The FastCGI wrapper Nginx calls a proprietary markdown rendering engine located at `/app/renderer`. Unfortunately, `/app/renderer` is highly unstable. When users push maliciously crafted markdown files to the repository, the renderer segfaults, causing Nginx to return a 502 Bad Gateway. 
4. **Security Filter:** I have provided a corpus of normal markdown files in `/app/corpus/clean/` and a corpus of malicious files that crash the renderer in `/app/corpus/evil/`. 
   You must investigate `/app/renderer` and the corpora to determine what causes the crash. Then, write a Bash script at `/home/user/filter.sh`. 
   - `filter.sh` must take exactly one argument (a file path).
   - It must exit with `0` if the file is safe to render (clean).
   - It must exit with `1` if the file contains the malicious pattern (evil).
5. **Git Hooks:** Once your filter is working, I need you to prevent malicious files from ever entering my documentation repository. The bare repository is located at `/home/user/site.git`.
   - Implement a `pre-receive` hook in this repository. The hook should extract the incoming files and run `/home/user/filter.sh` on any modified or newly added `.md` files. If `filter.sh` returns `1`, the push must be rejected.
   - Implement a `post-receive` hook that checks out the newly pushed `master` branch into `/home/user/deploy/current`, ensuring that the Nginx static webroot reflects the latest safe content.

Please fix the Nginx Nginx webroot symlinks and permissions, write the robust `filter.sh` script, and fully configure the Git hooks.