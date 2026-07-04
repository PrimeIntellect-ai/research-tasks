You are acting as a storage administrator. We recently had an issue where our automated archive extraction service filled up our disk space and triggered several security alerts. We suspect some archives attempted a "zip slip" attack (directory traversal using `../` or `..\` in the extraction paths) and were quarantined by the system.

You need to analyze the service logs and the quarantined binary files to generate a forensic report.

Here are the details:
1. There is a log file located at `/home/user/extraction_logs.dat`. It is encoded in `UTF-16LE`.
2. The log file contains multi-line records formatted exactly like this:
   ```
   BEGIN_RECORD
   Timestamp: <ISO-8601>
   ArchiveID: <string>
   ExtractedTo: <file path>
   Status: <SUCCESS|QUARANTINED|FAILED>
   END_RECORD
   ```
3. A "zip slip" attempt is defined as any record where the `ExtractedTo` path contains the substring `../` or `..\`. 
4. The system automatically quarantined some files. You must find all records that are BOTH a zip slip attempt AND have a Status of `QUARANTINED`.
5. For each matching record, note its `ArchiveID`.
6. Go to the `/home/user/quarantine/` directory. For each identified `ArchiveID`, there will be a corresponding binary file named `<ArchiveID>.bin`.
7. Read the first 16 bytes of each corresponding binary file.
8. Generate a final report at `/home/user/zip_slip_report.txt` encoded in standard `UTF-8`.
9. The report must contain exactly one line per identified zip slip ArchiveID, formatted as `ArchiveID:<lowercase hex string of the first 16 bytes>`.
10. The lines in `/home/user/zip_slip_report.txt` must be sorted alphabetically by the `ArchiveID`.

Use Python to write a script that accomplishes this task.