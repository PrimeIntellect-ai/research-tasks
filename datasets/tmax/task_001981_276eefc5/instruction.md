You are an infrastructure engineer tasked with building a configuration backup tool.

A previous engineer left a screenshot of the backup filtering rules in `/app/rules.png`. Your objective is to read these rules, find the matching configuration files, convert them, and package them into an archive.

Specifically, you must:
1. Extract the filtering rules from `/app/rules.png` (using OCR tools like `tesseract` which is preinstalled).
2. Write a Bash script at `/home/user/run_backup.sh` that implements the following workflow:
   a. Search the directory specified in the rules for files matching ALL the extracted criteria (e.g., size constraints, extension, and specific content requirements).
   b. Convert all matching configuration files from their original JSON format into YAML format. The converted files should have the `.yaml` extension and reside in their original directory structure (or a flattened staging directory, as long as filenames are preserved without path collisions).
   c. Generate a manifest file at `/home/user/backup_manifest.csv`. This file must be a comma-separated list formatted exactly as `filename.yaml,sha256sum`.
   d. Compress the converted `.yaml` files into a standard gzipped tarball at `/home/user/incremental.tar.gz`.

Ensure your Bash script is robust and correctly applies all the metadata and content-based search filters defined in the image. Do not include files that do not meet the criteria.

Your final output will be graded on the exact precision and recall (F1 score) of the files included in your `incremental.tar.gz` archive compared to the true expected set.