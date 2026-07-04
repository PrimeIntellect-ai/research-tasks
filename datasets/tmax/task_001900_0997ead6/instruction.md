You are a FinOps analyst and system administrator tasked with optimizing cloud storage costs and automating cost reporting. We have an old, undocumented billing binary that calculates exact cloud costs based on proprietary tiering, but it only accepts raw integer byte sizes. 

Your objective is to build a complete FinOps integration environment using C++ and bash.

Here are the requirements:

1. **Storage Topology (Link & Directory Management)**
   Create a directory `/app/data_links`. Inside it, create symlinks for three simulated cloud buckets that point to actual raw directories:
   - `bucket_alpha` -> `/app/raw_data/us-east-1`
   - `bucket_beta` -> `/app/raw_data/eu-west-1`
   - `bucket_gamma` -> `/app/raw_data/ap-south-1`
   (Note: You will need to create the `/app/raw_data/...` directories and populate them with dummy files of any size you choose for testing, but the grading script will replace them with its own sizes).

2. **Mount & fstab Configuration**
   As part of our cost reduction, we are migrating cold storage to specialized mount points. Create a file at `/app/fstab.optimized` containing a standard `fstab` format entry to mount a block device `/dev/sdb1` to `/mnt/cold_archive` using the `ext4` filesystem. To optimize IO costs, ensure the mount options explicitly include `noatime`, `nodiratime`, and `ro`. The dump/pass values should be `0 2`.

3. **Legacy Pricer (Stripped Binary)**
   There is a proprietary, stripped, and compressed executable at `/app/legacy_pricer`. It calculates our custom tiered pricing. 
   - Usage: `/app/legacy_pricer <size_in_bytes>`
   - Output: Prints a floating-point number representing the cost in USD.
   You must reverse-engineer or treat this binary as a black box to understand how it works, but ultimately your C++ service just needs to invoke it.

4. **Multi-Protocol C++ Service & Email Alerting**
   Write a C++ service (source at `/app/finops_service.cpp`, compiled to `/app/finops_service`) that listens on two ports on `127.0.0.1`:
   - **Port 8080 (HTTP):** Must accept `GET /cost?bucket=<bucket_name>`. 
     - It should check the size in bytes of the target directory via the symlinks in `/app/data_links/<bucket_name>`.
     - It must execute `/app/legacy_pricer` with that byte size.
     - It must return an HTTP 200 OK response with the exact body format: `Cost: $<result>`.
     - Authentication: It must enforce a header `Authorization: Bearer finops_secret_2024`. Reject unauthorized requests with 401.
   - **Port 2525 (SMTP):** Must act as a basic SMTP sink to receive automated cost anomaly alerts from our legacy mailing list server. 
     - It only needs to implement enough of the SMTP protocol (`HELO`, `MAIL FROM`, `RCPT TO`, `DATA`, `QUIT`) to accept an email.
     - When an email is received, extract the Subject line. If the subject contains "ALERT", append the subject line to `/app/alerts.log`.

5. **CI/CD Pipeline**
   Create a bash script at `/app/deploy.sh` that acts as a simple CI/CD pipeline:
   - Compiles `/app/finops_service.cpp` using `g++` (ensure you link necessary threads/networking libraries).
   - Verifies that `/app/fstab.optimized` exists.
   - Starts the compiled `finops_service` in the background.
   - Exits with code 0.

Ensure your service continues running in the background after `/app/deploy.sh` completes. Do not rely on root privileges for execution.