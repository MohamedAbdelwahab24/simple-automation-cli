#!/bin/bash
# Simple Automation CLI Installer
# Fast, no-dependencies installation script

set -e

echo "🚀 Installing Simple Automation CLI..."

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="${SCRIPT_DIR}"

python3 -m pip install --user "${PROJECT_DIR}"

# Ensure local bin is on PATH
INSTALL_DIR="${HOME}/.local/bin"
if [[ ":$PATH:" != *":${INSTALL_DIR}:"* ]]; then
    echo "" >> "${HOME}/.bashrc"
    echo "# Simple Automation CLI" >> "${HOME}/.bashrc"
    echo "export PATH=\"${INSTALL_DIR}:\$PATH\"" >> "${HOME}/.bashrc"
    echo "✓ Added to PATH"
else
    echo "✓ Already in PATH"
fi

# Update PATH in current session
export PATH="${INSTALL_DIR}:${PATH}"

# Verify installation
if command -v automation-cli &> /dev/null; then
    echo ""
    echo "✅ Installation successful!"
    echo ""
    echo "Version: $(automation-cli --version)"
    echo "Location: ${INSTALL_DIR}/automation-cli"
    echo ""
    echo "To start using:"
    echo "  automation-cli --help"
    echo ""
else
    echo "❌ Installation failed"
    exit 1
fi
