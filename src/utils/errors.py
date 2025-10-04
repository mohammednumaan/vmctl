"""
This module defines the custom exception classes and the centralized error handler for vmctl.
"""
from rich import print

class VmctlError(Exception):
    """Base class for all vmctl errors."""
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class LibvirtError(VmctlError):
    """Raised for libvirt-related errors."""
    def __init__(self, message):
        super().__init__(message)
        self.message = message

def handle_error(e: Exception):
    """Prints a user-friendly error message."""
    if isinstance(e, VmctlError):
        print(f"[bold red]Error:[/bold red] {e.message}")
    else:
        print(f"[bold red]An unexpected error occurred:[/bold red] {e}")