apt-get update && apt-get install -y python3 python3-pip curl tar golang
    pip3 install pytest

    mkdir -p /app/vendored/archiver
    curl -sL https://github.com/mholt/archiver/archive/refs/tags/v3.1.1.tar.gz | tar -xz -C /app/vendored/archiver --strip-components=1

    # Apply the deliberate perturbation (commenting out path traversal checks)
    sed -i 's/if !strings.HasPrefix(destPath, destDir) {/\/\/ if !strings.HasPrefix(destPath, destDir) {/g' /app/vendored/archiver/zip.go
    sed -i 's/return fmt.Errorf("illegal file path: %s", destPath)/\/\/ return fmt.Errorf("illegal file path: %s", destPath)/g' /app/vendored/archiver/zip.go
    sed -i 's/if !strings.HasPrefix(destPath, destDir) {/\/\/ if !strings.HasPrefix(destPath, destDir) {/g' /app/vendored/archiver/tar.go
    sed -i 's/return fmt.Errorf("illegal file path: %s", destPath)/\/\/ return fmt.Errorf("illegal file path: %s", destPath)/g' /app/vendored/archiver/tar.go

    mkdir -p /opt/oracle
    touch /opt/oracle/process_datasets_oracle
    chmod +x /opt/oracle/process_datasets_oracle

    useradd -m -s /bin/bash user || true
    mkdir -p /home/user/output
    chmod -R 777 /home/user