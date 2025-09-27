from rich import print
from rich.table import Table
from rich.console import Console

# lifecycle management of guest domains
# reference: https://libvirt-python.readthedocs.io/lifecycle-control/

class VMApi:
    def __init__(self, connection):
        self.connection = connection
        self.console = Console()

    def list_vms(self):
        domains = self.connection.listAllDomains()
        if not domains:
            print("[bold bright_yellow]No VMs found[/bold bright_yellow]")
        
        for domain in domains:
            state, _ = domain.state()
            vm_name = domain.name()

            mappedVmState = self._mapVmStateToString(state)
            mappedVmColor = self._mapStateToColor(mappedVmState)

            rich_table = Table(title="List of VMs")
            rich_table.add_column("VM name", style="bold bright_cyan")
            rich_table.add_column("VM state")

            rich_table.add_row(vm_name, f"[{mappedVmColor}]{mappedVmState}[/{mappedVmColor}]")
            self.console.print(rich_table)  



    def _mapVmStateToString(self, vm_state):
        string_mapping = {
            0: "no_state",    
            1: "running",     
            2: "blocked",     
            3: "paused",      
            4: "shutdown",    
            5: "shutoff",     
            6: "crashed",     
            7: "suspended", 
        }
        return string_mapping.get(vm_state, "unknown")


    def _mapStateToColor(self, vm_state_string):
        color_mapping = {
            "no_state": "grey50",
            "running": "green",
            "blocked": "blue",
            "paused": "cyan",
            "shutdown": "bright_yellow",
            "shutoff": "yellow",
            "crashed": "red",
            "suspended": "magenta",
            "unknown": "white",
        }
        return color_mapping.get(vm_state_string, "white")

        
    




