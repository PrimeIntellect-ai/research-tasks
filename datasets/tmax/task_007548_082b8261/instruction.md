You are assisting a bioinformatics researcher in recovering and organizing a fragmented dataset. The raw data consists of chunked tarball archives located in `/home/user/dataset_raw/`. Some of these archives are unfortunately corrupted due to a faulty backup drive, while others are intact.

Your objective is to merge the chunks, verify their integrity, extract the valid data, and write a Go program to organize the contents using symbolic links based on parsed metadata.

Follow these steps exactly:

1. **Merge and Verify:**
   In `/home/user/dataset_raw/`, you will find file chunks named like `set1.tar.gz.001`, `set1.tar.gz.002`, etc. 
   - Merge the chunks for each set into a single file (e.g., `set1.tar.gz`).
   - Verify the integrity of each merged `.tar.gz` file. 
   - Extract **only** the archives that are completely valid and uncorrupted into the directory `/home/user/extracted/`. Discard or ignore the corrupted ones.

2. **Understand the Data Format:**
   Inside the valid extracted archives, you will find pairs of files sharing a base name: a text metadata file (e.g., `sample_A.txt`) and a binary data file (e.g., `sample_A.dat`).
   The `.txt` files always contain exactly two lines in this format:
   ```
   ID: <alphanumeric_id>
   Category: <category_name>
   ```

3. **Develop the Go Organizer:**
   Write a Go program at `/home/user/organizer.go` that does the following:
   - Scans the `/home/user/extracted/` directory for all `.txt` files.
   - Parses the `ID` and `Category` from each text file.
   - For every parsed text file, finds its corresponding `.dat` file.
   - Creates a **symbolic link** to the `.dat` file at the following path: `/home/user/organized/<Category>/<ID>.dat`. You must create the `<Category>` directories as needed.
   - Writes a summary log to `/home/user/success.log`. This log must contain a sorted (alphabetical by Category, then by ID) list of the successfully processed files in the exact format: `<Category>:<ID>`. One entry per line.

4. **Execution:**
   - Compile and execute your Go program.
   - Ensure `/home/user/success.log` and the symbolic links in `/home/user/organized/` are correctly generated.