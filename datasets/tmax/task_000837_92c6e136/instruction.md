You are an operations engineer tasked with recovering critical metadata from an old, nested backup archive. Due to strict storage constraints on this server, you must extract this information *without* extracting the archive contents to disk (i.e., process the nested archives and compressed files entirely in memory/via streams).

A backup archive is located at `/home/user/backup_archive.tar`. 
Inside this uncompressed tarball, there are several compressed tarballs named like `node1_logs.tar.gz`, `node2_logs.tar.gz`, etc.
Inside those inner tarballs, there are multiple gzipped text logs named like `app_log_01.txt.gz`, `app_log_02.txt.gz`.

Within these gzipped text logs, there are scattered metadata lines formatted exactly like this:
`[METADATA-EXPORT] file=/path/to/backed/up/file checksum=a1b2c3d4e5f6...`

Your task is to write a Python script that parses this nested archive structure, reads the gzipped text streams, and extracts all the file paths and their corresponding checksums. 

Output requirements:
Generate a JSON file at `/home/user/metadata_report.json` containing a single dictionary mapping the extracted file paths (keys) to their checksums (values). 

Example of expected output format:
```json
{
    "/etc/config.yml": "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92",
    "/var/log/syslog": "52fdfc072182654f163f5f0f9a621d729566c74d10037c4d7bbb0407d1e2c649"
}
```

Write and execute the Python script to produce the final `metadata_report.json`.