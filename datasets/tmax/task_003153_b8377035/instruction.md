We are testing our backup restoration procedures, but we encountered a critical issue. A cron job that was supposed to process and normalize backup manifests was writing to the wrong path due to environment differences, and the original source code was lost. 

The only surviving documentation of the normalization algorithm is a screenshot of an old specification document located at `/app/backup_spec.png`.

Your task is to:
1. Extract the normalization algorithm rules from the image `/app/backup_spec.png`.
2. Re-implement the normalization program in Rust. Save the source code at `/home/user/packet_normalizer.rs` and compile the executable to `/home/user/packet_normalizer`.
3. The compiled program must accept exactly one command-line argument (the input string), apply the extracted rules in order, and print the resulting string to standard output (without any extra newlines other than the standard trailing newline).

The automated verifier will strictly check your compiled binary against a reference implementation using hundreds of randomly generated inputs to ensure bit-exact equivalence. Ensure your implementation perfectly matches the logic described in the image.