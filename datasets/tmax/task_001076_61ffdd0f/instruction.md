As a storage administrator, I need to clean up our disk space. Our systems have accumulated a large number of ELF binaries, but some of them are corrupted or deliberately bloated with unnecessary data, wasting gigabytes of space.

I have a partially working setup but need you to complete the task. 

First, we are using a vendored version of the `pyelftools` package located at `/app/vendored/pyelftools-0.31`. However, a junior admin accidentally modified some of its source files while trying to debug an issue, and now it fails to recognize any valid ELF files. You need to find and fix this perturbation so the library correctly parses ELF files again. (Do not install `pyelftools` from pip, you must fix and use the vendored version by ensuring `/app/vendored/pyelftools-0.31` is in your PYTHONPATH).

Second, write a Python script `/home/user/elf_filter.py` that takes a single command-line argument (a directory path). The script must:
1. Recursively search the given directory for any files.
2. Efficiently open each file (using standard file streams or mmap).
3. Attempt to parse it using the fixed `elftools.elf.elffile.ELFFile`.
4. Classify the file as `delete` (evil/bad) if ANY of the following are true:
   - It raises an exception during `ELFFile` initialization (i.e., it is corrupted, invalid magic, or points to out-of-bounds offsets).
   - The ELF file contains a section explicitly named `.storage_bloat`.
5. Classify the file as `preserve` (clean/good) if it is a perfectly valid ELF file and does NOT contain the `.storage_bloat` section.
6. Output a JSON file to `/home/user/elf_report.json` containing a dictionary mapping the absolute file path to either the string `"preserve"` or `"delete"`.

A test suite will run your script against two separate directories (one full of valid ELFs, one full of bloated/corrupted ELFs) to verify your logic. Ensure your script handles files robustly without crashing.