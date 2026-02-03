#!/bin/bash
# Simple Automation CLI Installer
# Fast, no-dependencies installation script

set -e

echo "🚀 Installing Simple Automation CLI..."

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
INSTALL_DIR="${HOME}/.local/bin"
PROJECT_DIR="${SCRIPT_DIR}"

# Create installation directory if it doesn't exist
mkdir -p "${INSTALL_DIR}"

# Copy main script
cp "${PROJECT_DIR}/src/main.py" "${INSTALL_DIR}/automation-cli"

# Make it executable
chmod +x "${INSTALL_DIR}/automation-cli"

# Add to PATH if not already there
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
