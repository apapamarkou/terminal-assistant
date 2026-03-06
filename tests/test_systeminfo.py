"""Tests for system information collection."""

import pytest
from ai.systeminfo import get_system_info


def test_get_system_info():
    """Test system information collection."""
    info = get_system_info()
    
    assert isinstance(info, str)
    assert "OS:" in info
    assert "Kernel:" in info
    assert "CPU:" in info
    assert "RAM:" in info


def test_system_info_format():
    """Test system info is properly formatted."""
    info = get_system_info()
    lines = info.split("\n")
    
    assert len(lines) == 4
    assert lines[0].startswith("OS:")
    assert lines[1].startswith("Kernel:")
    assert lines[2].startswith("CPU:")
    assert lines[3].startswith("RAM:")


def test_ram_in_gb():
    """Test RAM is reported in GB."""
    info = get_system_info()
    
    assert "GB" in info
