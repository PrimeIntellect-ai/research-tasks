You are a backup operator tasked with automating the validation of a legacy backup restore pipeline. Over time, the backup manifest has accumulated corrupted and potentially malicious file paths due to filesystem errors and untrusted user inputs. Before restoring these files, we must aggressively filter the manifest.

Your task involves writing a robust path sanitizer in C and an automation script to test it.

1. **Extract Validation Rules:**
   We have a strict corporate backup path policy, but the original text was lost. The only remaining copy is a screenshot located at `/app/backup_policy.png`. Extract the validation rules from this image (you may use `tesseract` which is pre-installed).

2. **Develop a C Filter:**
   Write a C program at `/home/user/path_filter.c` and compile it to `/home/user/path_filter`. 
   - The program must accept exactly one argument: a file path string.
   - It must apply the rules extracted from the image.
   - If the path perfectly adheres to all rules, the program must print strictly `ACCEPT` to standard output and exit with code `0`.
   - If the path violates ANY rule, contains directory traversal attacks, or possesses shell metacharacters, it must print strictly `REJECT` to standard output and exit with code `1`.

3. **Test with the Corpus:**
   To assist your development, a sample corpus is provided:
   - `/app/corpus/clean.txt`: Contains valid paths (one per line). Your program must ACCEPT all of these.
   - `/app/corpus/evil.txt`: Contains malicious or invalid paths (one per line). Your program must REJECT all of these.
   
4. **Automation Script:**
   Write a bash script at `/home/user/test_restores.sh` that iterates over any given text file of paths, processes them using your compiled `/home/user/path_filter`, and prints a summary report (Total valid, Total invalid). This script should be executable.

Ensure your compiled C program is robust and exactly matches the logic defined in the image, as it will be tested against a hidden, much larger adversarial dataset upon evaluation.