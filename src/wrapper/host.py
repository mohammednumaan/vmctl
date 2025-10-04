"""
This module provides a class for interacting with the host machine's libvirt API.
"""
from rich.console import Console
from rich.table import  Table
from libvirt import libvirtError
from utils.errors import LibvirtError

class HostApi:
    """
    A class for interacting with the host machine's libvirt API.
    """

    def __init__(self, connection):
        """
        Initializes the HostApi class.

        Args:
            connection (libvirt.virConnect): The connection object.
        """
        self.connection = connection
        self.console = Console()

    def get_hostname(self):
        """
        Gets the hostname of the host machine.

        Returns:
            str: The hostname of the host machine.
        """
        try:
            return self.connection.getHostname()
        except libvirtError as e:
            raise LibvirtError(f"Error getting hostname: {e}")

    def get_max_vCpus(self):
        """
        Gets the maximum number of vCPUs supported by the host machine.

        Returns:
            int: The maximum number of vCPUs.
        """
        try:
            return self.connection.getMaxVcpus(None)
        except libvirtError as e:
            raise LibvirtError(f"Error getting maximum vCPUs: {e}")
    
    def get_info(self):
        """
        Gets information about the host machine and displays it in a table.
        """
        try:
            host_info = self.connection.getInfo()
            rich_table = Table("Model", "Memory Size (in MB)", "Number of CPU's", "MHz of CPU's", "Number of NUMA Nodes", "Number of CPU Sockets", "Number of CPU cores per Socket", "Number of CPU threads per core", title="Host Machine Info")
            
            # unpacking the array to retrieve all the info the libvirt API returned
            model, size, no_cpu, cpu_freq, no_numa_nodes, no_cpu_sockets_per_node, no_cores_per_socket, no_threads_per_core = host_info
            rich_table.add_row(model, str(size), str(no_cpu), str(cpu_freq), 
                    str(no_numa_nodes), str(no_cpu_sockets_per_node), str(no_cores_per_socket), 
                    str(no_threads_per_core))
            self.console.print(rich_table)
        except libvirtError as e:
            raise LibvirtError(f"Error getting host information: {e}")