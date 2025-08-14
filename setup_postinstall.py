#!/usr/bin/env python3

import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd):
    """Run a system command safely."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ {cmd}")
        else:
            print(f"✗ {cmd} failed: {result.stderr}")
    except Exception as e:
        print(f"✗ Error running {cmd}: {e}")


def post_install():

    print("Running post-installation tasks for Liblouis Table Editor...")
    
    # Update desktop database
    run_command("update-desktop-database ~/.local/share/applications/ 2>/dev/null || true")
    run_command("update-desktop-database /usr/share/applications/ 2>/dev/null || true")
    
    # Update MIME database
    run_command("update-mime-database ~/.local/share/mime/ 2>/dev/null || true")
    run_command("update-mime-database /usr/share/mime/ 2>/dev/null || true")
    
    # Update icon caches
    run_command("gtk-update-icon-cache ~/.local/share/icons/hicolor/ 2>/dev/null || true")
    run_command("gtk-update-icon-cache /usr/share/icons/hicolor/ 2>/dev/null || true")
    
    print("Post-installation completed!")


if __name__ == "__main__":
    post_install()
