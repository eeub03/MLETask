#!/bin/bash

echo "Starting Repo Setup"

echo "============================================"
echo "Installing UV"
curl -LsSf https://astral.sh/uv/install.sh | sh
echo "Installed UV"

echo "============================================"

echo "Installing python 3.10 via uv"
uv python install 3.10

echo "Python 3.10 successfully installed"
echo "============================================"

echo "Pinning Python version to 3.10"
uv python pin 3.10
echo "Python 3.10 successfully pinned"
echo "============================================"

echo "Creating .venv directory"
uv venv
if [ $? -ne 0 ]; then
  echo "Venv Already exists, Skipping creation of venv"
fi
echo ".venv directory initialised"
echo "============================================"

echo "Starting venv to install as kernel"
source .venv/Scripts/activate
echo "Venv started"

echo "============================================"

echo "Installing venv as ipython kernel"
ipython kernel install --name ".venv" --user
echo "Kernel installed"
echo "============================================"

echo "Deactivating .venv"
source 
echo "Repo setup complete, to start using this venv:"
echo "input'.venv/Scripts/activate' into the cli" 