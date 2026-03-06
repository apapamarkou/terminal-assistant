"""System information collection."""

import platform
import psutil


def get_system_info() -> str:
    """Collect and format system information."""
    os_name = platform.system()
    os_version = platform.release()
    
    # Get CPU info
    cpu_info = platform.processor() or "Unknown"
    
    # Get RAM in GB
    ram_gb = round(psutil.virtual_memory().total / (1024 ** 3))
    
    # Format system info
    info = f"OS: {os_name} {os_version}\n"
    info += f"Kernel: {os_version}\n"
    info += f"CPU: {cpu_info}\n"
    info += f"RAM: {ram_gb}GB"
    
    return info
