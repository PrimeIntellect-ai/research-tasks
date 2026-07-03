You are a data engineer responsible for building out a highly performant, streaming ETL pipeline. A new compliance mandate has been issued regarding our log aggregation streams, but the specific filtering rules were only provided as a scanned image of a memo. 

Your task is to:
1. Locate the scanned policy document at `/app/memo.png`. 
2. Use OCR (e.g., `tesseract` is pre-installed) to extract the text and discover the strict data filtering rules required for our logs.
3. Write a Bash script at `/home/user/filter.sh` that implements these rules. 

Requirements for `/home/user/filter.sh`:
- It must read a stream of log lines from standard input (`stdin`) and write strictly compliant log lines to standard output (`stdout`).
- It must drop/reject any log line that violates the rules extracted from the memo.
- It must NOT use python, perl, or node; you are restricted to bash shell built-ins, standard coreutils (e.g., `grep`, `awk`, `sed`, `uniq`), and basic CLI text processing tools.
- It must handle extremely large streams efficiently (do not load the entire input into memory at once; stream processing is required).
- To monitor the pipeline, your script should optionally log the total number of rejected lines to `stderr` at the end of the stream (this is ignored by the stdout validator).
- Deduplicate: ensure that consecutive identical valid lines are collapsed into a single line.

We will test your script using an automated validation suite that pipes various log files into your script:
`cat test_file.log | bash /home/user/filter.sh > filtered_file.log`

Ensure your script is perfectly accurate. It must completely preserve lines that are compliant, and utterly reject lines that are non-compliant based on the memo.