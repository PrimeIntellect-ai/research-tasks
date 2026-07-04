We are currently organizing our legacy project files, specifically our database schema migrations. Back in the day, our team used a custom, proprietary schema definition language that was executed by a compiled emulator. 

The compiled emulator is located at `/app/schema_emulator`. Unfortunately, the source code is lost, and the binary is stripped. Recently, our security team discovered a severe web security and command injection flaw in this emulator: it apparently allows arbitrary command execution if a specific, undocumented command-syntax is used in the migration files. 

We have a directory of raw migration files located at `/home/user/raw_migrations/`. 
Your task is to:
1. Reverse-engineer or analyze the `/app/schema_emulator` binary (using `strings`, `objdump`, or black-box execution) to identify the exact syntax or keyword that triggers the unsafe shell execution feature in the custom schema language.
2. Write a Python CLI tool at `/home/user/classifier.py` that implements a detector for this vulnerability.
3. Your tool should take three command-line arguments: the input directory containing `.mig` files, a destination directory for safe migrations, and a destination directory for unsafe/malicious migrations.
   Usage: `python3 /home/user/classifier.py <input_dir> <safe_out_dir> <unsafe_out_dir>`
4. Run your script against `/home/user/raw_migrations/`, outputting the safe files into `/home/user/safe_migrations/` and the malicious files into `/home/user/unsafe_migrations/`.

Your `classifier.py` script must strictly analyze the contents of the files and copy them to the appropriate output directory. It must be robust enough to handle new, unseen migration files using the same proprietary syntax. Do not delete the original files.