You are a container specialist managing a deployment environment for a new microservice. The service requires a specific configuration file to set its localization and timezone settings on startup. 

Your task is to create a Python initialization script that generates this configuration file. 

Specifically, you must:
1. Write an executable Python script at `/home/user/init_microservice.py`.
2. The script must use the `argparse` module to accept two optional arguments: `--tz` (for timezone) and `--locale` (for locale).
3. If the script is run without these arguments, it **must** fall back to interactive mode and prompt the user using exactly these strings:
   - `Enter timezone: `
   - `Enter locale: `
4. The script must write the results to a configuration file located at `/home/user/config/app.env`.
5. The output in `/home/user/config/app.env` must be in the following exact format (three lines):
   APP_TZ=<provided_timezone>
   APP_LOCALE=<provided_locale>
   DEPLOY_TIME=<current_UTC_time_in_ISO_8601_format>
   *(Example for DEPLOY_TIME: 2023-10-25T15:30:00.123456)*
6. Ensure the `/home/user/config` directory exists.
7. Make sure your Python script is executable.
8. Finally, execute your script using the command-line arguments to set the timezone to `Asia/Tokyo` and the locale to `ja_JP.UTF-8`, so that the `/home/user/config/app.env` file is generated and populated correctly.