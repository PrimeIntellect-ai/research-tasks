You are a storage administrator managing a Linux file system that is rapidly running out of space. You suspect that old, nested archive files are hoarding massive log files filled with useless debug information. 

Your task is to identify specific nested archives, extract them, process the log files using a custom C program to strip out debug information, and report the total disk space saved.

Here are your detailed instructions:

1. **Find Target Archives:** 
   Search the directory `/home/user/storage_pool/` (and its subdirectories) for all `.zip` files that were modified **more than 30 days ago**. Ignore any `.zip` files modified more recently.

2. **Extract the Nested Archives:**
   Inside each of the targeted `.zip` files, you will find a `.tar.gz` archive. Extract the `.tar.gz` archive, and then extract its contents. Inside, you will find a single text file with a `.log` extension.

3. **Write a C Log Processor:**
   Write a C program at `/home/user/clean_logs.c`. 
   The program must accept two command-line arguments: an input file path and an output file path.
   Usage: `./clean_logs <input.log> <output.log>`
   The program must read the input file line by line. If a line begins exactly with the string `[DEBUG]`, it should be completely discarded. All other lines must be written unmodified to the output file. 
   Compile your C program using `gcc`.

4. **Process the Logs:**
   Run your compiled C program on every `.log` file extracted from the target archives. For each file, create a cleaned version. 
   
5. **Calculate Space Saved:**
   Calculate the total disk space saved in bytes across all the target logs you processed. The space saved for a single file is the difference in bytes between the original extracted `.log` file and its cleaned version. Sum these differences for all logs originating from the >30-day-old `.zip` files.

6. **Generate the Report:**
   Create a report file at `/home/user/space_saved.txt`.
   The file must contain exactly one line in the following format:
   `Bytes saved: <total_bytes>`
   (Replace `<total_bytes>` with the integer sum of bytes saved).