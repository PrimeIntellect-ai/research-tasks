You are a DevOps engineer investigating a catastrophic failure in our custom distributed database. The system crashed, leaving behind corrupted journal files and a fragmented code repository.

Your goal is to write a standalone Bash script at `/home/user/process_journal.sh` that parses a raw database journal file and accurately computes the final numeric state of the database, matching our reference implementation perfectly.

Here are your investigation steps and requirements:

1. **Information Extraction (Image):**
   The last screen captured before the kernel panic is saved at `/app/crash_alert.png`. You need to extract the `SALT` value displayed on this screen. (Tesseract is installed on your system).

2. **Git Forensics:**
   The developer who wrote the journal parsing logic accidentally hard-deleted the documentation branch, but the repository is located at `/app/system_repo`. You must explore the git history (e.g., reflogs, deleted commits, or dangling blobs) to find a file named `validation_rules.txt`. This file explains how to identify valid journal entries and skip corrupted ones, as well as the initial state of the database.

3. **Database Recovery Script:**
   Write a Bash script at `/home/user/process_journal.sh`. 
   - It must take a single argument: the path to a journal log file.
   - The journal file consists of lines in the format: `ACTION VALUE CHECKSUM`
   - Using the `SALT` from the image and the rules from `validation_rules.txt`, your script must filter out corrupted lines (invalid checksums) and apply the `ACTION` (which will be `ADD`, `SUB`, or `MUL`) and `VALUE` to the database state sequentially.
   - Your script must output *only* the final integer state of the database to standard output.
   - Intermediate validation: Your script should strictly use Bash built-ins, standard coreutils (like `awk`, `grep`, `sed`), and handle integer arithmetic properly.

Make sure your script perfectly replicates the correct state progression. We will test your script against hundreds of dynamically generated journal logs to ensure bit-exact equivalence with our internal recovery oracle.