You are an AI assistant helping a technical writer organize documentation submissions from various engineering teams. The submissions are located in `/home/user/submissions/`. Because the teams use different tools, the submissions are a chaotic mix of nested archives, multi-part files, and compressed streams.

Your objective is to traverse these archives, find all Markdown files (`*.md`), count their lines, and record the results in a single, shared index file: `/home/user/unified_index.log`.

Because there is a large volume of documentation, you must process the top-level files in `/home/user/submissions/` **concurrently** (in parallel). To prevent data corruption when multiple processes write to the index file at the same time, you must implement strict **file locking**.

Here are your requirements:
1. Write a script (in Python, Bash, Ruby, or Perl) that takes a single top-level archive/compressed file as an argument.
2. The script must inspect the file. If it is an archive (`.zip`, `.tar.gz`, etc.), it must search for all `.md` files inside it. It must also handle nested archives (e.g., a `.zip` inside a `.tar.gz`) recursively up to 2 levels deep.
3. If the script encounters a standalone compressed stream ending in `.stream.gz`, it should NOT extract it to disk. Instead, it must read it on-the-fly via compressed stream processing and count its lines.
4. For every Markdown file or stream found, append a line to `/home/user/unified_index.log` in the exact format: `[TopLevelFileName]::[InternalPath] -> [LineCount]`
   *(Note: For standalone streams, the `InternalPath` is just the stream filename itself without the `.gz` extension).*
5. Your script must use explicit file locking (e.g., `fcntl.flock` in Python, or `flock` in Bash) when opening and writing to `/home/user/unified_index.log`.
6. Finally, execute your script against all items in `/home/user/submissions/` concurrently. For example, if you write a bash wrapper or use `xargs -P` or background jobs (`&`), ensure they run at the same time to prove your locking mechanism works.

Example output format for `/home/user/unified_index.log`:
```
team_alpha.tar.gz::docs/api.md -> 45
team_alpha.tar.gz::legacy.zip/v1.md -> 12
team_beta.zip::readme.md -> 20
team_gamma.stream.gz::team_gamma.stream -> 150
```

Ensure the final `unified_index.log` contains all the markdown files present in the nested structures, completely intact.