You are an engineer investigating a severe memory leak in a long-running bash daemon. The service is located in a Git repository at `/home/user/app`. Recently, the service has been crashing due to Out-Of-Memory (OOM) errors. 

Your goals are to investigate the repository, find the historical secret needed to run the service, and isolate the exact commit that introduced the memory leak.

Here are your instructions:
1. **Recover the Secret**: The script `monitor.sh` now requires an `API_KEY` environment variable to run. This key is currently lost, but it was accidentally hardcoded into a configuration file earlier in the Git history before being removed. Find this API key.
2. **Diagnose the Leak**: The `monitor.sh` script tails a dummy log and processes entries in an infinite loop. Identify the bug causing unbounded memory growth (a resource leak) in the bash script.
3. **Bisect the Issue**: Write a minimal test wrapper if necessary, and use `git bisect` (or manual checkout and testing) to find the exact, first commit hash that introduced the memory leak. The repository has several commits; the first few are clean, and a later commit introduces the bug.
4. **Report Findings**: Once you have identified the API key and the exact commit hash that introduced the bug (the "first bad commit"), create a file at `/home/user/report.txt` with exactly the following format:

```text
API_KEY=<the_recovered_api_key>
BAD_COMMIT=<the_full_40_character_commit_hash>
```

Make sure you write the full 40-character git commit hash for `BAD_COMMIT`.