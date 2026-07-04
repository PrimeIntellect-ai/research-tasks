I am a network engineer trying to set up a custom health check monitoring tool for my infrastructure, but I am running into a few issues. I need you to fix my code, set up the environment, and configure log rotation. 

Here is what you need to do:

1. I have a C++ source file at `/home/user/net_monitor.cpp` that reads an environment variable `TARGET_HOSTS` and simulates a ping check. However, it currently fails to compile because of missing standard library inclusions and a minor syntax error on line 12. Please fix the C++ code and compile it into an executable named `/home/user/net_monitor`.

2. The tool requires the environment variable `TARGET_HOSTS` to be present. Add a line to my `/home/user/.bashrc` file that exports `TARGET_HOSTS="127.0.0.1 1.1.1.1"`.

3. To ensure the filesystem doesn't fill up with monitoring logs, I need you to create a logrotate configuration file specifically for this tool. Create a file at `/home/user/logrotate.conf` that targets the log file `/home/user/logs/net_monitor.log`. The configuration must specify:
   - Daily rotation
   - Keep 3 backlogged versions
   - Compress the rotated files
   - Do not output an error if the log file is missing (`missingok`)

Ensure all files are placed in the exact paths specified.