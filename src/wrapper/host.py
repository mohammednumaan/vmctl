from rich.console import Console
from rich.table import  Table


class HostApi:

    def __init__(self, connection):
        self.connection = connection
        self.console = Console()

    def get_hostname(self):
        return self.connection.getHostname()

    def get_max_vCpus(self):
        return self.connection.getMaxVcpus(None)
    
    def get_info(self):
        host_info = self.connection.getInfo()
        rich_table = Table("Model", "Memory Size (in MB)", "Number of CPU's", "MHz of CPU's", "Number of NUMA Nodes", "Number of CPU Sockets", "Number of CPU cores per Socket", "Number of CPU threads per core", title="Host Machine Info")
        
        # unpacking the array to retrieve all the info the libvirt API returned
        model, size, no_cpu, cpu_freq, no_numa_nodes, no_cpu_sockets_per_node, no_cores_per_socket, no_threads_per_core = host_info
        rich_table.add_row(model, str(size), str(no_cpu), str(cpu_freq), 
                str(no_numa_nodes), str(no_cpu_sockets_per_node), str(no_cores_per_socket), 
                str(no_threads_per_core))
        self.console.print(rich_table)
