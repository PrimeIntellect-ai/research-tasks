You are tasked with organizing and extracting a large dataset of legacy project archives. 

In `/home/user/dataset/`, there are 1,000 proprietary archive files with the `.parc` extension. These were created by an old, poorly-written archiving tool. We have provided the original tool as a stripped binary at `/app/unpacker`. 

Your goals are to write a high-performance C++ program (`/home/user/fast_extractor.cpp`) that parses and extracts these archives, because the original tool is too slow and has a severe security flaw.

Requirements:
1. **Reverse Engineer the Format**: Use `/app/unpacker` (and standard tools like `xxd`, `strings`, `ltrace`) to figure out the `.parc` binary format and its custom compression scheme. The format contains a magic header, file metadata, and compressed data.
2. **Prevent Zip-Slip**: The original tool blindly trusts file paths. Many archives contain malicious paths like `../../etc/shadow` or `nested/../../../home/user/.bashrc`. Your C++ extractor must neutralize this by flattening the directory structure—extract *every* file directly into `/home/user/output/`, using only the base filename (e.g., `../../a/b/malicious.sh` becomes `/home/user/output/malicious.sh`). If multiple files end up with the exact same base name across the dataset, overwrite the older one (for this task, assume last-writer-wins is acceptable, but you must use file locks if extracting concurrently to avoid corruption).
3. **High Performance**: The extraction process must be fast. You should use concurrent extraction (multi-threading) and efficient binary parsing.
4. **Build and Run**: Compile your program to `/home/user/fast_extractor` and run it on the `/home/user/dataset/` directory.

Success is determined by an automated verifier that will check:
1. **Accuracy**: The MD5 hashes of the files in `/home/user/output/` must match a golden reference (all compression correctly reversed, all zip-slips neutralized).
2. **Performance Metric**: Your extraction program must process the entire dataset significantly faster than a sequential bash script using `/app/unpacker`. 

Please write, compile, and execute your C++ solution. Ensure the final extracted files are resting cleanly in `/home/user/output/`.