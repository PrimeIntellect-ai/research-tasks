You need to create a Python script that acts as a local generator for a Kubernetes operator. The script will parse a mock `fstab` file to dynamically generate PersistentVolume (PV) manifests and set up a specific directory structure and environment configuration.

Write a Python script at `/home/user/generate_operator_config.py` that does the following when executed:

1. **Locale and Timezone Configuration Script**:
   The script must generate a shell script at `/home/user/operator_env.sh` containing exactly these two lines to standardize the operator's locale and timezone:
   ```bash
   export TZ=UTC
   export LANG=C.UTF-8
   ```
   Writing this file must be idempotent (running your Python script multiple times should safely overwrite or keep the file intact without errors).

2. **Directory Structure and Symlinks**:
   The script must idempotently create the directory `/home/user/operator/manifests/v1`.
   It must then create a symbolic link at `/home/user/operator/active` that points to `/home/user/operator/manifests/v1`. If the symlink already exists, it should be updated or left intact without throwing an error.

3. **Fstab Parsing and Manifest Generation**:
   The script should read a mock fstab file located at `/home/user/mock_fstab`.
   For every entry in the fstab file that has a filesystem type of `ext4`, the script must generate a YAML manifest for a Kubernetes PersistentVolume.
   
   The manifest must be written to `/home/user/operator/active/pv-<basename>.yaml`, where `<basename>` is the last component of the mount point path (e.g., if the mount point is `/data/volume1`, the basename is `volume1`, and the file is `pv-volume1.yaml`).

   The contents of each generated YAML file must be exactly:
   ```yaml
   apiVersion: v1
   kind: PersistentVolume
   metadata:
     name: local-ext4-<basename>
   spec:
     storageClassName: manual
     local:
       path: <mount_point>
   ```
   (Replace `<basename>` and `<mount_point>` with the respective parsed values).

Make sure the Python script is executable or runnable via `python3 /home/user/generate_operator_config.py`.

Assume the `/home/user/mock_fstab` file already exists and uses a standard fstab format (whitespace-separated columns: device, mount_point, fs_type, options, dump, pass). Ensure your fstab parsing handles variable amounts of whitespace.