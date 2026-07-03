I am a researcher organizing a massive, constantly updating dataset of biological sequences. I have a legacy, poorly documented binary utility located at `/app/renamer_utility` that we've been using to generate canonical filenames for our dataset chunks before backing them up. Unfortunately, this utility doesn't handle compressed streams directly and crashes if it encounters infinite symlink loops (which occasionally happen in our messy raw data directories).

I need you to reverse-engineer the naming logic inside `/app/renamer_utility` and write a robust replacement script. Your replacement must:
1. Accept a single filename string as a command-line argument.
2. Print the exact transformed filename to standard output, matching the behavior of `/app/renamer_utility` bit-for-bit on any valid filename string. 

The legacy utility simply takes a filename as an argument and prints the new name. For example: `/app/renamer_utility "sample_data.fasta"`. You can use standard tools like `strings`, `objdump`, or `gdb` to figure out the string transformation rules it applies. 

Please save your final script as `/home/user/new_renamer.sh` (or `.py`, etc., just ensure it's executable and accepts the filename as `$1`). 

In addition to matching the binary's logic for single files, your script must be the core of a new backup workflow we are designing, though for this specific task, we will only strictly verify that `/home/user/new_renamer` produces the exact same output strings as `/app/renamer_utility` across thousands of randomly generated filename inputs.