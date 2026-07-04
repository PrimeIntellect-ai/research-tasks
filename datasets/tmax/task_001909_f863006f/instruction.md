You are a storage administrator tasked with cleaning up disk space consumed by massive, poorly-formatted legacy application logs. The company's log retention policy is only available as a scanned image. 

First, locate the policy scan at `/app/storage_policy.png`. You will need to use an OCR tool (like `tesseract`, which is pre-installed) to extract the text from this image. The image contains a configuration block detailing:
1. The target character encoding the logs must be converted to.
2. The specific multi-line log record patterns (e.g., specific severity levels like DEBUG or TRACE) that must be entirely removed to save space. A multi-line log record begins with a timestamp in brackets, e.g., `[YYYY-MM-DD HH:MM:SS]`.
3. A specific bulk renaming prefix for the cleaned files.

Your task is to write a standalone script at `/home/user/log_filter.py` (or `.pl`, `.sh` etc.) that acts as a stream filter. It must read raw log data from standard input (`stdin`) and write the filtered, perfectly formatted log data to standard output (`stdout`). 

Requirements for your script:
- It must handle character encoding conversion as specified in the policy. Assume input logs might be a mix of encodings (like ISO-8859-1), but the output must strictly match the policy.
- It must parse multi-line log records. A record starts with the timestamp header and continues until the next timestamp header.
- It must drop any log record whose header matches the severity level forbidden by the policy document.
- It must retain all other records exactly as they are.

Ensure your program is executable and can handle arbitrary lengths of log data streamed into it.