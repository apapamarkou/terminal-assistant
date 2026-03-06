#!/usr/bin/env python3
"""Setup verification script for terminal-assistant."""

import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Check Python version."""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 11:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} (requires 3.11+)")
        return False


def check_ollama():
    """Check if Ollama is available."""
    try:
        result = subprocess.run(
            ["ollama", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"✓ Ollama installed")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("✗ Ollama not found (install from https://ollama.ai/)")
    return False


def check_git():
    """Check if git is available."""
    try:
        result = subprocess.run(
            ["git", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"✓ Git installed")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("✗ Git not found")
    return False


def main():
    """Run all checks."""
    print("Terminal Assistant - Setup Verification\n")
    
    checks = [
        check_python_version(),
        check_ollama(),
        check_git(),
    ]
    
    print("\n" + "="*50)
    if all(checks):
        print("✓ All checks passed!")
        print("\nNext steps:")
        print("  1. pip install -e .")
        print("  2. ollama serve")
        print("  3. ollama pull codellama")
        print("  4. ai 'hello world'")
    else:
        print("✗ Some checks failed. Please install missing dependencies.")
        sys.exit(1)


if __name__ == "__main__":
    main()
