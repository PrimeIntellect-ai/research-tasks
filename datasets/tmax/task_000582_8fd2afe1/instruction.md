You are a storage administrator responsible for managing disk space on a heavily utilized file server. 

You have received an automated audio voicemail from the lead architect located at `/app/voicemail.wav`. You need to transcribe or listen to this audio file to find out the name of a recently cancelled project whose data is slated for deletion.

In `/home/user/storage_meta/`, you will find a large number of metadata files in both JSON and CSV formats. These files represent the index of data currently residing on the storage array. Each entry contains a `file_id`, `filename`, `project_code`, and `size_bytes`.

Your tasks are to:
1. Identify the cancelled project code from the audio voicemail.
2. Traverse `/home/user/storage_meta/` and parse all JSON and CSV files to find every file associated with the cancelled project.
3. Calculate the total potential disk space savings (in bytes) if all files for this cancelled project were deleted. Save this exact integer value to `/home/user/reclaimed_bytes.txt`.
4. Create a manifest of all the remaining valid metadata entries (everything NOT belonging to the cancelled project). Use `sed`, `awk`, or `jq` to extract these entries and compile them into a single comprehensive CSV file at `/home/user/active_manifest.csv` with the header `file_id,filename,project_code,size_bytes`.
5. Generate a checksum manifest of all original metadata files in `/home/user/storage_meta/` that contained at least one entry for the cancelled project. Save this as `/home/user/modified_files_checksums.txt` in the standard `sha256sum` output format.

Ensure your parsing robustly handles both JSON and CSV files and accurately sums up the `size_bytes` for the correct `project_code`.