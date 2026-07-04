A former researcher in our lab left behind a proprietary dataset processing tool, but the source code was lost. We only have a stripped compiled binary located at `/app/dataset_packager`. 

We need you to reverse-engineer what this binary does and write an exact functional replacement. Your replacement can be written in any language of your choice, but must be invokable via a shell script or executable at `/home/user/my_packager`.

The original binary is invoked like this:
`/app/dataset_packager <input_file.json> <output_dir>`

Based on our notes, the tool does the following for a given input JSON file:
1. Parses the structured JSON data.
2. Performs a custom "compression" or binary serialization of the dataset into a specific binary format.
3. Uses atomic writes (managing a temporary file before renaming) to safely write the binary file.
4. Uses symbolic linking to organize the output by dataset categories.

Your task:
1. Analyze the `/app/dataset_packager` binary to understand its custom binary format, file naming conventions, and symbolic link logic. You can test it by passing dummy JSON files to it and observing the outputs and filesystem changes.
2. Create an executable script or compiled program at `/home/user/my_packager` that takes the same two arguments (`<input_file.json> <output_dir>`).
3. Your implementation must exactly replicate the behavior of the original binary for any valid JSON input conforming to the same schema. It must produce bit-exact identical binary files, the identical atomic write pattern (write to a temporary file first, then rename), and the exact same symbolic links in the output directory.

Ensure your script is marked as executable (`chmod +x /home/user/my_packager`). The automated verifier will fuzz both the original binary and your script with thousands of random JSON files to ensure absolute equivalence in the output directory structure, file metadata, symlinks, and binary file contents.