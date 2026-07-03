You are a system administrator tasked with managing custom application logs without relying on standard tools like `logrotate` due to restricted environment constraints. The application writes logs to `/home/user/app_logs/app.log`. 

We have a strict internal quota: the total size of all files in the `/home/user/app_logs` directory must not exceed 10240 bytes (10 KB).

Your task is to write and execute a Go script at `/home/user/rotate.go` that performs the following actions:
1. Calculates the total size (in bytes) of all files in the `/home/user/app_logs` directory.
2. If (and only if) the total size is strictly greater than 10240 bytes, the script must perform a log rotation:
   - Shift existing rotated logs: `app.log.2` becomes `app.log.3`, and `app.log.1` becomes `app.log.2`. (If `app.log.3` already exists, it is overwritten/deleted. Any logs beyond `.3` are not tracked).
   - Move the current `app.log` to `app.log.1`.
   - Create a new, empty `app.log`.
   - Append exactly one line to `/home/user/rotation_status.log` in the following format:
     `ROTATED. Previous directory size: X bytes` 
     (Replace X with the exact total size calculated in step 1).

After writing the script, execute it using `go run /home/user/rotate.go`.

Do not hardcode the total size; your Go script must dynamically calculate it.