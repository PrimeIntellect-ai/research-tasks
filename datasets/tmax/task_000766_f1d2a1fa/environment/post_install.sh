apt-get update && apt-get install -y python3 python3-pip qrencode ffmpeg coreutils tar
    pip3 install pytest

    # Create mock directory and files
    mkdir -p /tmp/repo
    dd if=/dev/urandom of=/tmp/repo/mock_bin_1.bin bs=1024 count=15
    touch -d '2022-05-01' /tmp/repo/mock_bin_1.bin
    dd if=/dev/urandom of=/tmp/repo/mock_bin_2.bin bs=1024 count=5
    touch -d '2022-05-01' /tmp/repo/mock_bin_2.bin
    dd if=/dev/urandom of=/tmp/repo/mock_bin_3.bin bs=1024 count=15
    touch -d '2024-05-01' /tmp/repo/mock_bin_3.bin

    # Create expected artifact
    mkdir -p /app/.hidden
    cd /tmp/repo
    tar -czf /app/.hidden/expected_artifact.tar.gz *

    # Base64 encode and split
    mkdir -p /tmp/qrs
    base64 /app/.hidden/expected_artifact.tar.gz | tr -d '\n' > /tmp/b64.txt
    split -b 100 /tmp/b64.txt /tmp/chunk_

    # Generate QR codes
    i=0
    for f in /tmp/chunk_*; do
        qrencode -o /tmp/qrs/qr_$(printf "%04d" $i).png -l L < "$f"
        i=$((i+1))
    done

    # Generate video
    ffmpeg -framerate 1 -pattern_type glob -i '/tmp/qrs/*.png' -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -c:v libx264 -pix_fmt yuv420p /app/artifact_feed.mp4

    # Clean up
    rm -rf /tmp/repo /tmp/qrs /tmp/b64.txt /tmp/chunk_*

    # Create user
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user