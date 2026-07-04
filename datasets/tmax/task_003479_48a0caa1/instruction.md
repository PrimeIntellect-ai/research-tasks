You are an AI assistant helping a system administrator manage configuration files for a legacy server. The configuration manager tracks changes using a custom Write-Ahead Log (WAL) format distributed via compressed archives.

Your objective is to write and execute a Python script that processes a backlog of configuration updates and applies them to a base configuration file.

Here is the setup:
- The working directory is `/home/user/config_manager/`.
- The base configuration file is located at `/home/user/config_manager/system.conf`. It is a standard UTF-8 text file containing `KEY=value` pairs.
- There is a directory `/home/user/config_manager/incoming/` containing several update archives named `update_1.tar.gz`, `update_2.tar.gz`, and `update_3.tar.gz`.

Your Python script must perform the following tasks:
1. Iterate through the `.tar.gz` archives in `/home/user/config_manager/incoming/` in alphabetical order.
2. Extract each archive. Each archive contains a single file named `changes.wal`.
3. Read `changes.wal`. Note that the system generating these logs uses a legacy Windows system, so **the `changes.wal` files are encoded in UTF-16LE**. You must correctly decode them to text.
4. Parse the WAL file and apply its changes to `system.conf` in memory. The WAL file contains one operation per line in the following format:
   - `SET <KEY>=<value>`: Updates the value of the key if it exists, or appends the new `KEY=value` pair to the end of the file.
   - `DELETE <KEY>`: Removes the key and its value from the configuration entirely if it exists.
5. After processing all three archives sequentially, overwrite `/home/user/config_manager/system.conf` with the final updated configuration in UTF-8 encoding. Maintain the original order of the keys, appending newly introduced keys at the bottom in the order they were first added.
6. Finally, create a gzip-compressed tarball of the final configuration file at `/home/user/config_manager/final_backup.tar.gz`. The archive should contain just `system.conf` at its root.

Please write and run the code to accomplish this.