You are a cloud architect tasked with migrating a legacy backup system to a new infrastructure. As part of this migration, you need to replicate the legacy backup naming algorithm, automate an interactive CLI tool, and set up a reverse proxy for the new API.

1. **Legacy Backup Naming Algorithm**
We only have a screenshot of the old documentation at `/app/backup_rules.png`. You must extract the backup naming algorithm, format, and the secret salt from this image.
Write a Go program at `/home/user/backup_name_gen.go` and compile it to an executable at `/home/user/backup_name_gen`. 
The executable must accept exactly two command-line arguments: `<service_name>` and `<date>`. 
It must print the resulting backup string exactly to standard output (with no trailing newline) according to the rules in the image.

2. **Interactive Automation**
The old system has an interactive backup submission tool located at `/app/submit_backup`. Write an Expect script at `/home/user/submit.exp` that takes two command-line arguments (`service_name` and `date`) and automates the execution of `/app/submit_backup`.
The interactive tool will prompt:
- `"Enter service:"` (Provide the first argument)
- `"Enter date:"` (Provide the second argument)
- `"Proceed? [y/N]:"` (Provide `y`)

3. **Reverse Proxy**
Write a simple Go-based reverse proxy at `/home/user/proxy.go` and compile it to `/home/user/proxy`. 
The proxy should listen on `127.0.0.1:8080` and transparently forward all incoming HTTP requests to a backend service running at `127.0.0.1:9090`. Leave the proxy running in the background.

Ensure all compiled binaries (`backup_name_gen` and `proxy`) and scripts (`submit.exp`) are executable and located precisely at the specified paths.