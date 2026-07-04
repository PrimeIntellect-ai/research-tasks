I need your help to recover and sanitize some lost server configurations. Our configuration manager tracking system crashed, but we have a screen recording of the terminal sessions where an administrator was displaying and modifying the configuration files. 

First, you need to extract and analyze the video located at `/app/config_session.mp4`. The video shows terminal text. You must extract the frames, parse the text to identify the configuration files being displayed, and extract the content of each configuration file.

Second, we've realized that some of these configurations might have been tampered with to include insecure or unauthorized settings (e.g., exposing restricted ports, disabling authentication, or pointing to external unauthorized IP addresses). 

You must write a Python script `/home/user/config_sanitizer.py` that acts as a filter. It should read a configuration file from standard input and do the following:
1. Determine if the configuration is "clean" (safe) or "evil" (unsafe).
2. If it is clean, exit with status code 0.
3. If it is evil, exit with status code 1.

A configuration is considered "evil" if it contains any of the following:
- `PermitRootLogin yes`
- `PasswordAuthentication yes`
- Any IP address outside the `10.0.0.0/8` or `192.168.0.0/16` subnets (except `127.0.0.1`).
- `ListenAddress 0.0.0.0`

Once your script is ready, run it against all the configurations you extracted from the video.
Archive all the "clean" configurations you found in the video into a tar.gz file at `/home/user/clean_configs.tar.gz`. Each file in the archive should be named based on the filename shown in the video (e.g., `sshd_config`, `app_config.json`).

The automated verifier will test your `config_sanitizer.py` script against a hidden adversarial corpus of clean and evil configuration files to ensure it correctly identifies all of them.