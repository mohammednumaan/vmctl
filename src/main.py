import typer
from rich import print

import wrapper.host as host_api
import wrapper.libvirt as libvirt_api

VMCTL_BANNER = r"""
                      _   _ 
__   ___ __ ___   ___| |_| |
\ \ / / '_ ` _ \ / __| __| |
 \ V /| | | | | | (__| |_| |
  \_/ |_| |_| |_|\___|\__|_|

"""
app = typer.Typer(no_args_is_help=True)
libvirt = libvirt_api.LibVirtApi()

@app.command()
def about():
    print(VMCTL_BANNER)
    print("""[bold blue]A simple CLI tool to manage VM's using the LibVirt API.[/bold blue]
To get started, type any of the commands vmctl supports.
If you are new, type [green]help[/green] (or) [green]--help[/green] to learn more about [bold blue]vmctl[/bold blue] and what it offers.
""")

@app.command()
def hostinfo():
    libvirt.host_api.get_info()

# these are the commands to manage
# the lifecycle of virtual machines
@app.command()
def list():
    libvirt.vm_api.list_vms()

@app.command()
def provision(vm_name: str, vm_memory: int, vm_vcpus: int, iso_path: str = None, disk_path: str = None):
    libvirt.vm_api.provision_vm(vm_name, vm_memory, vm_vcpus, iso_path, disk_path)

@app.command()
def info(vm_name: str):
    libvirt.vm_api.vm_info(vm_name)
    
@app.command()
def start(vm_name: str):
    libvirt.vm_api.start_vm(vm_name)

@app.command()
def shutdown(vm_name: str):
    libvirt.vm_api.shutdown_vm(vm_name)

@app.command()
def destroy(vm_name: str):
    libvirt.vm_api.destroy_vm(vm_name)


@app.command()
def suspend(vm_name: str):
    libvirt.vm_api.suspend_vm(vm_name)

@app.command()
def resume(vm_name: str):
    libvirt.vm_api.resume_vm(vm_name)

@app.command()
def reboot(vm_name: str):
    libvirt.vm_api.reboot_vm(vm_name)
    
if __name__ == "__main__":
    app()
