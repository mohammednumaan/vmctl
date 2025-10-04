from rich import print
from utils.table import create_table
from utils.xml import create_xml_config
from libvirt import libvirtError
from utils.errors import VmctlError, LibvirtError

# lifecycle management of guest domains
# reference: https://libvirt-python.readthedocs.io/lifecycle-control/

# maybe there is a better way to manage different states of a VM instead 
# the ugly if-else statements
class VMApi:
    def __init__(self, connection):
        self.connection = connection


    def provision_vm(self, vm_name: str, vm_memory: int, vm_vcpus: int, iso_path: str = None, disk_path: str = None):
        # to provision a vm in libvirt, we need to provide a xml file that defines the vm (size, os, disk path)
        # reference: https://libvirt-python.readthedocs.io/domain-config/

        # this is a small design decision i had to make, i.e flexibility vs usability
        # this version of vmctl is going to provide usability over flexibility
        # hence, the user will not be able to provide a custom xml file
        try:
            xml_config = create_xml_config(vm_name, vm_memory, vm_vcpus, iso_path, disk_path)
            if not xml_config:
                return

            domain = self.connection.defineXML(xml_config)
            if domain is None:
                raise VmctlError("Failed to define a domain from the XML configuration.")
            print(f"Domain [bold bright_cyan]{domain.name()}[/bold bright_cyan] has been defined successfully.")
            print("You can start the VM using the command: [green]vmctl start <vm_name>[/green]")
        except libvirtError as e:
            raise LibvirtError(f"Failed to define a domain from the XML configuration: {e}")


    def list_vms(self):
        try:
            domains = self.connection.listAllDomains()
            if not domains:
                print("[bold bright_yellow]No VMs found[/bold bright_yellow]")
                return

            columns = [
                {"header": "VM ID", "style": "bold bright_yellow"},
                {"header": "VM name", "style": "bold bright_cyan"},
                {"header": "VM state"},
            ]
            rows = []
            for domain in domains:
                state, _ = domain.state()
                vm_name = domain.name()
                vm_id = "--" if domain.ID() == -1 else str(domain.ID())

                mappedVmState = self._mapVmStateToString(state)
                mappedVmColor = self._mapStateToColor(mappedVmState)
                rows.append([vm_id, vm_name, f"[{mappedVmColor}]{mappedVmState}[/{mappedVmColor}]"])

            create_table("List of VMs", columns, rows)
        except libvirtError as e:
            raise LibvirtError(f"Error listing VMs: {e}")

    def vm_info(self, vm_name):
        try:
            domain = self.connection.lookupByName(vm_name)
            state, max_mem, curr_mem, no_vcpu, cpu_time = domain.info()

            vm_id = "--" if domain.ID() == -1 else str(domain.ID())
            mappedVmState = self._mapVmStateToString(state)

            title = f"Virtual Machine [bold bright_cyan]{vm_name}[/bold bright_cyan] Info"
            columns = [
                {"header": "VM ID"},
                {"header": "VM name"},
                {"header": "VM state"},
                {"header": "VM current memory"},
                {"header": "VM max memory"},
                {"header": "VM number of vCPU's"},
                {"header": "VM CPU time used"},
            ]
            rows = [[vm_id, vm_name, mappedVmState, str(max_mem), str(curr_mem), str(no_vcpu), str(cpu_time)]]
            create_table(title, columns, rows)
        except libvirtError as e:
            raise LibvirtError(f"Error getting VM info for '{vm_name}': {e}")


    def start_vm(self, vm_name):
        try:
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
        except libvirtError as e:
            raise LibvirtError(f"Error starting VM '{vm_name}': {e}")


    def shutdown_vm(self, vm_name):
        try:
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
        except libvirtError as e:
            raise LibvirtError(f"Error shutting down VM '{vm_name}': {e}")


    def destroy_vm(self, vm_name):
        try:
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
        except libvirtError as e:
            raise LibvirtError(f"Error destroying VM '{vm_name}': {e}")


    def suspend_vm(self, vm_name):
        try:
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
        except libvirtError as e:
            raise LibvirtError(f"Error suspending VM '{vm_name}': {e}")


    def resume_vm(self, vm_name):
        try:
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
        except libvirtError as e:
            raise LibvirtError(f"Error resuming VM '{vm_name}': {e}")


    def reboot_vm(self, vm_name):
        try:
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
        except libvirtError as e:
            raise LibvirtError(f"Error rebooting VM '{vm_name}': {e}")

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