from rich import print
from rich.table import Table
from rich.console import Console

# lifecycle management of guest domains
# reference: https://libvirt-python.readthedocs.io/lifecycle-control/

# maybe there is a better way to manage different states of a VM instead 
# the ugly if-else statements
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
            vm_id = "--" if domain.ID() == -1 else str(domain.ID())

            mappedVmState = self._mapVmStateToString(state)
            mappedVmColor = self._mapStateToColor(mappedVmState)

            rich_table = Table(title="List of VMs")
            rich_table.add_column("VM ID", style="bold bright_yellow")
            rich_table.add_column("VM name", style="bold bright_cyan")
            rich_table.add_column("VM state")

            rich_table.add_row(vm_id, vm_name, f"[{mappedVmColor}]{mappedVmState}[/{mappedVmColor}]")
            self.console.print(rich_table)  

    def vm_info(self, vm_name):
        domain = self.connection.lookupByName(vm_name)
        state, max_mem, curr_mem, no_vcpu, cpu_time = domain.info()

        vm_id = "--" if domain.ID() == -1 else str(domain.ID())
        mappedVmState = self._mapVmStateToString(state)

        
        rich_table = Table(title=f"Vritual Machine [bold bright_cyan]{vm_name}[/bold bright_cyan] Info")
        rich_table.add_column("VM ID")
        rich_table.add_column("VM name")
        rich_table.add_column("VM state")
        rich_table.add_column("VM current memory")
        rich_table.add_column("VM max memory")
        rich_table.add_column("VM number of vCPU's")
        rich_table.add_column("VM CPU time used")

        rich_table.add_row(vm_id, vm_name, mappedVmState, str(max_mem), str(curr_mem), str(no_vcpu), str(cpu_time))
        self.console.print(rich_table)


    def start_vm(self, vm_name):
        domain = self.connection.lookupByName(vm_name)
        state, _ = domain.state()
        mapped_vm_state = self._mapVmStateToString(state)

        if mapped_vm_state == "running":
            print(f"VM [bold bright_cyan]{domain.name()}[/bold bright_cyan] is already in [green]running[/green] state.")
        elif mapped_vm_state == "paused":
            print(f"VM [bold bright_cyan]{domain.name()}[/bold bright_cyan] is [cyan]paused[/cyan]. Resume it instead of starting.")
        elif mapped_vm_state == "suspended":
            print(f"VM [bold bright_cyan]{domain.name()}[/bold bright_cyan] is [magenta]suspended[/magenta]. Resume it instead of starting.")
        else:
            domain.create()
            print(f"Started VM [bold bright_cyan]{domain.name()}[/bold bright_cyan]. VM is now in [green]running[/green] state.")


    def shutdown_vm(self, vm_name):
        domain = self.connection.lookupByName(vm_name)
        state, _ = domain.state()
        mapped_vm_state = self._mapVmStateToString(state)

        if mapped_vm_state == "shutoff":
            print(f"VM [bold bright_cyan]{vm_name}[/bold bright_cyan] is already shut off.")
        elif mapped_vm_state == "suspended":
            print(f"VM [bold bright_cyan]{vm_name}[/bold bright_cyan] is suspended. Resume it first.")
        elif mapped_vm_state == "paused":
            print(f"VM [bold bright_cyan]{vm_name}[/bold bright_cyan] is paused. Resume it first.")
        elif mapped_vm_state != "running":
            print(f"VM [bold bright_cyan]{vm_name}[/bold bright_cyan] is not running. Current state is [{self._mapStateToColor(mapped_vm_state)}]{mapped_vm_state}[/{self._mapStateToColor(mapped_vm_state)}].")
        else:
            domain.shutdown()
            print(f"[red]Shutting down[/red] VM [bold bright_cyan]{domain.name()}[/bold bright_cyan].")


    def destroy_vm(self, vm_name):
        domain = self.connection.lookupByName(vm_name)
        state, _ = domain.state()
        mapped_vm_state = self._mapVmStateToString(state)

        if mapped_vm_state == "shutoff":
            print(f"VM [bold bright_cyan]{vm_name}[/bold bright_cyan] is already shut off.")
        elif mapped_vm_state not in ["running", "paused", "blocked"]:
            print(f"VM [bold bright_cyan]{vm_name}[/bold bright_cyan] cannot be forcefully shut down from its current state: [{self._mapStateToColor(mapped_vm_state)}]{mapped_vm_state}[/{self._mapStateToColor(mapped_vm_state)}].")
        else:
            domain.destroy()
            print(f"[red]Forcefully[/red] shutting down VM [bold bright_cyan]{domain.name()}[/bold bright_cyan].")


    def suspend_vm(self, vm_name):
        domain = self.connection.lookupByName(vm_name)
        state, _ = domain.state()
        mapped_vm_state = self._mapVmStateToString(state)

        if mapped_vm_state == "suspended":
            print(f"VM [bold bright_cyan]{vm_name}[/bold bright_cyan] is already suspended.")
        elif mapped_vm_state == "paused":
            print(f"VM [bold bright_cyan]{vm_name}[/bold bright_cyan] is paused. Resume it first.")
        elif mapped_vm_state == "shutoff":
            print(f"VM [bold bright_cyan]{vm_name}[/bold bright_cyan] is shut off. Start it first.")
        elif mapped_vm_state != "running":
            print(f"VM [bold bright_cyan]{vm_name}[/bold bright_cyan] cannot be suspended from its current state: [{self._mapStateToColor(mapped_vm_state)}]{mapped_vm_state}[/{self._mapStateToColor(mapped_vm_state)}].")
        else:
            domain.suspend()
            print(f"[bright_yellow]Suspending[/bright_yellow] VM [bold bright_cyan]{domain.name()}[/bold bright_cyan].")


    def resume_vm(self, vm_name):
        domain = self.connection.lookupByName(vm_name)
        state, _ = domain.state()
        mapped_vm_state = self._mapVmStateToString(state)

        if mapped_vm_state == "running":
            print(f"VM [bold bright_cyan]{vm_name}[/bold bright_cyan] is already running.")
        elif mapped_vm_state == "shutoff":
            print(f"VM [bold bright_cyan]{vm_name}[/bold bright_cyan] is shut off. Start it first.")
        elif mapped_vm_state not in ["paused", "suspended"]:
            print(f"VM [bold bright_cyan]{vm_name}[/bold bright_cyan] cannot be resumed from its current state: [{self._mapStateToColor(mapped_vm_state)}]{mapped_vm_state}[/{self._mapStateToColor(mapped_vm_state)}].")
        else:
            domain.resume()
            print(f"[green]Resuming[/green] VM [bold bright_cyan]{domain.name()}[/bold bright_cyan].")


    def reboot_vm(self, vm_name):
        domain = self.connection.lookupByName(vm_name)
        state, _ = domain.state()
        mapped_vm_state = self._mapVmStateToString(state)

        if mapped_vm_state == "shutoff":
            print(f"VM [bold bright_cyan]{vm_name}[/bold bright_cyan] is shut off. Start it first.")
        elif mapped_vm_state == "suspended":
            print(f"VM [bold bright_cyan]{vm_name}[/bold bright_cyan] is suspended. Resume it first.")
        elif mapped_vm_state == "paused":
            print(f"VM [bold bright_cyan]{vm_name}[/bold bright_cyan] is paused. Resume it first.")
        elif mapped_vm_state != "running":
            print(f"VM [bold bright_cyan]{vm_name}[/bold bright_cyan] cannot be rebooted from its current state: [{self._mapStateToColor(mapped_vm_state)}]{mapped_vm_state}[/{self._mapStateToColor(mapped_vm_state)}].")
        else:
            domain.reboot()
            print(f"[yellow]Rebooting[/yellow] VM [bold bright_cyan]{domain.name()}[/bold bright_cyan].")

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

        
    




