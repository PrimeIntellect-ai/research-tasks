You are an infrastructure engineer automating the provisioning of legacy VM filesystem backups.

We have a set of 10 extracted filesystem backups located in `/home/user/backups/`. Each backup is in a directory named `node_1` through `node_10`. 

These backups have a critical flaw: their SSH configurations (`etc/ssh/sshd_config` inside each backup directory) are currently set to silently reject key-based login (`PubkeyAuthentication no`). 

We need to convert these backup directories into bootable QEMU `.qcow2` images using our proprietary provisioning tool located at `/app/img_builder`. 

Your task is to write a Go program at `/home/user/provision.go` that automates this entire pipeline. The program must:
1. Iterate over all the backup directories in `/home/user/backups/`.
2. Locate the `etc/ssh/sshd_config` file in each directory and patch it so that `PubkeyAuthentication` is set to `yes`.
3. Invoke the `/app/img_builder` tool to build the image. The tool takes two arguments: the input directory and the output file path. The output files should be saved in `/home/user/images/` and named `node_1.qcow2`, `node_2.qcow2`, etc.
4. Set specific environment variables for the `/app/img_builder` process: The tool relies on the system locale and timezone to generate reproducible filesystem timestamps. You must execute the builder with `TZ=UTC` and `LC_ALL=C` in its environment, otherwise the resulting image hashes will fail compliance checks.

**Performance Constraint:** 
The `/app/img_builder` tool is a legacy, stripped binary that takes exactly 1.5 seconds to process a single image. You have a strict time budget. Your Go program must process all 10 nodes and terminate in **under 3.0 seconds**. You will need to implement a concurrent provisioning strategy in your Go code to meet this metric.

The final state should have 10 valid `.qcow2` files in `/home/user/images/`, and your `provision.go` must compile and execute successfully within the time threshold. Do not execute the Go script permanently in the background; our automated testing suite will execute `go run /home/user/provision.go` and measure its execution time and outputs.