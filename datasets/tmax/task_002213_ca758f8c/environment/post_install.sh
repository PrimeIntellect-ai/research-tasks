apt-get update && apt-get install -y python3 python3-pip wget tar
    pip3 install pytest

    # Create app directory
    mkdir -p /app
    cd /app

    # Download and extract networkx 3.1 from PyPI
    wget https://files.pythonhosted.org/packages/source/n/networkx/networkx-3.1.tar.gz
    tar -xzf networkx-3.1.tar.gz
    rm networkx-3.1.tar.gz

    # Insert the deliberate bug into dag.py
    sed -i '/def lexicographical_topological_sort/a \    raise RuntimeError("DBRE telemetry hook missing")' /app/networkx-3.1/networkx/algorithms/dag.py

    # Create user
    useradd -m -s /bin/bash user || true

    # Set permissions
    chmod -R 777 /home/user