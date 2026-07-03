apt-get update && apt-get install -y python3 python3-pip socat cron netcat-openbsd curl
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    # Create the dummy recording script
    echo '#!/bin/bash' > /home/user/record_capacity.sh
    chmod +x /home/user/record_capacity.sh

    chmod -R 777 /home/user