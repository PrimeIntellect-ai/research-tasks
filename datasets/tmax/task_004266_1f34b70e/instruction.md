I need your help organizing a large batch of legacy documentation for our new static site generator. 

Our documentation was previously exported from an old content management system into a proprietary format. I have a stripped binary tool provided by the vendor located at `/app/doc-extractor` that can unpack these proprietary files into `.docbundle` files. However, the export process was highly unreliable. Many of the resulting `.docbundle` files are corrupted, malformed, or contain malicious payloads (like zip bombs or infinite nested archives) that completely crash our static site generator.

A `.docbundle` is actually just a nested tar archive. A valid, "clean" `.docbundle` must conform to the following strict structure:
1. When extracted, it must contain exactly one `metadata.json` file at the root, and an `assets/` directory.
2. The `metadata.json` file must be valid JSON and contain a top-level key `"doc_id"` with a string value.
3. The `assets/` directory may contain sub-archives (only `.zip` or `.tar.gz`). If it does, none of these sub-archives can contain other archives (no nesting past level 1 inside `assets/`).
4. All binary image files (`.png` or `.jpg`) inside the unpacked assets must have valid magic byte headers matching their extension.

I have two directories of already unpacked `.docbundle` files to test your solution:
- `/home/user/test_data/clean/`: Contains known good documentation bundles.
- `/home/user/test_data/evil/`: Contains bundles that break the rules above.

Your task is to write a filtering script located at `/home/user/filter_docs.sh`.
Your script must take a single argument: the path to a `.docbundle` file.
It must exit with code `0` if the bundle is perfectly valid (clean) according to the rules above.
It must exit with code `1` (or any non-zero code) if the bundle violates any of the rules (evil).

You can use any programming language you prefer to write the actual logic, as long as `/home/user/filter_docs.sh` acts as the correct entry point. You may reverse engineer or use `/app/doc-extractor` if you need to understand how the vendor structured the files, though your primary goal is to analyze the `.docbundle` files.

Please implement the filter.