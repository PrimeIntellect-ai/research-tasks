You are an artifact manager tasked with curating and migrating binary repositories. Our system relies on a proprietary legacy archiver called `xpak_pack` to bundle binary and text files into a custom `.xpak` format. Unfortunately, the source code for this archiver was lost, and we only have the stripped compiled binary.

We need to port this functionality to Python to ensure long-term maintainability. 

Your task is to write a Python 3 script at `/home/user/xpak_pack.py` that behaves **exactly** like the legacy binary. It must produce bit-for-bit identical `.xpak` archives and identical manifest files when given the same inputs.

The legacy binary is located at `/app/xpak_pack`. 

Usage of the binary:
`/app/xpak_pack <output_file.xpak> <input_file_1> [<input_file_2> ...]`

When run, the binary produces two files:
1. The compressed archive `<output_file.xpak>`
2. A text-based manifest `<output_file.xpak>.manifest`

You must reverse-engineer the `.xpak` file structure, the custom compression algorithm it uses, and the format of the manifest file by feeding test files into `/app/xpak_pack` and analyzing its output (e.g., using `hexdump`, `xxd`, or Python scripts). 

Your script will be tested against the legacy binary using a rigorous fuzzing suite. The automated verifier will generate dozens of random combinations of binary and text files, pass them to both your script and the legacy binary, and assert that the resulting `.xpak` and `.manifest` files are strictly identical.

Requirements:
- Your script must be executable via: `python3 /home/user/xpak_pack.py <output> <inputs...>`
- It must handle binary and text files of varying lengths.
- It must faithfully replicate the custom compression scheme and metadata layout.
- You may create any temporary files or directories in `/home/user/` to analyze the legacy binary's behavior.