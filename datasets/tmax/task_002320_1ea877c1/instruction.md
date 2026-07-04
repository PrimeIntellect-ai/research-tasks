As a data scientist, I am preparing a large text corpus for language model training. The raw data is highly noisy, containing duplicated lines, inconsistent casing, and unwanted punctuation. 

I have an offline system, and I need you to build a high-performance text deduplication and cleaning pipeline in Rust. 

Here is what you need to do:
1. We have a highly optimized proprietary hashing library located at `/app/text-dedup-engine`. However, the previous engineer left it in a broken state and it currently fails to compile. You will need to diagnose and fix the build issue in this local vendored package.
2. Create a new Rust binary project at `/home/user/dataset_cleaner`.
3. Add the local `/app/text-dedup-engine` crate as a dependency to your project.
4. Your application must read from a raw text dataset located at `/home/user/raw_corpus.txt`.
5. For each line in the dataset, implement the following normalization pipeline:
   - Convert all characters to lowercase.
   - Remove all punctuation (keep only alphanumeric characters and whitespace).
   - Collapse multiple consecutive spaces into a single space, and trim leading/trailing whitespace.
6. Use the `text_dedup_engine::compute_hash(&str) -> u64` function from the fixed vendored crate to hash each normalized line.
7. Perform hash-based deduplication: keep only the first occurrence of each unique hash. 
8. Write the cleaned, unique, normalized lines to `/home/user/clean_corpus.txt`, one line per line, in any order.

The output will be evaluated automatically by an offline metric script that calculates the F1 score of your retained lines against a hidden golden reference. High performance and strict adherence to the normalization rules are essential.