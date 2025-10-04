"""
This module provides a wrapper around the libvirt API, making it easier to use.
"""
import libvirt
from wrapper.host import HostApi
from wrapper.vm import VMApi
from utils.errors import LibvirtError
import sys

class LibVirtApi:
    """
    A wrapper class for the libvirt API.
    """
    def __init__(self):
        """
        Initializes the LibVirtApi class.
        """
        self.connection = self._connect()
        if self.connection is None:
            raise LibvirtError("Failed to establish connection to libvirt.")
        self.host_api = HostApi(self.connection)
        self.vm_api = VMApi(self.connection)


    def _connect(self, uri: str = 'qemu:///system'):
        """
        Connects to the libvirt daemon.

        Args:
            uri (str, optional): The URI to connect to. Defaults to 'qemu:///system'.

        Returns:
            libvirt.virConnect: The connection object.
        """
        try:
            conn = libvirt.open(uri)
            if conn is None:
                raise LibvirtError('Failed to open connection to local qemu.')
            return conn
        except libvirt.libvirtError as e:
            raise LibvirtError(f"Error connecting to libvirt: {e}")

    def close(self):
        """
        Closes the connection to the libvirt daemon.
        """
        try:
            if self.connection:
                self.connection.close()
        except libvirt.libvirtError as e:
            raise LibvirtError(f"Error closing libvirt connection: {e}")