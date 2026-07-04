You are an infrastructure engineer tasked with diagnosing and fixing a service entrypoint script that acts as the main daemon for our data processing application. We are migrating a systemd-based service to run inside a containerized environment, but the startup script keeps crashing on initialization. 

The main service script is located at `/home/user/service/start_service.sh`. When executed, it is supposed to run continuously in the background. However, it currently fails to start and exits with an error.

Your objectives are:

1. **Diagnose and Fix the Service Script:**
   Analyze `/home/user/service/start_service.sh`. You will find that it fails due to filesystem-related assumptions. Modify the script so that:
   - It robustly creates any required directories before trying to use them.
   - It properly handles "stale" PID files (i.e., if the PID file exists but the process ID written inside it is no longer running, it should remove the stale PID file and proceed, rather than crashing). If the process *is* actually running, it should exit with code 1 and print "Service already running".

2. **Start the Service:**
   Once fixed, start the service in the background so it is actively running on the system.

3. **Create a Health Check Script:**
   Write a robust bash script at `/home/user/health_check.sh` that monitors this service. 
   The health check must:
   - Verify that the process ID found in `/home/user/service/run/service.pid` is actively running.
   - Read `/home/user/service/data/status.txt`.
   - If the process is running AND the `status.txt` file contains exactly the word `ACTIVE`, print `HEALTHY` to standard output and exit with code 0.
   - If either condition is not met, print `UNHEALTHY` to standard output and exit with code 1.
   - Make sure `/home/user/health_check.sh` is executable.

Ensure your modifications to `start_service.sh` are robust and that `health_check.sh` performs exactly as specified.