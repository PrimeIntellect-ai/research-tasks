You are tasked with replacing a legacy, proprietary backup utility with a standard Bash script. 

The company currently uses a compiled executable located at `/app/backup_packer` to package backup payloads. This binary is a "black box" (stripped of debug symbols) that reads a specific JSON format from standard input and outputs a base64-encoded archive to standard output.

We need to deprecate this binary. Your job is to reverse-engineer its behavior and write a 100% compatible Bash script at `/home/user/pack_backup.sh` that produces identically structured and identical bit-for-bit output given the same input.

Requirements for `/home/user/pack_backup.sh`:
1. It must read a JSON payload from `stdin`.
2. It must parse the payload (which contains files, base64-encoded contents, permissions, and an archive prefix).
3. It must use temporary directories securely to stage the files.
4. It must bundle these files into an archive and output the base64-encoded result to `stdout`.
5. The output must perfectly match the output of `/app/backup_packer` for any valid input payload. You will need to carefully analyze the legacy binary's output to determine the exact archive format, metadata (like timestamps, ownership, and permissions), sorting rules, and directory structures it applies.

A sample JSON structure that the tool accepts is:
```json
{
  "prefix": "backup_2024",
  "items": [
    {
      "path": "config/settings.json",
      "content": "ewogICJkZWJ1ZyI6IHRydWUKfQ==",
      "mode": "0644"
    },
    {
      "path": "secrets/keys.txt",
      "content": "c2VjcmV0X2tleV8xMjM0NQ==",
      "mode": "0600"
    }
  ]
}
```

Ensure your script is executable, handles temporary files safely, and leaves no residual files in `/tmp` after execution.