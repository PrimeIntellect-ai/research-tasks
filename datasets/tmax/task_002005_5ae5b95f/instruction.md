You are a cloud architect tasked with migrating a set of legacy on-premise services to a modern cloud infrastructure. As part of this migration, we are moving away from an old initialization system to systemd user services, and we need to automatically generate proper configuration IDs for mount points and directory structures based on our legacy rules.

We have a legacy compiled utility located at `/app/legacy_hasher`. In the old system, this utility was used in shell pipelines (alongside awk and grep) to generate unique configuration IDs for various filesystem mount points defined in `fstab`. 

Unfortunately, the source code for this utility has been lost. We need to replace it with a modern, maintainable Python script. 

Your task is to reverse-engineer the `/app/legacy_hasher` stripped binary and write a strictly equivalent Python 3 script at `/home/user/hasher.py`.

Requirements:
1. The script `/home/user/hasher.py` must take exactly one positional argument (an input string representing a path or dependency configuration) and print the generated ID to standard output (with a trailing newline).
2. For ANY valid input string, your Python script must produce the exact same standard output as the `/app/legacy_hasher` binary. 
3. The binary is available in the environment for you to analyze. You may use tools like `strings`, `objdump`, or treat it as a black box to deduce its logic.
4. Ensure your script handles standard ASCII string inputs gracefully.

Write the Python script to perfectly replicate the legacy binary's behavior.