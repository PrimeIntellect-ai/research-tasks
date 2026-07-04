I have a compressed archive of application logs located at `/home/user/project/logs.tar.gz`. The archive contains several log files in JSON Lines (JSONL) format. Each line is a JSON object with the following fields: `timestamp`, `level`, `service`, and `message`.

I need you to write a Bash script at `/home/user/project/process_logs.sh` that does the following:
1. Streams the contents of `/home/user/project/logs.tar.gz` without writing the extracted files to disk.
2. Parses the JSON data and filters for records where the `level` is exactly `"ERROR"`.
3. Transforms the filtered records into CSV format containing only the `timestamp`, `service`, and `message` fields, in that exact order.
4. The output CSV should not have a header row, and fields should be properly quoted if they contain spaces or special characters.
5. Pipes the CSV output directly into a gzip-compressed file located at `/home/user/project/error_logs.csv.gz`.

Make sure your script is executable. You can assume `jq` is installed and available on the system. Once you create the script, please run it to generate the output file.