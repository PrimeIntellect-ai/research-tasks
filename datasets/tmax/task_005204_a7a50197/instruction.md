I am a network engineer setting up a local network connectivity monitor, but the service keeps crashing and won't restart. I'm using `supervisord` running in user space to manage the service lifecycle.

The monitoring service is located in `/home/user/netmon`. Here is what you need to fix:

1. **Directory & Link Structure Management:** The monitoring script reads its configuration from `/home/user/netmon/config/active.json`. Currently, this is a broken symlink pointing to a missing `development.json` file. Update this symlink to point to the existing `/home/user/netmon/config/available/production.json` file.
2. **Process Supervision & Restart Policy:** The service is configured in `/home/user/netmon/supervisor/conf.d/netmon.conf`. It is currently set to `autorestart=false`. Modify this file to set `autorestart=true` so that the process supervisor will restart it if it drops.
3. **Service Lifecycle:** Once you have fixed the symlink and the configuration, start the supervisor daemon using its main configuration file: `/home/user/netmon/supervisor/supervisord.conf`. (Use `supervisord -c <path_to_conf>`). 
4. **Verification:** The monitoring script will automatically start pinging the simulated network and writing to `/home/user/netmon/logs/connectivity.log`. Wait a few seconds to ensure that the log file is created and contains the message `STATUS: PING_SUCCESS`.

Please perform these steps to get the network monitor running continuously.