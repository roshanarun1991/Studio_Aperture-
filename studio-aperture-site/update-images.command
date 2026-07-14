#!/bin/bash
cd "$(dirname "$0")"
python3 generate_manifest.py
echo ""
read -p "Press Enter to close this window..."
