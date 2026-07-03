You are a systems programmer debugging a dynamic linking issue with a C library. The library's build system uses a custom "symbol map" scripting language to dynamically generate the list of exported symbols based on build configurations. 

You have the base script for the old version of the library (`/home/user/v1.sym`) and a patch file (`/home/user/update.patch`) that updates this script to the new version (`v2.sym`).

The symbol map script consists of a sequence of commands executed from top to bottom. The script manipulates an internal, initially empty set of active symbols. The commands are:
- `DEF <symbol_name>`: Adds `<symbol_name>` to the active set.
- `ALIAS <new_name> <existing_name>`: Checks if `<existing_name>` is currently in the active set. If it is, adds `<new_name>` to the active set. If not, does nothing.
- `DROP <symbol_name>`: Removes `<symbol_name>` from the active set if it exists.

Your task is to:
1. Apply the `/home/user/update.patch` to `/home/user/v1.sym`.
2. Write a script in any language (your choice) to interpret the patched `.sym` file and compute the final active set of exported symbols after all commands are executed.
3. Serialize the final set of active symbols as a JSON array of strings, sorted in strictly alphabetical order.
4. Save this JSON array to `/home/user/exported_symbols.json`.

Ensure your final JSON file is strictly formatted as a valid JSON array of strings. Do not include any additional text in the output file.