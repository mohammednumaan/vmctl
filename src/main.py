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
def list():
    libvirt.vm_api.list_vms()

@app.command()
def hostinfo():
    libvirt.host_api.get_info()

if __name__ == "__main__":
    app()
