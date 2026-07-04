You are an artifact manager responsible for curating a secure binary repository. Your team has instituted a new strict policy for admitting executable artifacts into the repository.

You have been provided an image containing handwritten notes from the security team detailing the new binary curation policy. This image is located at:
`/app/policy.png`

Your task is to write a standalone Bash script located at `/home/user/parse_elf.sh` that implements this exact policy.

Requirements for `/home/user/parse_elf.sh`:
1. The script must take exactly one argument: the absolute path to a file.
2. It must use standard Linux utilities (like `readelf`, `file`, `grep`, `awk`, etc.) to analyze the provided file. No Python or Perl allowed—pure Bash and coreutils/binutils only.
3. It must analyze the file according to the ordered criteria found in the `/app/policy.png` image.
4. It must output a single line to `stdout` strictly formatted as specified in the image.
5. Make sure the script is executable (`chmod +x`).

The evaluation system will test your script against hundreds of different files (valid ELFs, invalid architectures, non-ELF files, etc.) and strictly compare its `stdout` output against our reference implementation. Ensure you perfectly handle the fallback states and order of evaluation as described in the image.