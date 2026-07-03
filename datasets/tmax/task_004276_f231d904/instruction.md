You are acting as an observability engineer's assistant. We are deploying a local metric aggregator that feeds into our dashboard. I need you to set up the deployment configuration files, adjust access controls, and write a Python script that generates the final dashboard configuration. 

Please perform the following steps in `/home/user`:

1. **Mount Configuration Setup:**
   Since you don't have root access to modify `/etc/fstab`, create a mock fstab file named `/home/user/metrics_fstab`. It must contain a single valid fstab line that maps the block device `/dev/loop99` to the mount point `/home/user/metrics_data`. Use the `ext4` filesystem. The mount options must be exactly `ro,user,noauto`, and the dump and fsck pass numbers should both be `0`. Use spaces or tabs to separate the fields.

2. **Metrics Directory & ACLs:**
   Create the directory `/home/user/metrics_data`. 
   Our dashboard viewer runs under a specific service account (UID `2048`). Use Access Control Lists (ACLs) to grant this UID explicit read and execute (`r-x`) permissions on `/home/user/metrics_data`. 
   Additionally, set the *default* ACL on this directory so that any newly created files inside it automatically inherit read (`r`) and execute (`x`) permissions for UID `2048`.

3. **System Configuration File:**
   Create a standard INI configuration file named `/home/user/dash_config.ini` with the following contents:
   - A `[Dashboard]` section containing `theme = dark` and `refresh_rate = 15`.
   - A `[Metrics]` section containing `source = /home/user/metrics_data`.

4. **Python Dashboard Tuner:**
   Write a Python script named `/home/user/build_dash.py`. The script must:
   - Read and parse `/home/user/dash_config.ini` using the built-in `configparser` module.
   - Generate a JSON file named `/home/user/dashboard.json` containing the tuned settings. The JSON file must have exactly this structure and types (convert the refresh rate to an integer):
     ```json
     {
       "config": {
         "theme": "dark",
         "refresh": 15
       },
       "status": "tuned",
       "data_source": "/home/user/metrics_data"
     }
     ```
   - Run the script so that `/home/user/dashboard.json` is generated.