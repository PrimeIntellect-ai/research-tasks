You are a container specialist managing a fleet of microservices backed by QEMU virtual machines. Your team uses a dashboard to monitor storage quotas, but the alerting system is currently down. You only have a screenshot of the recent storage policy dashboard located at `/app/dashboard.png`. 

Your task is to write a Python script `/home/user/manage_storage.py` that automates our disk quota management based on the policy in the image.

The script must do the following:
1. **Extract Policy Threshold**: Programmatically read `/app/dashboard.png` (you may use `pytesseract` and `Pillow`) to extract the "Max Utilization Threshold" percentage (it will be a floating-point number, e.g., 74.2%).
2. **Analyze QCOW2 Images**: The script must accept a directory path as a command-line argument (e.g., `python3 /home/user/manage_storage.py /app/vms/`). This directory contains several QCOW2 disk images.
3. **Calculate Utilization**: For each `.qcow2` file in the directory, use `qemu-img info --output=json <file>` to extract the `actual-size` and `virtual-size`. Calculate the utilization percentage: `(actual-size / virtual-size) * 100`.
4. **Generate FSTAB**: The script must generate a file named `/home/user/fstab_generated`. For every QCOW2 image where the utilization is **strictly less than** the extracted threshold, append an entry to the fstab file to mount it via the `qemu-nbd` tool. 
   The fstab format for each valid image must be exactly:
   `/dev/nbd<X> /mnt/services/<filename_without_ext> ext4 defaults,usrquota 0 2`
   where `<X>` is an auto-incrementing integer starting from 0 for the first valid image processed (sorted alphabetically by filename).

Your script must be robust and handle the standard output of `qemu-img`. Ensure your script runs correctly. A background verification test will run your script against a hidden directory of 100 QCOW2 images to evaluate the correctness of your generated fstab file.

Requirements:
- Only Python 3 is allowed for the script.
- Standard libraries + `Pillow`, `pytesseract` are available.