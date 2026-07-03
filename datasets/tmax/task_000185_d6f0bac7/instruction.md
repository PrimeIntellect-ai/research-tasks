You are tasked with implementing a custom configuration archiving tool for our configuration management system. We track thousands of system configuration files, but we only want to back up specific files based on metadata rules and store them in a highly compressed custom format. 

We have lost the source code for our legacy archival tool, but we still have the stripped deployment binary used to extract the archives, located at `/app/config_unpacker`. 

Your objectives are:
1. **Configuration & Metadata Search**: Read the backup rules from `/home/user/backup_rules.json`. This file specifies criteria for which configuration files in the `/home/user/configs/` directory should be archived (e.g., specific extensions, maximum file age in days, and minimum file size). You must write Go code to traverse the directory and filter the files according to these exact rules.
2. **Custom Compression**: Write a Go program (`/home/user/pack.go`) that packs all the filtered configuration files into a single archive file named `/home/user/backup.bin`.
3. **Format Reverse Engineering**: The archive you generate MUST be completely extractable by the `/app/config_unpacker` binary. You will need to analyze the `config_unpacker` binary to determine the correct custom archive format (magic bytes, headers, endianness, compression algorithm, etc.).
4. **Optimization (Metric)**: The final `/home/user/backup.bin` must be highly optimized. Your Go program must produce an archive size that is strictly less than **45,000 bytes**. Default compression levels may not be sufficient to meet this threshold; you will need to maximize the compression efficiency of your payload.

Run your Go script to generate `/home/user/backup.bin`. Do not manually compress the files using shell utilities; the entire search, filtering, and packing process must be implemented in your Go program.