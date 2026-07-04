You are a mobile build engineer maintaining the CI/CD pipelines for a large suite of applications. The build system outputs a metadata manifest of all historical builds, but due to pipeline transmission requirements, the raw data is Base64 encoded.

Your task is to write a Bash script that decodes this data, filters it, performs semantic version comparison to find the latest production release for each application, and outputs the result. 

Specifically, you must:
1. Create a bash script at `/home/user/get_latest_prod.sh`.
2. The script must read the file `/home/user/build_data.b64`. Each line in this file is a Base64-encoded string.
3. When decoded, each line contains data in the format: `AppName,SemanticVersion,Environment` (e.g., `PaymentApp,1.2.14,production`).
4. Your script must filter the records to only include those where the `Environment` is exactly `production`.
5. Group the production records by `AppName`, and determine the *highest* semantic version for each app. (Note: Semantic versioning rules apply, so `2.0.0` is greater than `1.15.0`, and `1.2.0` is greater than `1.2.0-rc1`).
6. The script must write its final output to `/home/user/latest_versions.log`.
7. The format of `/home/user/latest_versions.log` should be one line per application, formatted as `AppName:HighestVersion`, sorted alphabetically by the `AppName`.
8. Once you have written `/home/user/get_latest_prod.sh`, execute it to generate `/home/user/latest_versions.log`.

Make sure your script correctly handles standard semantic version sorting (hint: `sort -V` is very helpful in bash). Run your script and verify that the output log file is generated successfully.